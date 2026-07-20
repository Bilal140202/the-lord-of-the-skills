# 🌐 The Lord of the Skills — Web UI

> Browse and search 17,000+ AI agent skills in your browser.

## 🚀 Run Locally

```bash
pip install -r web/requirements.txt
streamlit run web/app.py
```

The app opens at `http://localhost:8501`.


## 🌐 Live Demo

Browse the AI agent skills directly in your browser:

https://the-lord-of-the-skills.streamlit.app/


## ☁ Deploy

### Option 1: Streamlit Cloud (free, recommended)

1. Go to https://share.streamlit.io/
2. Connect your GitHub account
3. Select repo: `Bilal140202/the-lord-of-the-skills`
4. Set main file: `web/app.py`
5. Set requirements: `web/requirements.txt`
6. Deploy — you get a public URL like `https://lord-of-the-skills.streamlit.app/`

### Option 2: Hugging Face Spaces (free)

1. Go to https://huggingface.co/spaces
2. Create new Space → Streamlit
3. Upload `web/app.py` and `web/requirements.txt`
4. You get a public URL like `https://bilal140202-lotr-skills.hf.space/`

### Option 3: Local only

```bash
streamlit run web/app.py
```

## ✨ Features

- **Search** — keyword search across title, summary, tags
- **Filter** — by kingdom (11), framework (14), canonical ⭐
- **Preview** — view full skill content without leaving the browser
- **Kingdoms dashboard** — visual cards + bar chart per kingdom
- **Frameworks table** — coverage stats + detection patterns
- **Install command** — copy the exact `lotr install` command for any skill

## 🏗 Architecture

```
web/
├── app.py              ← Streamlit app (single file)
└── requirements.txt    ← streamlit + pandas + requests
```

The app fetches `skills/index.json` from GitHub raw (with 1-hour cache) and displays it interactively. No backend server needed — all data is client-side after the initial fetch.

## 📊 Data Source

The app reads from [`skills/index.json`](../skills/index.json) — a 7 MB manifest containing all 17,126 skills with titles, summaries, tags, kingdom, framework, and source repo.

