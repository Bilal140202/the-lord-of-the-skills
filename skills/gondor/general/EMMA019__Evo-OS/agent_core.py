import os
import sys
import time
import json
import logging
import subprocess
import atexit
import uuid
import shutil
import contextvars
import re
from typing import Dict, List, Optional

# 設定とサービス群のインポート
from src.config import config
from src.services.budget_service import BudgetGuard
from src.services.workspace_manager import WorkspaceManager
from src.services.architect_service import ArchitectService
from src.services.kit_manager import KitManager
from src.services.kit_gen_service import KitGenService
from src.services.search_service import SearchService
from src.services.qa_service import QualityAssuranceService
from src.services.verifier_service import VerifierService
from src.services.healer_service import HealerService
from src.services.structure_service import StructureService
from src.services.data_recorder import DataRecorder

# ランタイムクラスの定義（簡略化のためここに配置。別ファイル分離を推奨）
class BaseRuntime:
    def start(self): pass
    def stop(self): pass
    def install_requirements(self): pass
    def test_run(self, entry_point): return True, "No runtime"
class DockerRuntime(BaseRuntime):
    def __init__(self):
        self.container = f"{config.CONTAINER_PREFIX}-{uuid.uuid4().hex[:8]}"
        self.workdir = os.path.abspath(config.OUTPUT_DIR)
        self._started = False
        self._available = bool(shutil.which("docker"))
        if self._available:
            try: subprocess.run(["docker", "info"], capture_output=True, check=True)
            except: self._available = False
    def start(self):
        if not self._available or self._started: return
        self._cleanup()
        try:
            env_args = ["-e", f"GOOGLE_API_KEY={config.LLM_API_KEY}"]
            subprocess.run(
                ["docker", "run", "-d", "--rm", "--name", self.container, "--network", "host", "-v", f"{self.workdir}:/workspace"] + env_args + [config.DOCKER_IMAGE, "sleep", "infinity"], 
                check=True, capture_output=True
            )
            self._started = True; atexit.register(self.stop)
            logger.info("🐳 Docker Runtime Started.")
        except Exception as e: 
            logger.warning(f"⚠️ Docker failed: {e}. Falling back to Local.")
            self._available = False
    def stop(self):
        if self._started: 
            subprocess.run(["docker", "rm", "-f", self.container], capture_output=True)
            self._started = False
            logger.info("🐳 Docker Runtime Stopped.")
    def _cleanup(self): self.stop()
    def install_requirements(self):
        if not self._started: return
        if os.path.exists(os.path.join(self.workdir, "requirements.txt")):
            logger.info("📦 Docker: Installing requirements...")
            subprocess.run(["docker", "exec", "-w", "/workspace", self.container, "pip", "install", "-r", "requirements.txt"], capture_output=True, timeout=120)
    def test_run(self, entry_point="app.py"):
        if not self._started: return False, "Docker not started"
        try:
            cmd = ["docker", "exec", "-w", "/workspace", self.container, "python", entry_point]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try: outs, errs = proc.communicate(timeout=10) 
            except subprocess.TimeoutExpired: proc.kill(); return True, "Running"
            if proc.returncode != 0: return False, f"Error:\n{errs}"
            return True, "Success"
        except Exception as e: return False, str(e)
class LocalRuntime(BaseRuntime):
    def __init__(self):
        self.workdir = os.path.abspath(config.OUTPUT_DIR)
        self.venv_dir = os.path.join(self.workdir, ".venv")
        is_win = os.name == 'nt'
        self.py_exe = os.path.join(self.venv_dir, "Scripts" if is_win else "bin", "python.exe" if is_win else "python")
    def start(self):
        if not os.path.exists(self.py_exe):
            logger.info("🐍 Creating Local venv...")
            subprocess.run([sys.executable, "-m", "venv", self.venv_dir], check=True)
        logger.info("🐍 Local Runtime Ready.")
    def install_requirements(self):
        req = os.path.join(self.workdir, "requirements.txt")
        if os.path.exists(req):
            logger.info("📦 Local: Installing requirements...")
            try: subprocess.run([self.py_exe, "-m", "pip", "install", "-r", req], cwd=self.workdir, capture_output=True, check=True, timeout=120)
            except: pass
    def test_run(self, entry_point="app.py"):
        if not os.path.exists(os.path.join(self.workdir, entry_point)): return False, "File not found"
        logger.info(f"🧪 Local Testing: {entry_point}...")
        try:
            env = os.environ.copy()
            env["GOOGLE_API_KEY"] = config.LLM_API_KEY
            proc = subprocess.Popen([self.py_exe, entry_point], cwd=self.workdir, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try: outs, errs = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired: proc.kill(); return True, "Running"
            if proc.returncode != 0: return False, f"Error:\n{errs}\n{outs}"
            return True, "Success"
        except Exception as e: return False, str(e)


# --- ロギング設定 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("EvoCore")

# --- ヘルパー: パスの安全性確保 ---
def safe_path_join(base, *paths):
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(os.path.abspath(base)): raise ValueError("Path traversal attempt")
    return final_path

# --- AIクライアント設定 ---
try:
    import google.generativeai as genai
    if config.LLM_API_KEY: genai.configure(api_key=config.LLM_API_KEY)
except: pass

class ResilientClient:
    """LLM呼び出しクライアント: configのMAX_RETRIESに依存"""
    def __init__(self, model, budget_guard):
        self.model = genai.GenerativeModel(model)
        self.budget = budget_guard
        self.name = model

    def generate(self, prompt, sys_prompt="") -> str:
        full_prompt = f"{sys_prompt}\n\n{prompt}"
        
        # configのMAX_RETRIESを使用 (現在は1)
        for i in range(config.MAX_RETRIES):
            try:
                res = self.model.generate_content(full_prompt)
                text = res.text.strip()
                self.budget.check_and_record(self.name, len(full_prompt), len(text))
                return text
            except Exception as e:
                if "Budget" in str(e): raise e
                logger.warning(f"⚠️ GenAI Error ({i+1}/{config.MAX_RETRIES}): {e}")
                time.sleep(1)
        raise RuntimeError("LLM Error: Failed after all retries.")


class Orchestrator:
    """
    エージェントの司令塔（God Objectの分離完了）。
    各専門サービスを呼び出すことに徹する。
    """
    def __init__(self):
        self.logs = []
        self.budget = BudgetGuard(config.MAX_BUDGET_PER_RUN)
        
        # 1. Workspace & Git (雑務係)
        self.ws = WorkspaceManager()
        
        # 2. AI Clients (全モデルをStandard Flashに統一済み)
        client_fast = ResilientClient(config.LLM_MODEL_FAST, self.budget)
        client_smart = ResilientClient(config.LLM_MODEL_SMART, self.budget)
        client_healer = ResilientClient(config.LLM_MODEL_HEALER, self.budget)
        
        # 3. Services (依存関係の注入)
        self.kit_mgr = KitManager(client_fast)
        # ArchitectはKitManagerに依存する
        self.architect = ArchitectService(client_smart, self.kit_mgr)
        
        self.verifier = VerifierService(None) # Runtimeは後で注入
        self.healer = HealerService(client_fast, client_healer)
        self.qa = QualityAssuranceService(client_smart)
        self.structure = StructureService()
        self.search = SearchService(client_fast)
        self.kit_gen = KitGenService(client_smart)
        self.recorder = DataRecorder()

        # 4. Runtime
        self.docker = DockerRuntime()
        self.runtime = self.docker if self.docker._available else LocalRuntime()
        self.runtime.start()
        self.verifier.runtime = self.runtime # VerifierにRuntimeを注入

        # 実行中のKit情報を保持
        self.current_kit = None 

    def log(self, msg):
        logger.info(msg)
        self.logs.append(msg)

    def cleanup(self):
        self.runtime.stop()

    def run(self, prompt: str) -> Dict:
        """メイン実行フロー: 直列的で読みやすい構造"""
        self.log(f"🚀 Evo Started: {prompt[:30]}...")
        
        try:
            # A. 特殊モード判定
            if any(k in prompt for k in ["キットを作って", "Kitを作って", "Create Kit"]):
                return self._mode_kit_gen(prompt)
            if any(k in prompt.lower() for k in ["調べて", "search", "research"]):
                return self._mode_research(prompt)

            # B. 準備フェーズ: 計画作成とキット選択を一度に行う
            plan, kit = self.architect.create_plan(prompt)
            
            self.current_kit = kit
            if kit: self.log(f"🧩 Kit Confirmed: {kit['name']}")
            
            # C. 実装フェーズ (Phase Execution)
            for step in plan:
                self.log(f"🏗️ Phase {step['phase']}: {step['description']}")
                self._execute_phase(step, prompt, kit)
                self.ws.commit(f"Phase {step['phase']} Done")

            # D. 検証フェーズ (Runtime Check)
            self._runtime_check(kit)

            # E. 監査フェーズ (QA)
            self._final_audit()

            # F. 保存
            self.recorder.save_success(prompt, kit['name'] if kit else None, self.ws.project_files)
            
            return {
                "success": True, 
                "files": self.ws.project_files, 
                "logs": self.logs,
                "kit_used": kit['name'] if kit else None
            }

        except Exception as e:
            self.log(f"💥 Fatal Error: {e}")
            return {"success": False, "error": str(e), "logs": self.logs}
        finally:
            self.cleanup()

    # --- Sub Routines (ロジックを分離) ---

    def _execute_phase(self, phase, original_prompt, kit):
        """コード生成と静的ヒーリング（1回）"""
        target_files = phase.get('files', [])
        if not target_files: return
        
        # 構造解析
        struct_map = self.structure.analyze_project(self.ws.project_files)
        
        for target_file in target_files: # ★ここが実行のトリガーになる
            self.log(f"📝 Coding: {target_file}")
            
            # 1. 生成 (Generation)
            kit_rules = ""
            if kit: kit_rules += f"\nKit Rules: {kit.get('name')}"

            sys_prompt = f"""
            Role: Expert Developer. Task: Write code for '{target_file}'.
            Map:\n{struct_map}
            {kit_rules}
            Important: Implement FULL code. Output ONLY the code.
            """
            
            # ★ 修正済み: LLMから raw_response を取得
            raw_response = self.architect.client.generate(f"Goal: {original_prompt}\nFile: {target_file}", sys_prompt)
            
            # 2. 保存 (Save)
            # raw_response を parse_and_save_files に渡す
            new_files = self.ws.parse_and_save_files(raw_response, default_filename=target_file)
            
            # 3. 静的修復 (Static Heal) - 1回勝負
            for fname in new_files.keys():
                self._static_heal(fname, kit)

    def _static_heal(self, filename, kit):
        """静的エラー修復の1回勝負ロジック"""
        # config.MAX_RETRIES (1回) だけ回る
        for _ in range(config.MAX_RETRIES):
            # ワークスペースから最新のファイル内容を取得
            content = self.ws.project_files.get(filename, "")
            
            res = self.verifier.verify(content, filename, self.ws.project_files)
            if res['valid']: break
            
            self.log(f"🩹 Static Healing {filename}: {res['errors'][0][:50]}...")
            
            success, fixed, strategy = self.healer.heal(filename, content, res['errors'], self.ws.project_files, kit)
            
            if success and strategy not in ["Loop_Ignored", "Skipped"]:
                self.ws.save_file(filename, fixed)
            else:
                self.log(f"⚠️ Static fix skipped for {filename} ({strategy}). Proceeding.")
                break 

    def _runtime_check(self, kit):
        """ランタイムチェックとヒーリング（1回勝負）"""
        entry = next((f for f in ["app.py", "main.py"] if f in self.ws.project_files), None)
        if not entry: return

        self.log(f"🧪 Runtime Test: {entry}")
        self.runtime.install_requirements()
        
        # 1回勝負
        for _ in range(config.MAX_RETRIES):
            ok, log = self.runtime.test_run(entry)
            if ok: 
                self.log("✅ Runtime OK")
                return
            
            # 依存関係エラーなら即インストールしてリトライ
            if "ModuleNotFoundError" in log:
                missing = self._extract_module(log)
                if missing:
                    self.log(f"📦 Installing missing: {missing}")
                    self.ws.add_to_requirements(missing)
                    self.runtime.install_requirements()
                    continue

            self.log(f"💥 Runtime Error: {log[:100]}...")
            
            # ヒーリング (1回勝負)
            content = self.ws.project_files[entry]
            _, fixed, strat = self.healer.heal(entry, content, [log], self.ws.project_files, kit)
            
            if strat not in ["Loop_Ignored", "Skipped"]:
                self.ws.save_file(entry, fixed)
                self.ws.commit(f"Runtime Fix {entry}")
            else:
                self.log("⚠️ Runtime fix skipped.")
                break

    def _final_audit(self):
        """最終 QA 監査（1回）"""
        self.log("🕵️ Final QA Audit")
        res = self.qa.audit_and_fix(self.ws.project_files)
        
        if res:
            # LLMの出力からファイルをパースして保存
            self.ws.parse_and_save_files(res)
            self.ws.commit("QA Fix")
            self.log("✨ QA Fixed files")

    def _extract_module(self, log):
        import re
        m = re.search(r"No module named ['\"]([^'\"]+)['\"]", log)
        return m.group(1).split('.')[0] if m else None

    # --- Special Modes ---
    def _mode_kit_gen(self, prompt):
        yaml = self.kit_gen.generate_kit(prompt)
        name = self.kit_mgr.save_new_kit(yaml)
        return {"success": True, "logs": self.logs + [f"Kit {name} created."]}

    def _mode_research(self, prompt):
        rep = self.search.research(prompt)
        self.ws.save_file("research_report.md", rep)
        return {"success": True, "logs": self.logs + ["Research done."], "files": self.ws.project_files}


# --- Entry Point ---

def run_agent_task(prompt):
    """外部APIから呼び出されるエージェントのメイン実行関数"""
    orchestrator = Orchestrator()
    try: 
        return orchestrator.run(prompt)
    except Exception as e: 
        logger.error(f"Err: {e}")
        return {"success": False, "error": str(e), "logs": orchestrator.logs}
    finally: 
        orchestrator.cleanup()

def get_realtime_data(start=0):
    # 実行環境外ではログ取得は機能しないため、ダミーを返す
    return {"new_logs": [], "stats": {}}