# -*- coding: utf-8 -*-
"""
agent_bridge.py - AI Agent 调用接口

将 AI Agent 的自然语言意图转换为 UIA 操作:
- 提供结构化的 Action 指令格式
- 解析 Agent 发出的操作意图
- 执行操作并返回结构化结果
- 支持批量操作和操作链
"""

from __future__ import annotations

import json
import dataclasses
from typing import Any, Optional
from enum import Enum

from uia_controller import UIAController
from element_finder import ElementInfo


class ActionType(str, Enum):
    """Agent 可发出的操作类型"""
    LIST_PROCESSES = "list_processes"
    CONNECT = "connect"
    FIND_INPUTS = "find_inputs"
    FIND_BUTTONS = "find_buttons"
    FIND_TEXTS = "find_texts"
    FIND_BY_NAME = "find_by_name"
    FIND_BY_ID = "find_by_id"
    GET_TREE = "get_tree"
    GLOBAL_FIND_INPUTS = "global_find_inputs"
    TYPE_TEXT = "type_text"
    CLICK = "click"
    READ_VALUE = "read_value"
    FOCUS = "focus"
    FIND_AND_TYPE = "find_and_type"
    FIND_AND_CLICK = "find_and_click"
    WAIT_FOR_ELEMENT = "wait_for_element"
    SNAPSHOT = "snapshot"


@dataclasses.dataclass
class ActionResult:
    """操作执行结果"""
    success: bool
    action: str
    data: Any = None
    error: Optional[str] = None
    element_count: int = 0

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "action": self.action,
            "data": self.data,
            "error": self.error,
            "element_count": self.element_count,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, default=str)


def _serialize_element(e: ElementInfo) -> dict:
    """将 ElementInfo 序列化为 dict（去除内部引用）"""
    return {
        "control_type": e.control_type,
        "name": e.name,
        "automation_id": e.automation_id,
        "value": e.value[:100] if e.value else "",
        "rect": list(e.rect),
        "is_enabled": e.is_enabled,
        "is_writable": e.is_writable,
        "process_name": e.process_name,
        "pid": e.pid,
        "window_title": e.window_title[:50],
    }


class AgentBridge:
    """
    AI Agent 与 UIA 之间的桥接层

    使用方式 1 - 结构化调用:
        bridge = AgentBridge()
        result = bridge.execute(ActionType.LIST_PROCESSES)
        result = bridge.execute(ActionType.CONNECT, target="msedge")
        result = bridge.execute(ActionType.FIND_INPUTS)
        result = bridge.execute(ActionType.TYPE_TEXT, field_name="Address", text="https://...")

    使用方式 2 - JSON 指令:
        bridge = AgentBridge()
        result = bridge.execute_json('{\"action\": \"connect\", \"target\": \"msedge\"}')
        result = bridge.execute_json('{\"action\": \"find_and_type\", \"field_name\": \"Address\", \"text\": \"...\"}')

    使用方式 3 - 快照（给 Agent 当前屏幕的结构化描述）:
        bridge = AgentBridge()
        snapshot = bridge.take_snapshot()
    """

    def __init__(self, backend: str = "uia"):
        self._controller = UIAController(backend=backend)
        # 缓存最近搜索到的元素，供后续操作引用
        self._element_cache: list[ElementInfo] = []

    def execute(self, action: ActionType | str, **kwargs) -> ActionResult:
        """
        执行单个操作

        Args:
            action: 操作类型
            **kwargs: 操作参数
        """
        if isinstance(action, str):
            try:
                action = ActionType(action)
            except ValueError:
                return ActionResult(
                    success=False, action=action, error=f"Unknown action: {action}"
                )

        try:
            return self._dispatch(action, **kwargs)
        except Exception as e:
            return ActionResult(success=False, action=action.value, error=str(e))

    def execute_json(self, json_str: str) -> ActionResult:
        """执行 JSON 格式的指令"""
        try:
            cmd = json.loads(json_str)
            action = cmd.pop("action")
            return self.execute(action, **cmd)
        except json.JSONDecodeError as e:
            return ActionResult(success=False, action="parse", error=f"Invalid JSON: {e}")
        except Exception as e:
            return ActionResult(success=False, action="execute", error=str(e))

    def execute_batch(self, actions: list[dict]) -> list[ActionResult]:
        """批量执行多个操作"""
        results = []
        for cmd in actions:
            action = cmd.pop("action", "")
            result = self.execute(action, **cmd)
            results.append(result)
            # 如果某步失败，后续依赖的步骤也会失败
            if not result.success and cmd.get("stop_on_error", False):
                break
        return results

    def _dispatch(self, action: ActionType, **kwargs) -> ActionResult:
        """分发操作到对应的处理方法"""
        ctrl = self._controller

        if action == ActionType.LIST_PROCESSES:
            procs = ctrl.list_processes()
            data = [
                {
                    "pid": p.pid,
                    "name": p.name,
                    "exe_path": p.exe_path,
                    "windows": p.window_titles[:5],
                    "memory_mb": round(p.memory_mb, 1),
                }
                for p in procs
            ]
            return ActionResult(
                success=True, action=action.value, data=data, element_count=len(data)
            )

        elif action == ActionType.CONNECT:
            target = kwargs.get("target")
            if target is None:
                return ActionResult(
                    success=False, action=action.value,
                    error="Missing 'target' (PID or process name)",
                )
            proc = ctrl.connect_to(int(target) if str(target).isdigit() else target)
            return ActionResult(
                success=True, action=action.value,
                data={"pid": proc.pid, "name": proc.name, "windows": proc.window_titles[:5]},
            )

        elif action == ActionType.FIND_INPUTS:
            elements = ctrl.find_inputs(max_results=kwargs.get("max", 50))
            self._element_cache = elements
            return ActionResult(
                success=True, action=action.value,
                data=[_serialize_element(e) for e in elements],
                element_count=len(elements),
            )

        elif action == ActionType.FIND_BUTTONS:
            elements = ctrl.find_buttons(max_results=kwargs.get("max", 50))
            self._element_cache = elements
            return ActionResult(
                success=True, action=action.value,
                data=[_serialize_element(e) for e in elements],
                element_count=len(elements),
            )

        elif action == ActionType.FIND_TEXTS:
            elements = ctrl.find_texts(max_results=kwargs.get("max", 50))
            self._element_cache = elements
            return ActionResult(
                success=True, action=action.value,
                data=[_serialize_element(e) for e in elements],
                element_count=len(elements),
            )

        elif action == ActionType.FIND_BY_NAME:
            name = kwargs.get("name", "")
            elements = ctrl.find_by_name(name, exact=kwargs.get("exact", False))
            self._element_cache = elements
            return ActionResult(
                success=True, action=action.value,
                data=[_serialize_element(e) for e in elements],
                element_count=len(elements),
            )

        elif action == ActionType.FIND_BY_ID:
            aid = kwargs.get("automation_id", "")
            element = ctrl.find_by_id(aid)
            if element:
                self._element_cache = [element]
                return ActionResult(
                    success=True, action=action.value,
                    data=_serialize_element(element), element_count=1,
                )
            return ActionResult(
                success=False, action=action.value,
                error=f"Element not found: {aid}",
            )

        elif action == ActionType.GET_TREE:
            tree = ctrl.get_tree()
            return ActionResult(success=True, action=action.value, data=tree)

        elif action == ActionType.GLOBAL_FIND_INPUTS:
            elements = ctrl.global_find_inputs(
                max_per_window=kwargs.get("max_per_window", 10)
            )
            self._element_cache = elements
            return ActionResult(
                success=True, action=action.value,
                data=[_serialize_element(e) for e in elements],
                element_count=len(elements),
            )

        elif action == ActionType.TYPE_TEXT:
            # 支持通过 index 引用缓存的元素，或通过 field_name 查找
            element = self._resolve_element(kwargs)
            if not element:
                return ActionResult(
                    success=False, action=action.value,
                    error="Target element not found",
                )
            text = kwargs.get("text", "")
            ok = ctrl.type_text(element, text, clear_first=kwargs.get("clear", True))
            return ActionResult(
                success=ok, action=action.value,
                data={"typed": text, "target": element.name},
            )

        elif action == ActionType.CLICK:
            element = self._resolve_element(kwargs)
            if not element:
                return ActionResult(
                    success=False, action=action.value,
                    error="Target element not found",
                )
            ok = ctrl.click(element)
            return ActionResult(
                success=ok, action=action.value,
                data={"clicked": element.name},
            )

        elif action == ActionType.READ_VALUE:
            element = self._resolve_element(kwargs)
            if not element:
                return ActionResult(
                    success=False, action=action.value,
                    error="Target element not found",
                )
            value = ctrl.read_value(element)
            return ActionResult(
                success=True, action=action.value,
                data={"name": element.name, "value": value},
            )

        elif action == ActionType.FOCUS:
            element = self._resolve_element(kwargs)
            if not element:
                return ActionResult(
                    success=False, action=action.value,
                    error="Target element not found",
                )
            ok = ctrl.focus(element)
            return ActionResult(success=ok, action=action.value)

        elif action == ActionType.FIND_AND_TYPE:
            field = kwargs.get("field_name", "")
            text = kwargs.get("text", "")
            ok = ctrl.find_and_type(field, text)
            return ActionResult(
                success=ok, action=action.value,
                data={"field": field, "text": text},
            )

        elif action == ActionType.FIND_AND_CLICK:
            button = kwargs.get("button_name", "")
            ok = ctrl.find_and_click(button)
            return ActionResult(
                success=ok, action=action.value,
                data={"button": button},
            )

        elif action == ActionType.WAIT_FOR_ELEMENT:
            name = kwargs.get("name", "")
            timeout = kwargs.get("timeout", 10.0)
            element = ctrl.wait_for_element(name, timeout=timeout)
            if element:
                self._element_cache = [element]
                return ActionResult(
                    success=True, action=action.value,
                    data=_serialize_element(element), element_count=1,
                )
            return ActionResult(
                success=False, action=action.value,
                error=f"Element '{name}' did not appear within {timeout}s",
            )

        elif action == ActionType.SNAPSHOT:
            level = kwargs.get("level", "L1")
            return self.take_snapshot(level=level)

        return ActionResult(
            success=False, action=action.value, error="Unhandled action"
        )

    def _resolve_element(self, kwargs: dict) -> Optional[ElementInfo]:
        """解析元素引用（通过 index 或 field_name/button_name/name）"""
        idx = kwargs.get("index")
        if idx is not None and 0 <= idx < len(self._element_cache):
            return self._element_cache[idx]

        name = kwargs.get("field_name") or kwargs.get("button_name") or kwargs.get("name")
        if name:
            elements = self._controller.find_by_name(name)
            if elements:
                return elements[0]

        return None

    def take_snapshot(self, level: str = "L1") -> ActionResult:
        """
        分层快照算法

        L0 — 进程列表（仅 PID/Name/Title），~100ms
        L1 — 目标进程详情（连接后获取控件摘要），~800ms
        L2 — 全量扫描（遍历所有进程控件树），~27s（仅调试用）

        默认 L1：为 LLM 提供足够上下文而不浪费时间在无关进程上。
        """
        import time
        t0 = time.perf_counter()
        ctrl = self._controller
        procs = ctrl.list_processes()

        snapshot = {
            "level": level,
            "total_processes": len(procs),
            "processes": [],
        }

        if level == "L0":
            # ─── L0: 仅进程元数据，零 UIA 操作 ───
            for p in procs[:20]:
                snapshot["processes"].append({
                    "pid": p.pid,
                    "name": p.name,
                    "windows": p.window_titles[:2],
                    "memory_mb": round(p.memory_mb, 1),
                })

        elif level == "L1":
            # ─── L1: 进程列表 + 目标进程深度扫描 ───
            target_name = ""
            if ctrl._current_process:
                target_name = ctrl._current_process.name.lower()

            for p in procs[:20]:
                proc_info = {
                    "pid": p.pid,
                    "name": p.name,
                    "windows": p.window_titles[:2],
                    "memory_mb": round(p.memory_mb, 1),
                }

                is_target = (
                    target_name and target_name in p.name.lower()
                ) or (ctrl._current_process and p.pid == ctrl._current_process.pid)

                if is_target:
                    # 对目标进程做多窗口控件树遍历
                    try:
                        app = ctrl._process_tree.connect(p.pid)

                        # 枚举全部窗口（而非仅 top_window）
                        all_wins = []
                        try:
                            all_wins = app.windows()
                        except Exception:
                            try:
                                all_wins = [app.top_window()]
                            except Exception:
                                pass

                        total_elems = 0
                        type_counts: dict[str, int] = {}
                        key_elements = []
                        window_details = []

                        for w in all_wins:
                            try:
                                win_title = w.window_text() or ""
                                if not win_title or "Program Manager" in win_title:
                                    continue

                                descendants = w.descendants()
                                total_elems += len(descendants)

                                for d in descendants:
                                    try:
                                        ct = d.element_info.control_type or "Unknown"
                                        type_counts[ct] = type_counts.get(ct, 0) + 1
                                    except Exception:
                                        pass

                                # 提取关键交互元素
                                win_keys = []
                                for d in descendants:
                                    try:
                                        ct = d.element_info.control_type or ""
                                        if ct in ("Button", "Edit", "MenuItem", "TabItem"):
                                            name = d.element_info.name or ""
                                            if name and len(name) > 1:
                                                win_keys.append({
                                                    "type": ct,
                                                    "name": name[:50],
                                                })
                                                if len(win_keys) >= 15:
                                                    break
                                    except Exception:
                                        continue

                                window_details.append({
                                    "title": win_title[:80],
                                    "element_count": len(descendants),
                                    "key_elements": win_keys,
                                })
                                key_elements.extend(win_keys)
                            except Exception:
                                continue

                        proc_info["elements_summary"] = type_counts
                        proc_info["total_elements"] = total_elems
                        proc_info["window_count"] = len(window_details)
                        proc_info["window_details"] = window_details
                        proc_info["key_elements"] = key_elements[:30]
                    except Exception:
                        proc_info["total_elements"] = 0

                snapshot["processes"].append(proc_info)

        else:
            # ─── L2: 全量扫描（旧行为，仅调试用）───
            for p in procs[:15]:
                proc_info = {
                    "pid": p.pid,
                    "name": p.name,
                    "windows": p.window_titles[:3],
                    "memory_mb": round(p.memory_mb, 1),
                    "elements_summary": {},
                }

                try:
                    app = ctrl._process_tree.connect(p.pid)
                    win = app.top_window()
                    descendants = win.descendants()

                    type_counts: dict[str, int] = {}
                    for d in descendants:
                        try:
                            ct = d.element_info.control_type or "Unknown"
                            type_counts[ct] = type_counts.get(ct, 0) + 1
                        except Exception:
                            pass

                    proc_info["elements_summary"] = type_counts
                    proc_info["total_elements"] = len(descendants)
                except Exception:
                    proc_info["total_elements"] = 0

                snapshot["processes"].append(proc_info)

        elapsed_ms = (time.perf_counter() - t0) * 1000
        snapshot["elapsed_ms"] = round(elapsed_ms, 1)

        return ActionResult(
            success=True, action="snapshot", data=snapshot,
            element_count=sum(p.get("total_elements", 0) for p in snapshot["processes"]),
        )

