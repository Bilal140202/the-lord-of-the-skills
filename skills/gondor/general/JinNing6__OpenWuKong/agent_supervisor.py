# -*- coding: utf-8 -*-
"""
agent_supervisor.py — 通用 IDE Agent 全时督导器

适用场景：任何通过智能 IDE（Cursor/Antigravity/VS Code + AI Agent）执行的任务。
科研跑分、功能开发、Bug 修复、UI 设计、部署运维……所有 Agent 任务皆可督导。

设计灵感：借鉴 OpenClaw 龙虾项目的 subagent-lifecycle-events（细粒度生命周期）、
subagent-control（steer 续发机制 + 速率限制）、cascade-kill（级联终止）模式。

核心逻辑：
  监控 → Agent 空闲? → 读取对话 → 达标? → YES: ✅ → NO: steer 续发指令
  监控 → Agent 报错?                           → 自动重试
  监控 → Agent 超时?                           → stall 检测 → 续发

使用：
    # 生成配置模板
    python agent_supervisor.py --gen-config goals.json

    # 启动督导（自动操控）
    python agent_supervisor.py --config goals.json

    # 演示模式（只读不操作）
    python agent_supervisor.py --config goals.json --demo

    # 24 小时全时运行
    python agent_supervisor.py --config goals.json --max-hours 24
"""

from __future__ import annotations

import sys
import io
import os
import json
import time
import enum
import uuid
import dataclasses
from typing import Optional
from datetime import datetime

import psutil
from pywinauto import Desktop
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

from logger import get_logger, log_event
from ai_monitor import MultiProjectAIMonitor, AIStatus, AIProjectState

logger = get_logger("supervisor")

# 注: UTF-8 由 ai_monitor.py 统一处理，此处无需重复包装


# ═══════════════════════════════════════════════
#  生命周期事件（借鉴 OpenClaw subagent-lifecycle-events）
# ═══════════════════════════════════════════════

class LifecycleEvent(enum.Enum):
    """Agent 生命周期事件类型——比简单的 Running/Idle 更细致"""
    SPAWNED = "spawned"             # 首次探测到 Agent 运行
    RUNNING = "running"             # Agent 持续运行中
    COMPLETED = "completed"         # Agent 完成一轮 (Running→Idle)
    ERROR = "error"                 # Agent 报错
    STALLED = "stalled"             # Agent 长时间无变化
    STEERED = "steered"             # 已发送续发指令
    GOAL_ACHIEVED = "goal-achieved" # 目标达成
    GOAL_FAILED = "goal-failed"     # 达到重试上限
    KILLED = "killed"               # 被手动终止


class GoalStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    CHECKING = "checking"
    ACHIEVED = "achieved"
    STALLED = "stalled"
    FAILED = "failed"


# ═══════════════════════════════════════════════
#  任务目标（通用）
# ═══════════════════════════════════════════════

@dataclasses.dataclass
class TaskGoal:
    """
    单个任务目标——适用于任何 IDE Agent 可执行的工作
    """
    # ── 匹配 ──
    window_match: str               # 窗口标题匹配关键词

    # ── 目标 ──
    task_name: str                  # 任务名称
    goal: str                       # 目标描述（给人看的）
    success_keywords: list[str]     # 成功信号
    failure_keywords: list[str]     # 失败信号

    # ── Steer 行为（借鉴 OpenClaw steer 机制）──
    retry_command: str              # 未达标时续发的指令
    max_retries: int = 30           # 最大续发次数
    cooldown_sec: float = 10.0      # 两次续发最小间隔（速率限制）
    stall_timeout: float = 600.0    # 无变化超时（秒）

    # ── 运行时（不写入配置）──
    status: GoalStatus = GoalStatus.PENDING
    retry_count: int = 0
    last_action_time: float = 0
    last_status_change: float = 0
    matched_pid: int = 0
    lifecycle: list[dict] = dataclasses.field(default_factory=list)

    def emit(self, event: LifecycleEvent, detail: str = ""):
        """记录生命周期事件"""
        entry = {
            "ts": datetime.now().strftime("%H:%M:%S"),
            "event": event.value,
            "detail": detail,
            "id": str(uuid.uuid4())[:8],  # 幂等键
        }
        self.lifecycle.append(entry)
        if len(self.lifecycle) > 200:
            self.lifecycle = self.lifecycle[-100:]

    @property
    def last_event(self) -> str:
        if not self.lifecycle:
            return ""
        e = self.lifecycle[-1]
        return f"[{e['ts']}] {e['event']}: {e['detail']}"


# ═══════════════════════════════════════════════
#  Chat 操作（Steer 层）
# ═══════════════════════════════════════════════

class SteerOperator:
    """
    IDE AI Chat 面板操作

    命名灵感来自 OpenClaw 的 steer 机制：
    向 Agent 注入新指令，带速率限制和幂等保护。
    """

    # Chat 输入框特征词（覆盖主流 IDE）
    _CHAT_HINTS = [
        "ask", "message", "chat", "prompt", "type",
        "send", "input", "agent", "copilot", "cline",
        "ask anything", "type a message",
    ]
    _EXCLUDE_HINTS = [
        "search", "filter", "find", "terminal",
        "grep", "replace", "rename",
    ]

    # 速率限制追踪（借鉴 OpenClaw STEER_RATE_LIMIT_MS）
    _last_steer: dict[int, float] = {}

    @classmethod
    def find_chat_input(cls, app: Application) -> Optional[object]:
        """定位 IDE 窗口中的 AI Chat 输入框"""
        for win in app.windows():
            try:
                wt = win.window_text() or ""
                if not wt or "Program Manager" in wt:
                    continue

                candidates = []
                for d in win.descendants():
                    try:
                        ct = d.element_info.control_type or ""
                        if ct != "Edit":
                            continue
                        name = (d.element_info.name or "").lower()
                        if any(kw in name for kw in cls._EXCLUDE_HINTS):
                            continue
                        if (any(kw in name for kw in cls._CHAT_HINTS)
                                or name.strip() == ""):
                            candidates.append(d)
                    except Exception:
                        continue

                if candidates:
                    return candidates[-1]
            except Exception:
                continue
        return None

    @classmethod
    def steer(
        cls,
        app: Application,
        message: str,
        pid: int,
        cooldown: float = 10.0,
    ) -> tuple[bool, str]:
        """
        向 Agent 发送续跑指令（steer）

        Returns: (success, idempotency_key)
        """
        # 速率限制
        now = time.time()
        last = cls._last_steer.get(pid, 0)
        if now - last < cooldown:
            return False, ""

        chat_input = cls.find_chat_input(app)
        if not chat_input:
            log_event(logger, f"PID={pid}: Chat 输入框未找到",
                      event_type="steer_no_input")
            return False, ""

        idempotency_key = str(uuid.uuid4())[:8]

        try:
            chat_input.set_focus()
            time.sleep(0.1)

            try:
                chat_input.set_edit_text("")
            except Exception:
                send_keys("^a{DELETE}", pause=0.02)
            time.sleep(0.05)

            try:
                chat_input.set_edit_text(message)
            except Exception:
                chat_input.type_keys(message, with_spaces=True, pause=0.01)
            time.sleep(0.1)

            send_keys("{ENTER}", pause=0.05)

            cls._last_steer[pid] = now

            log_event(
                logger,
                f"PID={pid}: steer #{idempotency_key} ({len(message)} chars)",
                event_type="steer_sent",
                event_data={"key": idempotency_key, "preview": message[:80]},
            )
            return True, idempotency_key

        except Exception as e:
            log_event(logger, f"PID={pid}: steer 失败 - {e}",
                      event_type="steer_failed")
            return False, ""

    @staticmethod
    def read_conversation(app: Application) -> str:
        """读取 AI 对话面板最近内容"""
        texts = []
        for win in app.windows()[:3]:
            try:
                wt = win.window_text() or ""
                if not wt or "Program Manager" in wt:
                    continue
                for d in win.descendants():
                    try:
                        ct = d.element_info.control_type or ""
                        if ct not in ("Text", "Document", "Edit"):
                            continue
                        content = ""
                        try:
                            content = d.window_text() or ""
                        except Exception:
                            content = (d.element_info.name or "").strip()
                        if len(content) > 20 and content != wt:
                            texts.append(content[:500])
                    except Exception:
                        continue
            except Exception:
                continue
        return "\n".join(texts[-10:])


# ═══════════════════════════════════════════════
#  督导器核心
# ═══════════════════════════════════════════════

class AgentSupervisor:
    """
    通用 IDE Agent 全时督导器

    状态机 + 生命周期事件驱动：
    PENDING → RUNNING → CHECKING → RUNNING/ACHIEVED/FAILED
                 ↕             ↕
              STALLED      (steer)
    """

    def __init__(self, goals: list[TaskGoal]):
        self.goals = goals
        self.monitor = MultiProjectAIMonitor()
        self._prev_states: dict[int, AIStatus] = {}
        self._total_steers = 0
        self._total_events = 0

    def run(
        self,
        interval: float = 5.0,
        dry_run: bool = False,
        max_hours: float = 24.0,
    ):
        """启动督导循环"""
        start_time = time.time()
        max_seconds = max_hours * 3600

        print("=" * 60)
        print("  🤖 Agent Supervisor — IDE 全时督导")
        print(f"  {len(self.goals)} 个任务目标")
        print(f"  模式: {'🔍 只读演示' if dry_run else '⚡ 自动督导'}")
        print(f"  最长运行: {max_hours}h")
        print("=" * 60)
        for g in self.goals:
            print(f"  📌 [{g.window_match}] {g.task_name}")
            print(f"     目标: {g.goal}")
        print()

        try:
            while True:
                elapsed = time.time() - start_time
                if elapsed > max_seconds:
                    print(f"\n  ⏰ 已达最大运行时间 ({max_hours}h)")
                    break

                if all(g.status in (GoalStatus.ACHIEVED, GoalStatus.FAILED)
                       for g in self.goals):
                    achieved = sum(1 for g in self.goals
                                   if g.status == GoalStatus.ACHIEVED)
                    print(f"\n  🏁 全部任务处理完毕 "
                          f"({achieved}/{len(self.goals)} 达标)")
                    break

                states = self.monitor.scan_all()

                for goal in self.goals:
                    if goal.status in (GoalStatus.ACHIEVED, GoalStatus.FAILED):
                        continue
                    matched = self._match_window(goal, states)
                    if matched:
                        self._tick(goal, matched, dry_run)

                self._dashboard(states, elapsed)
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n  督导已停止。")

        self._report()

    # ── 窗口匹配 ──

    def _match_window(
        self, goal: TaskGoal, states: list[AIProjectState]
    ) -> Optional[AIProjectState]:
        kw = goal.window_match.lower()
        for s in states:
            if kw in s.project_name.lower() or kw in s.window_title.lower():
                goal.matched_pid = s.pid
                return s
        return None

    # ── 核心状态机（受 OpenClaw lifecycle 启发）──

    def _tick(self, goal: TaskGoal, state: AIProjectState, dry_run: bool):
        prev = self._prev_states.get(state.pid)
        curr = state.ai_status
        self._prev_states[state.pid] = curr
        now = time.time()

        # ── 首次检测到运行 → SPAWNED ──
        if prev is None and curr == AIStatus.RUNNING:
            goal.status = GoalStatus.RUNNING
            goal.last_status_change = now
            goal.emit(LifecycleEvent.SPAWNED, f"Agent 首次探测, PID={state.pid}")
            self._total_events += 1
            return

        # ── Running → Idle: Agent 完成一轮 (COMPLETED) ──
        if prev == AIStatus.RUNNING and curr == AIStatus.IDLE:
            goal.last_status_change = now
            goal.status = GoalStatus.CHECKING
            goal.emit(LifecycleEvent.COMPLETED, "Agent 完成一轮")
            self._total_events += 1

            try:
                app = Application(backend="uia").connect(process=state.pid)
                conv = SteerOperator.read_conversation(app)
                achieved = self._check_goal(goal, conv)

                if achieved:
                    goal.status = GoalStatus.ACHIEVED
                    goal.emit(LifecycleEvent.GOAL_ACHIEVED, "🏆 目标达成!")
                    self._total_events += 1
                    return

                # 未达标 → steer 续发
                self._steer(goal, app, state.pid, dry_run)
            except Exception as e:
                goal.emit(LifecycleEvent.ERROR, f"检查异常: {str(e)[:50]}")
                self._total_events += 1
            return

        # ── Idle → Error || Error 持续: 报错重试 ──
        if curr == AIStatus.ERROR:
            if now - goal.last_action_time > goal.cooldown_sec:
                goal.emit(LifecycleEvent.ERROR, "Agent 报错")
                self._total_events += 1
                try:
                    app = Application(backend="uia").connect(process=state.pid)
                    self._steer(goal, app, state.pid, dry_run)
                except Exception as e:
                    goal.emit(LifecycleEvent.ERROR, f"重试异常: {str(e)[:40]}")
            return

        # ── Running 持续 ──
        if curr == AIStatus.RUNNING:
            if goal.status != GoalStatus.RUNNING:
                goal.status = GoalStatus.RUNNING
                goal.last_status_change = now
            return

        # ── Idle 持续 → stall 检测 ──
        if curr == AIStatus.IDLE and prev == AIStatus.IDLE:
            if (goal.status in (GoalStatus.RUNNING, GoalStatus.CHECKING)
                    and now - goal.last_status_change > goal.stall_timeout):
                goal.status = GoalStatus.STALLED
                goal.emit(
                    LifecycleEvent.STALLED,
                    f"Agent 静默 {goal.stall_timeout:.0f}s"
                )
                self._total_events += 1
                try:
                    app = Application(backend="uia").connect(process=state.pid)
                    self._steer(goal, app, state.pid, dry_run)
                except Exception:
                    pass

    # ── 目标检查 ──

    def _check_goal(self, goal: TaskGoal, conversation: str) -> bool:
        conv_lower = conversation.lower()

        for kw in goal.failure_keywords:
            if kw.lower() in conv_lower:
                goal.emit(LifecycleEvent.ERROR, f"检测到问题信号: '{kw}'")
                return False

        for kw in goal.success_keywords:
            if kw.lower() in conv_lower:
                goal.emit(LifecycleEvent.COMPLETED, f"✅ 成功信号: '{kw}'")
                return True

        goal.emit(LifecycleEvent.COMPLETED, "未检测到明确完成信号")
        return False

    # ── Steer 续发（借鉴 OpenClaw steerControlledSubagentRun）──

    def _steer(
        self, goal: TaskGoal, app: Application, pid: int, dry_run: bool
    ):
        # 重试上限检查
        if goal.retry_count >= goal.max_retries:
            goal.status = GoalStatus.FAILED
            goal.emit(
                LifecycleEvent.GOAL_FAILED,
                f"已达重试上限 ({goal.max_retries})"
            )
            self._total_events += 1
            return

        if dry_run:
            goal.retry_count += 1
            goal.status = GoalStatus.RUNNING
            goal.emit(
                LifecycleEvent.STEERED,
                f"[DRY] 将发送: {goal.retry_command[:60]}..."
            )
            self._total_steers += 1
            self._total_events += 1
            return

        # 实际 steer
        ok, key = SteerOperator.steer(
            app, goal.retry_command, pid, goal.cooldown_sec
        )
        if ok:
            goal.retry_count += 1
            goal.last_action_time = time.time()
            goal.status = GoalStatus.RUNNING
            goal.emit(
                LifecycleEvent.STEERED,
                f"📤 指令已发送 #{goal.retry_count} key={key}"
            )
            self._total_steers += 1
            self._total_events += 1
        else:
            goal.emit(LifecycleEvent.ERROR, "steer 失败（速率限制或输入框未找到）")

    # ── 仪表盘 ──

    def _dashboard(self, states: list[AIProjectState], elapsed: float):
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)

        emoji_map = {
            GoalStatus.PENDING:  "⏸", GoalStatus.RUNNING: "🔄",
            GoalStatus.CHECKING: "🔍", GoalStatus.ACHIEVED: "🏆",
            GoalStatus.STALLED:  "⚠", GoalStatus.FAILED:  "❌",
        }

        lines = [
            "\033[2J\033[H",
            "=" * 62,
            f"  🤖 Agent Supervisor  │  {h}h {m}m  │  "
            f"steers:{self._total_steers}  events:{self._total_events}",
            "=" * 62, "",
        ]

        for g in self.goals:
            e = emoji_map.get(g.status, "❓")
            retry = f" #{g.retry_count}/{g.max_retries}" if g.retry_count else ""
            lines.append(
                f"  {e} {g.task_name[:30]:<30} {g.status.value}{retry}"
            )
            lines.append(f"     📌 {g.goal[:50]}")
            if g.last_event:
                lines.append(f"     └ {g.last_event}")
            lines.append("")

        lines.append("─" * 62)
        for s in states:
            model = f" [{s.ai_model}]" if s.ai_model else ""
            lines.append(
                f"  {s.status_emoji} {s.project_name[:20]:<20} "
                f"{s.ai_status.value:<8}{model}"
            )
        lines.append("=" * 62)

        print("\n".join(lines), flush=True)

    # ── 报告 ──

    def _report(self):
        print("\n" + "=" * 62)
        print("  📊 督导报告")
        print("=" * 62)
        achieved_count = 0
        for g in self.goals:
            is_ok = g.status == GoalStatus.ACHIEVED
            if is_ok:
                achieved_count += 1
            e = "🏆" if is_ok else "❌"
            print(f"\n  {e} {g.task_name}")
            print(f"     状态: {g.status.value}  |  Steers: {g.retry_count}")
            # 最近 3 条生命周期事件
            for ev in g.lifecycle[-3:]:
                print(f"     [{ev['ts']}] {ev['event']}: {ev['detail']}")
        print(f"\n  总计: {achieved_count}/{len(self.goals)} 达标, "
              f"共 {self._total_steers} 次 steer, "
              f"{self._total_events} 个事件")
        print()

        # 导出 JSON 报告
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total": len(self.goals),
                    "achieved": achieved_count,
                    "total_steers": self._total_steers,
                    "total_events": self._total_events,
                },
                "goals": [
                    {
                        "task_name": g.task_name,
                        "status": g.status.value,
                        "retry_count": g.retry_count,
                        "lifecycle": g.lifecycle[-10:],
                    }
                    for g in self.goals
                ],
            }
            report_path = os.path.join("logs", "supervisor_report.json")
            os.makedirs("logs", exist_ok=True)
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"  📄 详细报告已保存: {report_path}")
        except Exception:
            pass


# ═══════════════════════════════════════════════
#  配置文件
# ═══════════════════════════════════════════════

def load_goals(path: str) -> list[TaskGoal]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    goals = []
    for item in data.get("goals", []):
        goals.append(TaskGoal(
            window_match=item["window_match"],
            task_name=item["task_name"],
            goal=item["goal"],
            success_keywords=item.get("success_keywords", []),
            failure_keywords=item.get("failure_keywords", ["Error", "failed"]),
            retry_command=item.get("retry_command",
                "继续寻找最佳方案并执行，分析之前的结果，优化策略，直到达到目标。"
            ),
            max_retries=item.get("max_retries", 30),
            cooldown_sec=item.get("cooldown_sec", 10.0),
            stall_timeout=item.get("stall_timeout", 600),
        ))
    return goals


def save_example_config(path: str):
    example = {
        "_doc": (
            "Agent Supervisor 通用任务配置。"
            "每个 goal 对应一个 IDE 窗口中需要督导的任务。"
            "window_match 匹配窗口标题关键词。"
            "Agent 完成时检查 success_keywords 判断目标是否达成，"
            "未达标则自动发送 retry_command 续发指令（steer）。"
        ),
        "goals": [
            {
                "window_match": "DOW",
                "task_name": "安全攻防基准测试",
                "goal": "全部攻击向量 ASR > 85%",
                "success_keywords": ["ASR: 0.9", "ASR: 0.8", "passed", "达标"],
                "failure_keywords": ["Error", "failed", "rate limit"],
                "retry_command": (
                    "分析上一轮实验结果中的失败用例，"
                    "寻找更优方案，调整参数后重新执行，直到超过目标。"
                ),
                "max_retries": 30,
                "cooldown_sec": 15,
                "stall_timeout": 600
            },
            {
                "window_match": "cpop",
                "task_name": "功能开发与测试",
                "goal": "pnpm test 全部通过, pnpm check 无错误",
                "success_keywords": [
                    "all tests passed", "0 errors", "通过",
                    "pnpm test", "done"
                ],
                "failure_keywords": ["FAILED", "error", "TypeError"],
                "retry_command": (
                    "检查最新测试与 lint 输出，修复全部失败项，"
                    "然后重新运行 pnpm test 和 pnpm check 验证。"
                ),
                "max_retries": 20
            },
            {
                "window_match": "Measurement",
                "task_name": "安全扫描数据收集",
                "goal": "1835 仓库扫描完成",
                "success_keywords": ["scan complete", "1835", "完成"],
                "failure_keywords": ["Error", "timeout"],
                "retry_command": "继续扫描剩余仓库，修复解析错误，确保全部完成。"
            }
        ]
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(example, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 示例配置已保存: {path}")
    print(f"  编辑后用 --config {path} 启动")


# ═══════════════════════════════════════════════
#  start.bat 集成入口
# ═══════════════════════════════════════════════

def cli_entry(args: list[str]):
    """从 start.bat supervisor 模式调用"""
    import argparse
    parser = argparse.ArgumentParser(
        description="Agent Supervisor — 通用 IDE Agent 全时督导"
    )
    parser.add_argument("--config", type=str, default="",
                        help="任务配置文件 (JSON)")
    parser.add_argument("--demo", action="store_true",
                        help="只读演示模式")
    parser.add_argument("--interval", type=float, default=5.0,
                        help="轮询间隔（秒）")
    parser.add_argument("--max-hours", type=float, default=24.0,
                        help="最大运行小时数")
    parser.add_argument("--gen-config", type=str, default="",
                        help="生成示例配置")
    parsed = parser.parse_args(args)

    if parsed.gen_config:
        save_example_config(parsed.gen_config)
        return

    if parsed.config:
        if not os.path.exists(parsed.config):
            print(f"  ❌ 配置文件不存在: {parsed.config}")
            print(f"  生成模板: python agent_supervisor.py --gen-config goals.json")
            return
        goals = load_goals(parsed.config)
    else:
        print("  ℹ 未指定配置，使用内置演示目标")
        print("  生成配置: python agent_supervisor.py --gen-config goals.json\n")
        goals = [
            TaskGoal(
                window_match="DOW",
                task_name="演示任务",
                goal="Agent 完成当前工作",
                success_keywords=["完成", "done", "passed"],
                failure_keywords=["Error", "failed"],
                retry_command="继续寻找最佳方案并执行，直到达到目标。",
            ),
        ]

    AgentSupervisor(goals).run(
        interval=parsed.interval,
        dry_run=parsed.demo,
        max_hours=parsed.max_hours,
    )


if __name__ == "__main__":
    cli_entry(sys.argv[1:])
