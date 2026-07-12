#!/usr/bin/env python3
"""
The Lord of the Skills — Web UI
================================
A Streamlit app for browsing and searching 17,000+ AI agent skills.

Features:
  - Search by keyword (title, summary, tags)
  - Filter by kingdom, framework, canonical status
  - Preview skill content
  - Kingdom statistics dashboard
  - Framework coverage chart
  - Copy install command with one click

Run locally:
  streamlit run web/app.py

Deploy to Hugging Face Spaces / Streamlit Cloud / GitHub Pages (via static export)
"""

import json
import sys
import os
from pathlib import Path
from collections import Counter
import urllib.request

import streamlit as st

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
INDEX_URL = "https://raw.githubusercontent.com/Bilal140202/the-lord-of-the-skills/main/skills/index.json"
RAW_BASE = "https://raw.githubusercontent.com/Bilal140202/the-lord-of-the-skills/main"
LOCAL_INDEX = Path(__file__).resolve().parent.parent / "skills" / "index.json"
CACHE_TTL = 3600  # 1 hour

KINGDOM_INFO = {
    "gondor":       {"name": "Gondor",       "domain": "Coding & Software Engineering",  "symbol": "⚔", "color": "#1e3a8a"},
    "rivendell":    {"name": "Rivendell",    "domain": "Research & Knowledge",           "symbol": "✦", "color": "#0f766e"},
    "moria":        {"name": "Moria",        "domain": "DevOps & Infrastructure",        "symbol": "⛏", "color": "#4b5563"},
    "lothlorien":   {"name": "Lothlórien",   "domain": "Data & Analysis",                "symbol": "✿", "color": "#15803d"},
    "mordor":       {"name": "Mordor",       "domain": "Security & Auditing",            "symbol": "👁", "color": "#991b1b"},
    "the-shire":    {"name": "The Shire",    "domain": "Writing & Content",              "symbol": "✎", "color": "#a16207"},
    "isengard":     {"name": "Isengard",     "domain": "Agents & Orchestration",         "symbol": "⚙", "color": "#52525b"},
    "rohan":        {"name": "Rohan",        "domain": "Testing & Verification",         "symbol": "🐴", "color": "#92400e"},
    "fangorn":      {"name": "Fangorn",      "domain": "Documentation & Memory",         "symbol": "🌳", "color": "#166534"},
    "mirkwood":     {"name": "Mirkwood",     "domain": "Specialized & Niche",            "symbol": "🕸", "color": "#581c87"},
    "minas-tirith": {"name": "Minas Tirith", "domain": "UI & Design",                    "symbol": "🏰", "color": "#7c3aed"},
}

# ─────────────────────────────────────────────
# Data loading (with caching)
# ─────────────────────────────────────────────

@st.cache_data(ttl=CACHE_TTL, show_spinner="Loading 17,000+ skills...")
def load_index():
    """Load the skills index. Tries remote first, falls back to local."""
    # Try remote
    try:
        req = urllib.request.Request(INDEX_URL, headers={
            "User-Agent": "lotr-skills-web-ui/1.0"
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            return data
    except Exception:
        pass
    # Fall back to local
    if LOCAL_INDEX.exists():
        with open(LOCAL_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    st.error("Could not load skills index. Please check your internet connection.")
    st.stop()


def fetch_skill_content(kingdom, framework, skill_path):
    """Fetch a single skill file's content from GitHub raw."""
    url = f"{RAW_BASE}/skills/{kingdom}/{framework}/{skill_path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "lotr-skills-web-ui/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8")
    except Exception:
        # Try local
        local = Path(__file__).resolve().parent.parent / "skills" / kingdom / framework / skill_path
        if local.exists():
            return local.read_text(encoding="utf-8")
        return f"*Could not fetch skill content from {url}*"


# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="The Lord of the Skills — AI Agent Skills Browser",
    page_icon="⚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────

index_data = load_index()
all_skills = index_data.get("skills", [])
total_skills = index_data.get("total_skills", len(all_skills))
canonical_count = index_data.get("canonical_count", 0)
kingdom_dist = index_data.get("kingdoms", {})
framework_dist = index_data.get("frameworks", {})

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

st.markdown("""
<div style='text-align: center; padding: 20px 0 10px 0;'>
<h1 style='color: #B8860B; margin-bottom: 5px;'>⚔ The Lord of the Skills</h1>
<p style='color: #666; font-size: 1.2em;'>
One catalog to rule them all — {total:,} AI agent skills across {kingdoms} kingdoms and {frameworks} frameworks
</p>
</div>
""".format(
    total=total_skills,
    kingdoms=len(kingdom_dist),
    frameworks=len(framework_dist),
), unsafe_allow_html=True)

# Top stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Skills", f"{total_skills:,}")
with col2:
    st.metric("Canonical ⭐", f"{canonical_count}")
with col3:
    st.metric("Kingdoms", f"{len(kingdom_dist)}")
with col4:
    st.metric("Frameworks", f"{len(framework_dist)}")

st.divider()

# ─────────────────────────────────────────────
# Sidebar — Filters
# ─────────────────────────────────────────────

st.sidebar.markdown("## 🔍 Filters")

# Search box
search_query = st.sidebar.text_input(
    "Search skills",
    placeholder="e.g., code review, git commit, react, security...",
    help="Searches title, summary, and tags"
)

# Kingdom filter
kingdom_options = ["All Kingdoms"] + sorted(kingdom_dist.keys())
selected_kingdom = st.sidebar.selectbox(
    "Kingdom",
    kingdom_options,
    format_func=lambda x: f"{KINGDOM_INFO.get(x, {}).get('symbol', '')} {KINGDOM_INFO.get(x, {}).get('name', x.title())}" if x != "All Kingdoms" else "All Kingdoms"
)

# Framework filter
framework_options = ["All Frameworks"] + sorted(framework_dist.keys())
selected_framework = st.sidebar.selectbox("Framework", framework_options)

# Canonical filter
canonical_only = st.sidebar.checkbox("⭐ Canonical only", value=False)

# Limit results
result_limit = st.sidebar.slider("Max results", min_value=10, max_value=500, value=50, step=10)

# Install command
st.sidebar.divider()
st.sidebar.markdown("## 📦 Install")
st.sidebar.code("pip install lotr-skills", language="bash")
st.sidebar.markdown("**Then:**")
st.sidebar.code('lotr "write unit tests"', language="bash")
st.sidebar.markdown("📖 [Quick Start](https://github.com/Bilal140202/the-lord-of-the-skills#-quick-start-60-seconds)")

# ─────────────────────────────────────────────
# Apply filters
# ─────────────────────────────────────────────

filtered = all_skills

# Kingdom filter
if selected_kingdom != "All Kingdoms":
    filtered = [s for s in filtered if s.get("kingdom") == selected_kingdom]

# Framework filter
if selected_framework != "All Frameworks":
    filtered = [s for s in filtered if selected_framework in s.get("frameworks", [])]

# Canonical filter
if canonical_only:
    filtered = [s for s in filtered if s.get("canonical")]

# Search filter
if search_query:
    q = search_query.lower()
    filtered = [
        s for s in filtered
        if q in (s.get("title", "").lower() or "")
        or q in (s.get("summary", "").lower() or "")
        or q in (s.get("filename", "").lower() or "")
        or any(q in tag.lower() for tag in s.get("tags", []))
    ]

# Limit
filtered_limited = filtered[:result_limit]

# ─────────────────────────────────────────────
# Results count
# ─────────────────────────────────────────────

st.markdown(f"**Found {len(filtered):,} skills** (showing {len(filtered_limited)})")

# ─────────────────────────────────────────────
# Tabs: Browse | Kingdoms | Frameworks
# ─────────────────────────────────────────────

tab_browse, tab_kingdoms, tab_frameworks = st.tabs(["📋 Browse Skills", "🏰 Kingdoms", "⚙ Frameworks"])

# ── Browse tab ───────────────────────────────

with tab_browse:
    if not filtered_limited:
        st.info("No skills found. Try adjusting your filters or search query.")
    else:
        # Display as a data table
        import pandas as pd

        df_data = []
        for s in filtered_limited:
            info = KINGDOM_INFO.get(s.get("kingdom", ""), {})
            df_data.append({
                "⭐": "⭐" if s.get("canonical") else "",
                "Title": s.get("title", "(untitled)")[:60],
                "Kingdom": f"{info.get('symbol', '')} {info.get('name', s.get('kingdom','?').title())}",
                "Framework": ", ".join(s.get("frameworks", [])),
                "Source": s.get("source_repo", ""),
                "Tags": ", ".join(s.get("tags", [])[:5]),
                "_skill": s,  # hidden reference
            })

        df = pd.DataFrame(df_data)

        # Display as editable table (clickable-ish)
        st.dataframe(
            df.drop(columns=["_skill"]),
            use_container_width=True,
            hide_index=True,
            column_config={
                "⭐": st.column_config.TextColumn("⭐", width="small"),
                "Title": st.column_config.TextColumn("Title", width="medium"),
                "Kingdom": st.column_config.TextColumn("Kingdom", width="small"),
                "Framework": st.column_config.TextColumn("Framework", width="small"),
                "Source": st.column_config.TextColumn("Source Repo", width="small"),
                "Tags": st.column_config.TextColumn("Tags", width="medium"),
            },
        )

        # Skill detail viewer
        st.divider()
        st.markdown("### 📄 Skill Detail Viewer")

        selected_idx = st.selectbox(
            "Select a skill to preview:",
            range(len(filtered_limited)),
            format_func=lambda i: f"{filtered_limited[i].get('title', '(untitled)')[:60]} — {filtered_limited[i].get('kingdom', '?')}"
        )

        if selected_idx is not None:
            skill = filtered_limited[selected_idx]
            info = KINGDOM_INFO.get(skill.get("kingdom", ""), {})

            # Skill metadata
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown(f"**Kingdom:** {info.get('symbol', '')} {info.get('name', '?')}")
                st.markdown(f"**Domain:** {info.get('domain', '?')}")
            with mc2:
                st.markdown(f"**Framework:** {', '.join(skill.get('frameworks', []))}")
                st.markdown(f"**Canonical:** {'⭐ Yes' if skill.get('canonical') else 'No'}")
            with mc3:
                st.markdown(f"**Source:** [`{skill.get('source_repo', '?')}`](https://github.com/{skill.get('source_repo', '')})")
                st.markdown(f"**Size:** {skill.get('size_bytes', 0):,} bytes")

            # Summary
            summary = skill.get("summary", "")
            if summary:
                st.markdown(f"**Summary:** {summary}")

            # Tags
            tags = skill.get("tags", [])
            if tags:
                st.markdown("**Tags:** " + " ".join(f"`{t}`" for t in tags[:15]))

            # Fetch and display content
            st.markdown("---")
            st.markdown("#### 📜 Skill Content")

            # Build the relative path for fetching
            skill_path = skill.get("path", "")
            kingdom = skill.get("kingdom", "")
            framework = skill.get("frameworks", ["general"])[0] if skill.get("frameworks") else "general"
            # Strip the prefix to get the relative path within the kingdom/framework
            rel_path = skill_path
            for prefix in [f"skills/{kingdom}/{framework}/", f"skills/{kingdom}/"]:
                if rel_path.startswith(prefix):
                    rel_path = rel_path[len(prefix):]
                    break

            with st.spinner("Fetching skill content..."):
                content = fetch_skill_content(kingdom, framework, rel_path)

            st.markdown(content)

            # Install command
            st.markdown("---")
            st.markdown("**Install this skill:**")
            kingdom = skill.get("kingdom", "gondor")
            framework = skill.get("frameworks", ["claude-code"])[0]
            filename = skill.get("filename", "SKILL.md")
            st.code(f'lotr install --kingdom {kingdom} --framework {framework}', language="bash")


# ── Kingdoms tab ─────────────────────────────

with tab_kingdoms:
    st.markdown("## 🏰 The Eleven Kingdoms")
    st.markdown("*Ten domains of agent capability, one catalog to rule them all.*")

    # Kingdom cards
    cols = st.columns(3)
    for i, (kingdom, count) in enumerate(sorted(kingdom_dist.items(), key=lambda x: -x[1])):
        info = KINGDOM_INFO.get(kingdom, {"name": kingdom.title(), "domain": "?", "symbol": "?", "color": "#666"})
        col = cols[i % 3]
        with col:
            st.markdown(f"""
            <div style='
                border: 2px solid {info["color"]};
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
                text-align: center;
            '>
                <div style='font-size: 2em;'>{info["symbol"]}</div>
                <div style='font-size: 1.2em; font-weight: bold; color: {info["color"]};'>{info["name"]}</div>
                <div style='font-size: 0.9em; color: #888;'>{info["domain"]}</div>
                <div style='font-size: 1.5em; font-weight: bold; margin-top: 5px;'>{count:,}</div>
                <div style='font-size: 0.8em; color: #aaa;'>artifacts</div>
            </div>
            """, unsafe_allow_html=True)

    # Bar chart
    st.divider()
    st.markdown("### 📊 Skills per Kingdom")
    k_df = pd.DataFrame([
        {"Kingdom": KINGDOM_INFO.get(k, {}).get("name", k.title()), "Skills": v}
        for k, v in sorted(kingdom_dist.items(), key=lambda x: -x[1])
    ])
    st.bar_chart(k_df.set_index("Kingdom"))


# ── Frameworks tab ───────────────────────────

with tab_frameworks:
    st.markdown("## ⚙ Framework Coverage")
    st.markdown(f"*{len(framework_dist)} frameworks supported by the CLI.*")

    # Framework table
    fw_data = []
    for fw, count in sorted(framework_dist.items(), key=lambda x: -x[1]):
        fw_data.append({
            "Framework": fw,
            "Skills": count,
            "Install Command": f"lotr install --framework {fw} \"your task\"",
        })
    fw_df = pd.DataFrame(fw_data)
    st.dataframe(fw_df, use_container_width=True, hide_index=True)

    # Bar chart
    st.divider()
    st.markdown("### 📊 Skills per Framework")
    f_df = pd.DataFrame([
        {"Framework": k, "Skills": v}
        for k, v in sorted(framework_dist.items(), key=lambda x: -x[1])
    ])
    st.bar_chart(f_df.set_index("Framework"))

    # Per-framework detection patterns
    st.divider()
    st.markdown("### 🔍 How lotr Detects Your Framework")
    st.markdown("""
    | Framework | Detection Marker | Destination |
    |:---|:---|:---|
    | antigravity | `.antigravity/` | `.antigravity/skills/` |
    | cursor | `.cursor/`, `.cursorrules` | `.cursor/rules/` |
    | claude-code | `.claude/`, `CLAUDE.md` | `~/.claude/skills/` |
    | cline | `.clinerules/` | `.clinerules/` |
    | roo | `.roo/` | `.roo/rules/` |
    | aider | `CONVENTIONS.md`, `.aider*` | appends to `CONVENTIONS.md` |
    | codex | `AGENTS.md` | appends to `AGENTS.md` |
    | continue | `.continue/` | `.continue/rules/` |
    | goose | `.goose/` | `.goose/extensions/` |
    | copilot | `.github/copilot-instructions.md` | appends |
    """)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────

st.divider()
st.markdown("""
<div style='text-align: center; color: #888; padding: 20px 0;'>
<p>⚔ <strong>The Lord of the Skills</strong> — Built by <a href='https://github.com/Bilal140202'>Ansari Mohammad Bilal</a></p>
<p>
<a href='https://github.com/Bilal140202/the-lord-of-the-skills'>GitHub</a> ·
<a href='https://pypi.org/project/lotr-skills/'>PyPI</a> ·
<a href='https://dev.to/ansari_bilal/the-ultimate-collection-of-18k-ai-agent-skills-across-14-frameworks-fbo'>Dev.to Article</a> ·
<code>pip install lotr-skills</code>
</p>
<p><em>May your agents be wise, your prompts be sharp, and your skills be many.</em></p>
</div>
""", unsafe_allow_html=True)
