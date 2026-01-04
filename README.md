# 🛡️ PushGuardian

> **Git Pre-Push Security & Best-Practice Analyzer powered by LangGraph**

PushGuardian automatically detects security risks, credential leaks, and architectural violations **before** you push to remote. Built with LangGraph for intelligent multi-step analysis.

## 🎯 Features

### Local Git Hook Protection
- ⚡ **Hard Abort Rules**: Instantly block commits with secrets (API keys, private keys, `.env` files)
- 🧠 **Soft LLM Checks**: AI-powered detection of DTO/Schema violations, dependency risks, permission changes
- 🔍 **Research Loop**: Auto-fetches principle + example links (Tavily → Serper fallback)
- 📝 **Markdown Reports**: Saved outside repo (survives `git reset`)
- 🤝 **Human-in-Loop**: Override with reason logging

### Web Demo
- 🌐 **FastAPI + Streamlit**: Upload diffs or paste text
- 📥 **Download Reports**: Get MD file with findings + learning links
- 🚀 **Deploy-Ready**: Railway (backend) + Streamlit Cloud (frontend)

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create conda environment
conda create -n p_guard python=3.10 -y
conda activate p_guard

# Install package in editable mode
pip install -e .
```

### 2. Configure API Keys

Create API key files in `C:\workplace\document\API\`:
- `openai.txt` - OpenAI API key
- `tavily.txt` - Tavily API key
- `serper.txt` - Serper API key (optional)

Or use `.env` file:
```bash
cp .env.example .env
# Edit .env with your keys
```

### 3. Install Git Hook

```bash
# In your target git repository
cd /path/to/your/project
conda activate p_guard
python -m pushguardian.install_hook
```

This installs a `pre-push` hook that runs PushGuardian before every `git push`.

### 4. Run Web Demo

**Option A: Streamlit (Recommended)**
```bash
streamlit run streamlit_app.py
```

**Option B: FastAPI**
```bash
uvicorn pushguardian.web:app --reload --port 8000
```

## 📁 Project Structure

```
pushguardian/
├── pushguardian/
│   ├── config.py           # YAML + API key loader
│   ├── git_ops.py          # Git diff extraction
│   ├── detectors/          # Hard rule detectors
│   │   ├── secrets.py
│   │   ├── files.py
│   │   └── stack_guess.py
│   ├── llm/                # LLM analysis
│   │   ├── judge.py        # Soft check judge
│   │   └── observe.py      # Evidence validator
│   ├── research/           # Web search
│   │   ├── tavily_client.py
│   │   ├── serper_client.py
│   │   └── gather.py
│   ├── report/             # Report generation
│   │   ├── models.py
│   │   └── writer.py
│   ├── graph.py            # LangGraph workflow ⭐
│   ├── cli.py              # Pre-push CLI
│   ├── install_hook.py     # Hook installer
│   └── web.py              # FastAPI server
├── .pushguardian/
│   └── config.yaml         # User configuration
├── examples/
│   └── sample_diff.txt     # Test diff
├── tests/                  # Unit tests
└── streamlit_app.py        # Streamlit frontend
```

## ⚙️ Configuration

Edit `.pushguardian/config.yaml`:

```yaml
# Report storage (outside repo)
report_dir: "%USERPROFILE%\\Documents\\PushGuardian\\reports"

# Your stack profile
stacks_known:
  - python
  - fastapi
stacks_weak:
  - react
  - kubernetes

# Hard abort patterns
hard_abort:
  file_patterns:
    - ".env"
    - "*.pem"
  secret_patterns:
    - "sk-"
    - "AKIA"
```

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Test with sample diff:
```bash
# Web mode
curl -X POST http://localhost:8000/analyze-diff \
  -F "diff_file=@examples/sample_diff.txt"
```

## 📊 LangGraph Workflow

```
load_config → scope_classify → hard_policy_check → soft_llm_judge
                                                          ↓
                                            [need research?]
                                                          ↓
                                                   research_tavily
                                                          ↓
                                               observation_validate
                                                          ↓
                                              [sufficient? or recheck?]
                                                    ↙         ↘
                                          write_report    research_serper
                                                ↓
                                          persist_report → END
```

## 🌐 Deployment

### Streamlit Cloud (Frontend)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy `streamlit_app.py`
4. Add secrets in Streamlit dashboard

### Railway (Backend - Optional)
1. Create `Procfile`: `web: uvicorn pushguardian.web:app --host 0.0.0.0 --port $PORT`
2. Push to GitHub
3. Connect to Railway
4. Add environment variables

## 🔒 Security Notes

- ⚠️ Hook can be bypassed with `git push --no-verify`
- 📂 Reports saved outside repo: `%USERPROFILE%\Documents\PushGuardian\`
- 🔐 Never commit `.env` or API keys

## 📚 Learn More

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Tavily API](https://tavily.com)
- [Git Hooks Guide](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

---

**Built with ❤️ using LangGraph, FastAPI, and Streamlit**
