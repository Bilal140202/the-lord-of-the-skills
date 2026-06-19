#!/usr/bin/env python3
"""
The Lord of the Skills — Master PDF Catalog Generator
======================================================
Builds a LOTR-themed PDF catalog using ReportLab.

Structure:
  1. Cover page (LOTR themed, dark background, gold title)
  2. Fellowship Manifesto (intro)
  3. Map of the Kingdoms (10 kingdoms overview)
  4. Per-kingdom sections (top canonical skills with summaries)
  5. Framework coverage table
  6. Credits summary
"""

from __future__ import annotations

import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, Image, Flowable
)
from reportlab.platypus.flowables import HRFlowable

ROOT = Path("/home/z/my-project/the-lord-of-the-skills")
IN_PATH = ROOT / "_cache" / "manifest_final.json"
OUT_PATH = Path("/home/z/my-project/download/the-lord-of-the-skills/Lord_of_the_Skills_Catalog.pdf")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Font registration (CJK-safe + serif for that "tome" feel)
# ----------------------------------------------------------------------
FONT_PATHS = {
    "BodySerif":     "/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Regular.otf",
    "BodySerifBold": "/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.otf",
    "HeadingSerif":  "/usr/share/fonts/truetype/noto-serif-sc/NotoSerifSC-Bold.otf",
    "BodySans":      "/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
    "BodySansBold":  "/usr/share/fonts/truetype/chinese/NotoSansSC-Bold.ttf",
    "Mono":          "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
}
for name, path in FONT_PATHS.items():
    if Path(path).exists():
        try:
            pdfmetrics.registerFont(TTFont(name, path))
        except Exception as e:
            print(f"  font register fail {name}: {e}")

# Fallback names
SERIF = "BodySerif" if "BodySerif" in pdfmetrics.getRegisteredFontNames() else "Times-Roman"
SERIF_BOLD = "BodySerifBold" if "BodySerifBold" in pdfmetrics.getRegisteredFontNames() else "Times-Bold"
SANS = "BodySans" if "BodySans" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
SANS_BOLD = "BodySansBold" if "BodySansBold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
MONO = "Mono" if "Mono" in pdfmetrics.getRegisteredFontNames() else "Courier"

# ----------------------------------------------------------------------
# LOTR theme palette
# ----------------------------------------------------------------------
COLOR_PARCHMENT = colors.HexColor("#F5E9C9")     # aged parchment
COLOR_DARK_BROWN = colors.HexColor("#3D2817")    # dark leather
COLOR_GOLD = colors.HexColor("#B8860B")          # dark gold
COLOR_DEEP_RED = colors.HexColor("#7C1F1F")      # mordor red
COLOR_FOREST = colors.HexColor("#1F4D2C")        # fangorn green
COLOR_ROYAL_BLUE = colors.HexColor("#1E3A8A")    # gondor blue
COLOR_STONE = colors.HexColor("#4B5563")         # moria stone
COLOR_TEAL = colors.HexColor("#0F766E")          # rivendell teal
COLOR_HORSE = colors.HexColor("#92400E")         # rohan brown
COLOR_PURPLE = colors.HexColor("#581C87")        # mirkwood purple
COLOR_LIGHT_GRAY = colors.HexColor("#F3F4F6")
COLOR_MID_GRAY = colors.HexColor("#9CA3AF")

KINGDOMS = {
    "gondor":      {"name": "Gondor",       "domain": "Coding & Software Engineering",
                    "motto": "Gondor sees, Gondor codes.",
                    "color": COLOR_ROYAL_BLUE, "symbol": "⚔"},
    "rivendell":   {"name": "Rivendell",    "domain": "Research & Knowledge",
                    "motto": "Knowledge flows from the Last Homely House.",
                    "color": COLOR_TEAL, "symbol": "✦"},
    "moria":       {"name": "Moria",        "domain": "DevOps & Infrastructure",
                    "motto": "Speak, friend, and enter the deploy.",
                    "color": COLOR_STONE, "symbol": "⛏"},
    "lothlorien":  {"name": "Lothlórien",   "domain": "Data & Analysis",
                    "motto": "Where data roots run deep.",
                    "color": COLOR_FOREST, "symbol": "✿"},
    "mordor":      {"name": "Mordor",       "domain": "Security & Auditing",
                    "motto": "One audit to rule them all.",
                    "color": COLOR_DEEP_RED, "symbol": "👁"},
    "the-shire":   {"name": "The Shire",    "domain": "Writing & Content",
                    "motto": "Quiet writing, deep roots.",
                    "color": COLOR_GOLD, "symbol": "✎"},
    "isengard":    {"name": "Isengard",     "domain": "Agents & Orchestration",
                    "motto": "Industry wakes the deep.",
                    "color": COLOR_STONE, "symbol": "⚙"},
    "rohan":       {"name": "Rohan",        "domain": "Testing & Verification",
                    "motto": "Ride now, ride to verify.",
                    "color": COLOR_HORSE, "symbol": "🐴"},
    "fangorn":     {"name": "Fangorn",      "domain": "Documentation & Memory",
                    "motto": "The old forest remembers.",
                    "color": COLOR_FOREST, "symbol": "🌳"},
    "mirkwood":    {"name": "Mirkwood",     "domain": "Specialized & Niche",
                    "motto": "Strange paths through the wood.",
                    "color": COLOR_PURPLE, "symbol": "🕸"},
}

KINGDOM_ORDER = ["gondor", "rivendell", "isengard", "moria", "lothlorien",
                 "mordor", "the-shire", "rohan", "fangorn", "mirkwood"]

# ----------------------------------------------------------------------
# Paragraph styles
# ----------------------------------------------------------------------
def build_styles():
    base = getSampleStyleSheet()
    styles = {}
    styles["CoverTitle"] = ParagraphStyle(
        "CoverTitle", parent=base["Title"],
        fontName=SERIF_BOLD, fontSize=42, leading=48,
        alignment=1, textColor=COLOR_GOLD, spaceAfter=12)
    styles["CoverSub"] = ParagraphStyle(
        "CoverSub", parent=base["Normal"],
        fontName=SERIF, fontSize=14, leading=18,
        alignment=1, textColor=COLOR_PARCHMENT, spaceAfter=8)
    styles["CoverTagline"] = ParagraphStyle(
        "CoverTagline", parent=base["Normal"],
        fontName=SERIF, fontSize=11, leading=15,
        alignment=1, textColor=COLOR_GOLD, spaceAfter=4,
        leftIndent=60, rightIndent=60)
    styles["CoverFooter"] = ParagraphStyle(
        "CoverFooter", parent=base["Normal"],
        fontName=SERIF, fontSize=9, leading=12,
        alignment=1, textColor=COLOR_MID_GRAY)
    styles["H1"] = ParagraphStyle(
        "H1", parent=base["Heading1"],
        fontName=SERIF_BOLD, fontSize=24, leading=30,
        textColor=COLOR_DARK_BROWN, spaceBefore=12, spaceAfter=12,
        borderPadding=4, borderWidth=0, borderColor=COLOR_GOLD)
    styles["H2"] = ParagraphStyle(
        "H2", parent=base["Heading2"],
        fontName=SERIF_BOLD, fontSize=18, leading=22,
        textColor=COLOR_DARK_BROWN, spaceBefore=16, spaceAfter=8)
    styles["H3"] = ParagraphStyle(
        "H3", parent=base["Heading3"],
        fontName=SANS_BOLD, fontSize=12, leading=16,
        textColor=COLOR_DARK_BROWN, spaceBefore=8, spaceAfter=4)
    styles["Body"] = ParagraphStyle(
        "Body", parent=base["BodyText"],
        fontName=SERIF, fontSize=10, leading=14,
        textColor=COLOR_DARK_BROWN, alignment=4,  # justify
        spaceAfter=6)
    styles["BodyItalic"] = ParagraphStyle(
        "BodyItalic", parent=styles["Body"],
        fontName=SERIF, fontSize=11, leading=15,
        textColor=COLOR_DARK_BROWN, alignment=1,
        spaceAfter=8, leftIndent=20, rightIndent=20)
    styles["Quote"] = ParagraphStyle(
        "Quote", parent=base["BodyText"],
        fontName=SERIF, fontSize=10, leading=14,
        textColor=COLOR_DARK_BROWN, alignment=2,  # right
        leftIndent=40, rightIndent=20, spaceAfter=6,
        fontStyle="italic")
    styles["SkillTitle"] = ParagraphStyle(
        "SkillTitle", parent=base["BodyText"],
        fontName=SANS_BOLD, fontSize=10, leading=12,
        textColor=COLOR_DARK_BROWN, spaceAfter=2)
    styles["SkillMeta"] = ParagraphStyle(
        "SkillMeta", parent=base["BodyText"],
        fontName=MONO, fontSize=8, leading=10,
        textColor=COLOR_STONE, spaceAfter=2)
    styles["SkillSummary"] = ParagraphStyle(
        "SkillSummary", parent=base["BodyText"],
        fontName=SERIF, fontSize=9, leading=11,
        textColor=COLOR_DARK_BROWN, alignment=0,  # left
        spaceAfter=6, leftIndent=10)
    styles["KingdomHeader"] = ParagraphStyle(
        "KingdomHeader", parent=base["Heading1"],
        fontName=SERIF_BOLD, fontSize=32, leading=38,
        alignment=1, textColor=COLOR_GOLD, spaceAfter=12)
    styles["KingdomSub"] = ParagraphStyle(
        "KingdomSub", parent=base["Normal"],
        fontName=SERIF, fontSize=14, leading=18,
        alignment=1, textColor=COLOR_PARCHMENT, spaceAfter=8)
    styles["KingdomMotto"] = ParagraphStyle(
        "KingdomMotto", parent=base["Normal"],
        fontName=SERIF, fontSize=11, leading=15,
        alignment=1, textColor=COLOR_GOLD,
        leftIndent=40, rightIndent=40, spaceAfter=12,
        fontStyle="italic")
    styles["TableCell"] = ParagraphStyle(
        "TableCell", parent=base["BodyText"],
        fontName=SANS, fontSize=9, leading=11,
        textColor=COLOR_DARK_BROWN)
    styles["TableHeader"] = ParagraphStyle(
        "TableHeader", parent=base["BodyText"],
        fontName=SANS_BOLD, fontSize=10, leading=12,
        textColor=colors.white, alignment=1)
    return styles

# ----------------------------------------------------------------------
# Cover page (drawn directly on canvas via onFirstPage)
# ----------------------------------------------------------------------
def draw_cover(canvas, doc):
    """Draw LOTR-themed cover page background, then content via flowables."""
    c = canvas
    w, h = A4
    # full dark background
    c.setFillColor(COLOR_DARK_BROWN)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    # subtle gold border frame
    c.setStrokeColor(COLOR_GOLD)
    c.setLineWidth(2)
    c.rect(2 * cm, 2 * cm, w - 4 * cm, h - 4 * cm, fill=0, stroke=1)
    c.setLineWidth(0.5)
    c.rect(2.3 * cm, 2.3 * cm, w - 4.6 * cm, h - 4.6 * cm, fill=0, stroke=1)
    # corner flourishes
    for cx, cy in [(2 * cm, 2 * cm), (w - 2 * cm, 2 * cm),
                   (2 * cm, h - 2 * cm), (w - 2 * cm, h - 2 * cm)]:
        c.setFillColor(COLOR_GOLD)
        c.circle(cx, cy, 4, fill=1, stroke=0)
    # title block (top third)
    c.setFillColor(COLOR_GOLD)
    c.setFont(SERIF_BOLD, 48)
    c.drawCentredString(w / 2, h - 8 * cm, "THE LORD")
    c.drawCentredString(w / 2, h - 10 * cm, "OF THE SKILLS")
    # decorative divider
    c.setStrokeColor(COLOR_GOLD)
    c.setLineWidth(1)
    c.line(w / 2 - 6 * cm, h - 11 * cm, w / 2 + 6 * cm, h - 11 * cm)
    # subtitle
    c.setFillColor(COLOR_PARCHMENT)
    c.setFont(SERIF, 14)
    c.drawCentredString(w / 2, h - 12.5 * cm, "A Compilation of Agentic AI Skills")
    c.drawCentredString(w / 2, h - 13.5 * cm, "from across the GitHub realm")
    # tagline (italic)
    c.setFillColor(COLOR_GOLD)
    c.setFont(SERIF, 11)
    tagline_lines = [
        "One catalog to rule them all, one catalog to find them,",
        "One catalog to bring them all, and in the darkness bind them.",
    ]
    for i, line in enumerate(tagline_lines):
        c.drawCentredString(w / 2, h - 16 * cm - i * 0.6 * cm, line)
    # middle stats block
    c.setFillColor(COLOR_PARCHMENT)
    c.setFont(SERIF_BOLD, 11)
    c.drawCentredString(w / 2, 10 * cm, "Compiled by the Spider of the Skills")
    c.setFont(SERIF, 10)
    c.drawCentredString(w / 2, 9.2 * cm, f"{datetime.now(timezone.utc).strftime('%B %Y')}")
    # bottom: kingdoms crest row
    c.setFillColor(COLOR_GOLD)
    c.setFont(SERIF_BOLD, 9)
    kingdoms_str = " · ".join(KINGDOMS[k]["name"] for k in KINGDOM_ORDER)
    c.drawCentredString(w / 2, 5 * cm, kingdoms_str)
    # bottom motto
    c.setFillColor(COLOR_MID_GRAY)
    c.setFont(SERIF, 8)
    c.drawCentredString(w / 2, 3.5 * cm,
                        "May your agents be wise, your prompts be sharp, and your skills be many.")

# ----------------------------------------------------------------------
# Footer for body pages
# ----------------------------------------------------------------------
def draw_body_footer(canvas, doc):
    """Footer with page number + document title."""
    c = canvas
    w, h = A4
    c.saveState()
    c.setFillColor(COLOR_MID_GRAY)
    c.setFont(SERIF, 8)
    c.drawCentredString(w / 2, 1.2 * cm,
                        f"The Lord of the Skills  ·  Page {doc.page - 1}")
    # gold rule above footer
    c.setStrokeColor(COLOR_GOLD)
    c.setLineWidth(0.3)
    c.line(2 * cm, 1.6 * cm, w - 2 * cm, 1.6 * cm)
    c.restoreState()

# ----------------------------------------------------------------------
# Build flowables
# ----------------------------------------------------------------------
def build_cover_page(styles):
    """Cover content (mostly drawn via onFirstPage; this just occupies space)."""
    return [Spacer(1, 24 * cm)]  # leave room for canvas-drawn cover

def build_manifesto(styles, manifest):
    """Fellowship Manifesto intro."""
    flow = []
    flow.append(Paragraph("The Fellowship Manifesto", styles["H1"]))
    flow.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD,
                            spaceBefore=4, spaceAfter=12))
    flow.append(Paragraph(
        "<i>Ash nazg durbatulûk, ash nazg gimbatul, ash nazg thrakatulûk agh burzum-ishi krimpatul.</i>",
        styles["BodyItalic"]))
    flow.append(Paragraph(
        "<i>One catalog to rule them all, one catalog to find them, one catalog to bring them all, "
        "and in the darkness bind them.</i>",
        styles["BodyItalic"]))
    flow.append(Spacer(1, 12))
    flow.append(Paragraph(
        f"Across the wide lands of GitHub, scattered among ten thousand repositories, lie the Artifacts "
        f"of Agency — <b>SKILL.md</b> files that teach machines to act, <b>AGENTS.md</b> tomes that bind "
        f"them to conventions, <b>.cursorrules</b> scrolls that direct their hands, <b>.clinerules</b> "
        f"memory-banks that preserve their thought. For an age these artifacts lay divided: Claude Code "
        f"in the West, Cursor in the East, Cline in the deep places, Aider in the libraries, OpenHands "
        f"in the wild. No single hand gathered them. Until now.",
        styles["Body"]))
    flow.append(Paragraph(
        f"<b>The Lord of the Skills</b> is that gathering. A reusable Python crawler spidered "
        f"<b>{manifest.get('total_discovered_repos', 0)}</b> GitHub repositories, cloned "
        f"<b>{manifest.get('total_cloned_repos', 0)}</b> of them, and extracted "
        f"<b>{manifest.get('total_extracted_files', 0)}</b> skill, agent, and rule files. "
        f"Each artifact was sorted into one of ten kingdoms, tagged by its source framework, "
        f"classified by skill type, and deduplicated with a canonical representative chosen per concept. "
        f"The result is a portable library you can drop into any agentic AI tool — Claude Code, Cursor, "
        f"Cline, Roo, Aider, OpenHands, Continue, Goose, Copilot, or any future fellowship.",
        styles["Body"]))
    flow.append(Paragraph(
        f"This catalog is the printed companion to the digital package. It lists the canonical "
        f"representative of each concept cluster — those marked <b>⭐</b> — organized by kingdom. "
        f"The full set of {manifest.get('total_extracted_files', 0)} artifacts, with all variants "
        f"preserved, lives in the <code>skills/</code> directory of the digital package. Use the "
        f"Excel index for filtering and the manifest JSON for programmatic access.",
        styles["Body"]))
    flow.append(Spacer(1, 8))
    flow.append(Paragraph("— The Compiler", styles["Quote"]))
    flow.append(PageBreak())
    return flow

def build_map_of_kingdoms(styles, files):
    flow = []
    flow.append(Paragraph("The Map of the Kingdoms", styles["H1"]))
    flow.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD,
                            spaceBefore=4, spaceAfter=12))
    flow.append(Paragraph(
        "The Ten Kingdoms of the Lord of the Skills, each ruling a domain of agent capability. "
        "Artifacts were assigned to kingdoms by weighted keyword matching against their content, "
        "with framework bias for agent-orchestration skills. The table below shows the distribution.",
        styles["Body"]))
    counts = Counter(f["kingdom"] for f in files)
    canon_counts = Counter(f["kingdom"] for f in files if f.get("canonical"))
    header = [Paragraph(t, styles["TableHeader"]) for t in
              ["Kingdom", "Domain", "Artifacts", "Canonical", "Motto"]]
    rows = [header]
    for k in KINGDOM_ORDER:
        info = KINGDOMS[k]
        rows.append([
            Paragraph(f"{info['symbol']} {info['name']}", styles["TableCell"]),
            Paragraph(info["domain"], styles["TableCell"]),
            Paragraph(str(counts.get(k, 0)), styles["TableCell"]),
            Paragraph(str(canon_counts.get(k, 0)), styles["TableCell"]),
            Paragraph(f"<i>{info['motto']}</i>", styles["TableCell"]),
        ])
    total = sum(counts.values())
    total_canon = sum(canon_counts.values())
    rows.append([
        Paragraph("<b>TOTAL</b>", styles["TableCell"]),
        Paragraph("", styles["TableCell"]),
        Paragraph(f"<b>{total}</b>", styles["TableCell"]),
        Paragraph(f"<b>{total_canon}</b>", styles["TableCell"]),
        Paragraph("", styles["TableCell"]),
    ])
    table = Table(rows, colWidths=[3.2 * cm, 5.5 * cm, 2.2 * cm, 2 * cm, 5.3 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_DARK_BROWN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [COLOR_LIGHT_GRAY, colors.white]),
        ("BACKGROUND", (0, -1), (-1, -1), COLOR_GOLD),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.3, COLOR_MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flow.append(table)
    flow.append(Spacer(1, 14))
    flow.append(Paragraph(
        "Each kingdom hosts artifacts from multiple source frameworks. The chart below shows the "
        "breakdown by framework across all kingdoms, illustrating the diversity of the compilation.",
        styles["Body"]))
    fw_counts = Counter(f["framework"] for f in files)
    header2 = [Paragraph(t, styles["TableHeader"]) for t in ["Framework", "Artifacts", "Kingdoms"]]
    rows2 = [header2]
    fw_kingdoms = defaultdict(set)
    for f in files:
        fw_kingdoms[f["framework"]].add(f["kingdom"])
    for fw, count in fw_counts.most_common():
        rows2.append([
            Paragraph(fw, styles["TableCell"]),
            Paragraph(str(count), styles["TableCell"]),
            Paragraph(str(len(fw_kingdoms[fw])), styles["TableCell"]),
        ])
    table2 = Table(rows2, colWidths=[5 * cm, 5 * cm, 5 * cm])
    table2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_DARK_BROWN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_LIGHT_GRAY, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.3, COLOR_MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    flow.append(table2)
    flow.append(PageBreak())
    return flow

def build_kingdom_section(styles, kingdom_key, files, max_skills=40):
    """One section per kingdom."""
    info = KINGDOMS[kingdom_key]
    flow = []
    # Section header (styled)
    kingdom_files = [f for f in files if f["kingdom"] == kingdom_key]
    canon = sorted([f for f in kingdom_files if f.get("canonical")],
                   key=lambda x: x.get("title", "").lower())
    flow.append(Paragraph(f"{info['symbol']}  {info['name']}", styles["KingdomHeader"]))
    flow.append(Paragraph(info["domain"], styles["KingdomSub"]))
    flow.append(Paragraph(f"<i>\"{info['motto']}\"</i>", styles["KingdomMotto"]))
    flow.append(HRFlowable(width="60%", thickness=1, color=COLOR_GOLD,
                            hAlign="CENTER", spaceBefore=4, spaceAfter=14))
    # Stats line
    total = len(kingdom_files)
    canon_count = len(canon)
    fws = Counter(f["framework"] for f in kingdom_files)
    fw_str = ", ".join(f"{fw} ({c})" for fw, c in fws.most_common(5))
    flow.append(Paragraph(
        f"<b>Artifacts:</b> {total}  ·  <b>Canonical (⭐):</b> {canon_count}  ·  "
        f"<b>Top frameworks:</b> {fw_str}",
        styles["Body"]))
    flow.append(Spacer(1, 12))
    # List canonical skills
    flow.append(Paragraph("Canonical Artifacts", styles["H3"]))
    flow.append(Paragraph(
        f"Showing up to {max_skills} of {canon_count} canonical representatives. "
        f"See the digital package's <code>skills/{kingdom_key}/</code> directory for the full set, "
        f"including all variants.",
        styles["Body"]))
    flow.append(Spacer(1, 6))
    shown = canon[:max_skills]
    for i, f in enumerate(shown, 1):
        title = f.get("title", "(untitled)")[:80]
        meta = f"{f['framework']} · {f['source_repo']} · cluster size {f.get('cluster_size', 1)}"
        summary = f.get("summary", "(no summary available)")
        # escape HTML-unfriendly chars
        title_e = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        meta_e = meta.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        summary_e = summary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        block = [
            Paragraph(f"{i}. <b>{title_e}</b>", styles["SkillTitle"]),
            Paragraph(meta_e, styles["SkillMeta"]),
            Paragraph(summary_e, styles["SkillSummary"]),
        ]
        flow.append(KeepTogether(block))
    if canon_count > max_skills:
        flow.append(Spacer(1, 8))
        flow.append(Paragraph(
            f"<i>...and {canon_count - max_skills} more canonical artifacts. "
            f"See SKILL_INDEX.md or the Excel index for the full list.</i>",
            styles["Body"]))
    flow.append(PageBreak())
    return flow

def build_credits_section(styles, manifest, files):
    flow = []
    flow.append(Paragraph("Credits & Sources", styles["H1"]))
    flow.append(HRFlowable(width="100%", thickness=1, color=COLOR_GOLD,
                            spaceBefore=4, spaceAfter=12))
    flow.append(Paragraph(
        f"Every artifact in The Lord of the Skills was extracted from a public GitHub repository. "
        f"A total of <b>{manifest.get('total_cloned_repos', 0)}</b> repositories contributed to this "
        f"compilation. Each retains its original license; the compilation itself does not re-license "
        f"any artifact. The complete credits list is in <code>CREDITS.md</code> in the digital package.",
        styles["Body"]))
    # Top contributors table
    repo_counts = Counter(f["source_repo"] for f in files)
    flow.append(Paragraph("Top 20 Source Repositories by Artifact Count", styles["H3"]))
    header = [Paragraph(t, styles["TableHeader"]) for t in
              ["#", "Repository", "Artifacts", "Frameworks"]]
    rows = [header]
    repo_fws = defaultdict(set)
    for f in files:
        repo_fws[f["source_repo"]].add(f["framework"])
    for i, (repo, count) in enumerate(repo_counts.most_common(20), 1):
        rows.append([
            Paragraph(str(i), styles["TableCell"]),
            Paragraph(repo, styles["TableCell"]),
            Paragraph(str(count), styles["TableCell"]),
            Paragraph(", ".join(sorted(repo_fws[repo])), styles["TableCell"]),
        ])
    table = Table(rows, colWidths=[1 * cm, 6 * cm, 2.5 * cm, 6 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_DARK_BROWN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_LIGHT_GRAY, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.3, COLOR_MID_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    flow.append(table)
    flow.append(Spacer(1, 14))
    flow.append(Paragraph("How to Use This Compilation", styles["H2"]))
    flow.append(Paragraph(
        "The digital package at <code>/home/z/my-project/download/the-lord-of-the-skills/</code> "
        "contains the full set of artifacts, organized by kingdom → framework → source repository. "
        "Each artifact is a self-contained markdown file you can drop into your agent's skills or "
        "rules directory.",
        styles["Body"]))
    flow.append(Paragraph(
        "<b>For Claude Code:</b> Copy artifacts from <code>skills/&lt;kingdom&gt;/claude-code/</code> "
        "into your <code>~/.claude/skills/</code> directory.",
        styles["Body"]))
    flow.append(Paragraph(
        "<b>For Cursor:</b> Copy artifacts from <code>skills/&lt;kingdom&gt;/cursor/</code> into "
        "your project's <code>.cursor/rules/</code> directory.",
        styles["Body"]))
    flow.append(Paragraph(
        "<b>For Cline / Roo Code:</b> Copy from <code>skills/&lt;kingdom&gt;/cline/</code> or "
        "<code>skills/&lt;kingdom&gt;/roo/</code> into <code>.clinerules/</code> or "
        "<code>.roo/rules/</code> respectively.",
        styles["Body"]))
    flow.append(Paragraph(
        "<b>For canonical-only:</b> Files prefixed with <code>⭐_</code> are the canonical "
        "representative of each concept cluster. Use these for a curated, deduplicated set.",
        styles["Body"]))
    flow.append(Spacer(1, 10))
    flow.append(Paragraph(
        "<i>May your agents be wise, your prompts be sharp, and your skills be many.</i>",
        styles["Quote"]))
    return flow

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    if not IN_PATH.exists():
        print(f"ERROR: {IN_PATH} not found.")
        return
    manifest = json.loads(IN_PATH.read_text())
    files = manifest.get("files", [])
    print(f"Generating PDF catalog from {len(files)} files...")

    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2.2 * cm, bottomMargin=2 * cm,
        title="The Lord of the Skills",
        author="Z.ai",
        subject="Agentic AI skill compilation",
        creator="Z.ai",
    )

    flow = []
    # Cover (page 1) — drawn via onFirstPage
    flow.extend(build_cover_page(styles))
    # Manifesto (page 2+)
    flow.extend(build_manifesto(styles, manifest))
    # Map of kingdoms (page 3+)
    flow.extend(build_map_of_kingdoms(styles, files))
    # Per-kingdom sections
    for k in KINGDOM_ORDER:
        kingdom_files = [f for f in files if f["kingdom"] == k]
        if not kingdom_files:
            continue
        print(f"  kingdom {k}: {len(kingdom_files)} files")
        flow.extend(build_kingdom_section(styles, k, files, max_skills=30))
    # Credits
    flow.extend(build_credits_section(styles, manifest, files))

    print(f"Building PDF with {len(flow)} flowables...")
    doc.build(flow, onFirstPage=draw_cover, onLaterPages=draw_body_footer)
    print(f"\n✓ PDF catalog written: {OUT_PATH}")
    print(f"  Size: {OUT_PATH.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
