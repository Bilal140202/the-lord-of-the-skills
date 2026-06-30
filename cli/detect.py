#!/usr/bin/env python3
"""
lotr detect — Stack + framework detector.

Reads the user's project folder and returns:
  {framework, languages, stack, project_root}

Priority order (first match wins):
  .antigravity/ → antigravity
  .cursor/      → cursor
  .claude/      → claude-code
  .clinerules/  → cline
  .roo/         → roo
  .continue/    → continue
  .goose/       → goose
  AGENTS.md     → codex
  CONVENTIONS.md → aider
  .github/copilot-instructions.md → copilot

Then sniffs package.json / requirements.txt / pyproject.toml / Gemfile / etc.
for language + framework stack.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Optional

# Framework detection order — first match wins
FRAMEWORK_MARKERS = [
    ("antigravity",  [".antigravity"]),
    ("cursor",       [".cursor", ".cursorrules"]),
    ("claude-code",  [".claude", "CLAUDE.md"]),
    ("cline",        [".clinerules", ".cline"]),
    ("roo",          [".roo"]),
    ("continue",     [".continue"]),
    ("goose",        [".goose"]),
    ("aider",        ["CONVENTIONS.md", ".aider.conf.yml", ".aider.conf.yaml"]),
    ("codex",        ["AGENTS.md"]),
    ("copilot",      [".github/copilot-instructions.md"]),
]

# Language / stack sniffers (file → parser)
def _parse_package_json(path: Path) -> dict:
    """Extract stack from package.json deps."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    stack = []
    # Frameworks
    if "react" in deps:        stack.append("react")
    if "next" in deps:         stack.append("next")
    if "vue" in deps:          stack.append("vue")
    if "nuxt" in deps:         stack.append("nuxt")
    if "svelte" in deps or "@sveltejs/kit" in deps: stack.append("svelte")
    if "astro" in deps:        stack.append("astro")
    if "@angular/core" in deps: stack.append("angular")
    if "solid-js" in deps:     stack.append("solid")
    # Languages
    if "typescript" in deps:   stack.append("typescript")
    # Build tools
    if "vite" in deps:         stack.append("vite")
    if "webpack" in deps:      stack.append("webpack")
    if "esbuild" in deps:      stack.append("esbuild")
    if "turbo" in deps or "@turbo/gen" in deps: stack.append("turbo")
    # Testing
    if "jest" in deps or "vitest" in deps: stack.append("jest")
    if "playwright" in deps:   stack.append("playwright")
    if "cypress" in deps:      stack.append("cypress")
    # Backend
    if "express" in deps:      stack.append("express")
    if "fastify" in deps:      stack.append("fastify")
    if "hono" in deps:         stack.append("hono")
    # Styling
    if "tailwindcss" in deps:  stack.append("tailwind")
    if "@emotion/react" in deps: stack.append("emotion")
    # Misc
    if "prisma" in deps or "@prisma/client" in deps: stack.append("prisma")
    if "drizzle-orm" in deps:  stack.append("drizzle")
    if "trpc" in deps or "@trpc/server" in deps: stack.append("trpc")
    return {"language": "typescript" if "typescript" in deps else "javascript",
            "stack": stack, "deps": list(deps.keys())[:20]}

def _parse_requirements_txt(path: Path) -> dict:
    """Extract stack from requirements.txt."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    lines = [l.split("#")[0].split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].strip().lower()
             for l in text.splitlines()]
    stack = []
    if any("fastapi" in l for l in lines):  stack.append("fastapi")
    if any("django" in l for l in lines):   stack.append("django")
    if any("flask" in l for l in lines):    stack.append("flask")
    if any("starlette" in l for l in lines): stack.append("starlette")
    if any("pydantic" in l for l in lines): stack.append("pydantic")
    if any("sqlalchemy" in l for l in lines): stack.append("sqlalchemy")
    if any("torch" in l for l in lines):    stack.append("pytorch")
    if any("tensorflow" in l for l in lines): stack.append("tensorflow")
    if any("transformers" in l for l in lines): stack.append("transformers")
    if any("langchain" in l for l in lines): stack.append("langchain")
    if any("pandas" in l for l in lines):   stack.append("pandas")
    if any("numpy" in l for l in lines):    stack.append("numpy")
    return {"language": "python", "stack": stack, "deps": [l for l in lines if l][:20]}

def _parse_pyproject_toml(path: Path) -> dict:
    """Extract stack from pyproject.toml (basic, no tomllib needed for v3.10+)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    try:
        import tomllib
        data = tomllib.loads(text)
    except Exception:
        # Fallback: regex sniff
        stack = []
        for lib in ["fastapi", "django", "flask", "pydantic", "sqlalchemy", "torch",
                    "transformers", "langchain", "pandas", "numpy"]:
            if re.search(rf'["\']{lib}["\']', text, re.I):
                stack.append(lib)
        return {"language": "python", "stack": stack, "deps": []}
    # tomllib available
    deps = []
    for section in ["dependencies", "project.dependencies"]:
        if "project" in data and "dependencies" in data["project"]:
            deps = data["project"]["dependencies"]
            break
        if "dependencies" in data:
            deps = data["dependencies"]
            break
    stack = []
    for d in deps:
        dl = d.lower()
        for lib in ["fastapi", "django", "flask", "pydantic", "sqlalchemy", "torch",
                    "transformers", "langchain", "pandas", "numpy"]:
            if lib in dl and lib not in stack:
                stack.append(lib)
    return {"language": "python", "stack": stack, "deps": [d.split("==")[0].split(">=")[0].strip() for d in deps][:20]}

def _parse_gemfile(path: Path) -> dict:
    """Extract stack from Gemfile."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    stack = []
    if "rails" in text.lower(): stack.append("rails")
    if "sinatra" in text.lower(): stack.append("sinatra")
    if "jekyll" in text.lower(): stack.append("jekyll")
    return {"language": "ruby", "stack": stack, "deps": []}

def _parse_go_mod(path: Path) -> dict:
    """Extract stack from go.mod."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    stack = []
    if "gin-gonic" in text: stack.append("gin")
    if "fiber" in text: stack.append("fiber")
    if "echo" in text: stack.append("echo")
    if "gorm" in text: stack.append("gorm")
    return {"language": "go", "stack": stack, "deps": []}

def _parse_cargo_toml(path: Path) -> dict:
    """Extract stack from Cargo.toml."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    stack = []
    if "tokio" in text: stack.append("tokio")
    if "axum" in text: stack.append("axum")
    if "actix" in text: stack.append("actix")
    if "serde" in text: stack.append("serde")
    return {"language": "rust", "stack": stack, "deps": []}

# Language sniffers by filename
LANGUAGE_SNIFFERS = [
    ("package.json",    _parse_package_json),
    ("requirements.txt", _parse_requirements_txt),
    ("pyproject.toml",  _parse_pyproject_toml),
    ("Pipfile",         lambda p: {"language": "python", "stack": [], "deps": []}),
    ("Gemfile",         _parse_gemfile),
    ("go.mod",          _parse_go_mod),
    ("Cargo.toml",      _parse_cargo_toml),
    ("composer.json",   lambda p: {"language": "php", "stack": [], "deps": []}),
    ("pom.xml",         lambda p: {"language": "java", "stack": ["maven"], "deps": []}),
    ("build.gradle",    lambda p: {"language": "java", "stack": ["gradle"], "deps": []}),
    ("mix.exs",         lambda p: {"language": "elixir", "stack": [], "deps": []}),
]

def detect_framework(project_root: Path) -> Optional[str]:
    """Detect the AI agent framework in use. Returns None if no framework detected."""
    for framework, markers in FRAMEWORK_MARKERS:
        for marker in markers:
            if (project_root / marker).exists():
                return framework
    return None

def detect_stack(project_root: Path) -> dict:
    """Detect the project's language + stack. Returns {language, stack, deps}."""
    for filename, parser in LANGUAGE_SNIFFERS:
        path = project_root / filename
        if path.exists():
            result = parser(path)
            if result:
                return result
    # Fallback: sniff by extension counts
    py_count = sum(1 for _ in project_root.rglob("*.py") if _.is_file())
    js_count = sum(1 for _ in project_root.rglob("*.js") if _.is_file()) + \
               sum(1 for _ in project_root.rglob("*.ts") if _.is_file())
    rs_count = sum(1 for _ in project_root.rglob("*.rs") if _.is_file())
    go_count = sum(1 for _ in project_root.rglob("*.go") if _.is_file())
    counts = {"python": py_count, "javascript": js_count, "rust": rs_count, "go": go_count}
    top = max(counts, key=counts.get)
    if counts[top] > 0:
        return {"language": top, "stack": [], "deps": []}
    return {"language": "unknown", "stack": [], "deps": []}

def detect(project_root: Path | str = ".") -> dict:
    """Full detection: framework + stack. Returns:
        {
            "framework": "antigravity" | "cursor" | ... | None,
            "language": "typescript" | "python" | ... | "unknown",
            "stack": ["react", "next", ...],
            "deps": ["react", "next", ...],
            "project_root": "/abs/path"
        }
    """
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Project root not found: {root}")
    return {
        "framework": detect_framework(root),
        "language": None,  # filled below
        "stack": [],
        "deps": [],
        "project_root": str(root),
        **detect_stack(root),
    }

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    result = detect(target)
    print(json.dumps(result, indent=2))
