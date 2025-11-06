# 🛡️ Fake News Detection AI

A hybrid Machine Learning + Groq AI system to detect fake news with a beautiful desktop UI and smart caching.

- Repository: https://github.com/Mabbasrz/Fake-News-Detection-AI
- License: MIT

---

## 🚀 Quick Start

1) Clone or download the repository
2) Install requirements
3) First run will guide you to set the Groq API key automatically

```bash
# 1) (Optional) Create & activate a virtual environment
# python -m venv .venv
# .venv\\Scripts\\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Start the app (first run will show API Key wizard)
python start_app.py
```

Note: This is a desktop application built with CustomTkinter. It runs locally on your machine and does not execute inside the browser.

---

## ✨ Highlights

- Hybrid detection: ML models (LogReg, RandomForest, GradBoost) + Groq AI
- Automatic first-run setup for API key (no manual editing)
- Smart caching for repeated analyses (zero API cost on repeats)
- Auto-training on high-confidence results
- Dark/Light themes with modern UI

---

## 📸 Screens (Overview)

- First-run: API Key setup wizard with step-by-step guide
- Main UI: Split panels for input and results with confidence and AI analysis

---

## 📚 Documentation

- README, FEATURES, SETUP_INSTRUCTIONS included in the repo
- For detailed first-run flow: API_KEY_SETUP_GUIDE.md

---

## 🧰 Troubleshooting

- If the setup dialog doesn’t appear, ensure customtkinter is installed and try running `python setup_api_key.py`
- Ensure your API key starts with `gsk_`

---

Created by Muzammil Abbas (GitHub: @Mabbasrz)