

# 🛡️ Fake News Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI](https://img.shields.io/badge/AI-Groq%20Llama%203.1-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen?logo=github)](https://mabbasrz.github.io/Fake-News-Detection-AI/)
[![Stars](https://img.shields.io/github/stars/Mabbasrz/Fake-News-Detection-AI?style=social)](https://github.com/Mabbasrz/Fake-News-Detection-AI/stargazers)
[![Issues](https://img.shields.io/github/issues/Mabbasrz/Fake-News-Detection-AI)](https://github.com/Mabbasrz/Fake-News-Detection-AI/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blueviolet)](https://github.com/Mabbasrz/Fake-News-Detection-AI/pulls)

> **Advanced Fake News Detection using AI + Machine Learning + Wikipedia Knowledge Base**

Created by **Muzammil Abbas**

---

## 🌟 Overview

A powerful, intelligent fake news detection system that combines multiple AI technologies to analyze and verify news articles with high accuracy. The system uses a hybrid approach combining Machine Learning models, Groq AI (Llama 3.1), and Wikipedia verification to provide reliable verdicts on news authenticity.

## ✨ Key Features

### 🤖 **Intelligent Detection System**
- **Hybrid AI Approach**: Combines 3 ML models (Logistic Regression, Random Forest, Gradient Boosting) with Groq AI
- **Smart Caching**: Stores AI analysis and replays exact reasoning for repeated texts (zero API cost on repeats)
- **Adaptive Processing**: Different strategies for short queries vs. long articles
- **Self-Learning**: Automatically trains on new data with high-confidence AI verdicts

### 🎯 **Advanced Analysis Pipeline**
1. **Short Text (< 200 chars)**: Direct AI verdict → Store → Replay on exact match
2. **Long Articles**: ML confidence gate → AI verification if needed → Wikipedia cross-reference
3. **Exact Match Replay**: Instant results using cached AI analysis (no re-processing)

### 🎨 **Modern User Interface**
- **Dark/Light Theme**: Beautiful toggle between neon-dark and clean-white themes
- **Split Panel Layout**: Detailed analysis on left, verdict summary on right
- **Real-time Progress**: Animated status updates during analysis
- **Verdict Box**: Large, color-coded verdict display with confidence metrics
- **One-Key Maximize**: Press 'F' to maximize window (one-way toggle)

### 📊 **Database Management**
- **Visual Database Viewer**: Treeview display of all analyzed texts
- **Right-Click Delete**: Easy deletion with confirmation dialogs
- **In-Place Refresh**: Updates without closing the viewer window
- **Persistent Storage**: JSON-based learning database

### 🌍 **Live Training Features**
- **Live News Training**: Fetch and train on real RSS feeds from BBC, CNN, Reuters
- **Mega Training**: Train on millions of samples from Kaggle datasets
- **Auto-Training**: Automatically adds high-confidence AI verdicts (>60%) to training data
- **Background Processing**: Non-blocking training with progress indicators

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **Internet connection** for API calls and Wikipedia lookups
- **Groq API Key** (free account)

### Installation Steps

#### 1️⃣ Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/github-fake-news-detection-by-Muzammil-Abbas.git
cd "github fake news detection by Muzammil Abbas"
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- `customtkinter` - Modern UI framework
- `scikit-learn` - Machine Learning models
- `nltk` - Natural Language Processing
- `requests` - API calls
- `beautifulsoup4` - Web scraping
- `feedparser` - RSS feed parsing
- `joblib` - Model persistence

#### 3️⃣ Get Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Create a free account (no credit card required)
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy your API key (starts with `gsk_...`)

#### 4️⃣ Configure API Key

Open `config.json` and replace `YOUR_GROQ_API_KEY_HERE` with your actual API key:

```json
{
    "groq_api_key": "gsk_YOUR_ACTUAL_KEY_HERE"
}
```

or when you start program it will ask api enter it in the box and ready 

#### 5️⃣ Run Application

**Quick Start (with loading bar):**
```bash
python start_app.py
```

**Direct Launch:**
```bash
python clean_app.py
```

## 🎮 Usage Guide

### Analyzing News

1. **Paste Text**: Copy any news article or claim into the input box
2. **Click Analyze**: Press "🔮 SCAN & ANALYZE" button
3. **View Results**: 
   - Left panel shows detailed AI reasoning, confidence, verdict, and sources
   - Right panel shows color-coded verdict (REAL/FAKE) with confidence bar

### Training Models

- **🧠 RETRAIN NEURAL**: Manually retrain on current learning database
- **🌍 TRAIN ON LIVE NEWS**: Fetch and train on latest news from major outlets
- **⚡ MEGA TRAIN**: Train on millions of samples from Kaggle datasets

### Managing Database

- **📊 VIEW DATABASE**: Opens database viewer
- **Right-click** any entry to delete (with confirmation)
- Database auto-saves all analyses for replay and training

### Theme Toggle

- Press **☀️ LIGHT** / **🌙 DARK** button to switch themes
- Press **F** key to maximize window

## 🧠 How It Works

### Detection Flow

```
Input Text
    ↓
Is text < 200 chars?
    ↓ YES → Check DB for exact match
    |         ↓ Found → Replay stored analysis (INSTANT)
    |         ↓ Not Found → Call Groq AI → Store & Display
    ↓ NO → Long Article Path
    |
    ↓ ML Model Analysis (3 models voting)
    ↓ Confidence > 75%?
        ↓ YES → Check for stored AI analysis
        |         ↓ Found → Replay (FAST MODE)
        |         ↓ Not Found → Continue to AI
        ↓ NO or No Cached Analysis
        |
        ↓ Groq AI Analysis (Llama 3.1-8b-instant)
        ↓ Wikipedia Cross-Reference
        ↓ Final Verdict + Detailed Reasoning
        ↓ Auto-Train if confidence > 60%
```

### AI Analysis Components

1. **Groq AI (Llama 3.1)**: Provides reasoning-based verdict with confidence
2. **Wikipedia Search**: Validates claims against factual knowledge base
3. **ML Ensemble**: TF-IDF features + 3 classifiers for pattern detection
4. **Smart Caching**: Exact-match storage prevents redundant API calls

### Learning System

- **Automatic**: High-confidence AI verdicts (>60%) added to database
- **Manual Training**: User can trigger retraining anytime
- **Live Updates**: Can train on breaking news from RSS feeds
- **Persistent**: All learned data saved in `learning_db.json`

## 📁 Project Structure

```
github fake news detection by Muzammil Abbas/
│
├── clean_app.py           # Main application (UI + ML + AI logic)
├── start_app.py           # Quick launcher with loading animation
├── config.json            # API key configuration
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── models/               # (Created on first run)
│   └── model.joblib      # Trained ML models
│
├── learning_db.json      # (Created on first use)
│                         # Stores analyzed texts + AI reasoning
│
└── history.json          # (Created on first use)
                          # Analysis history
```

## 🎨 Screenshots

Screenshots coming soon (UI preview and setup wizard will be added here.)

### Dark Theme
- Neon cyan/green accents
- High contrast for readability
- Professional hacker aesthetic

### Light Theme
- Clean white backgrounds
- Blue accents
- Easy on the eyes for daytime use

### Verdict Display
- **FAKE NEWS**: Red color coding with warning indicators
- **REAL NEWS**: Green color coding with checkmarks
- **Confidence Bar**: Visual progress indicator (0-100%)

## 🔧 Advanced Features

### Exact Match Caching
- Zero processing time for repeated texts
- Replays AI's exact original reasoning
- Uses stored verdict (not ML prediction)
- Saves API costs and time

### Short Query Optimization
- Queries under 200 characters always use AI first
- Better suited for claims, headlines, social media posts
- Trains ML models on these for future offline detection

### Background Processing
- Model training doesn't block UI
- Smooth animations during analysis
- Responsive interface at all times

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Muzammil Abbas**

- Created: November 2025
- Purpose: Combat misinformation with AI technology
- Technologies: Python, CustomTkinter, Scikit-learn, Groq AI, NLTK

## 🙏 Acknowledgments

- **Groq** for providing fast LLM inference API
- **Wikipedia** for knowledge verification
- **CustomTkinter** for modern UI framework
- **Scikit-learn** for ML capabilities
- **NLTK** for NLP preprocessing

## 🐛 Known Issues

- First-time model training may take 2-3 minutes
- Wikipedia API may have rate limits on heavy usage
- Groq API requires internet connection

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Chrome extension for instant page verification
- [ ] Fact-checking source citations
- [ ] Historical trend analysis
- [ ] Export analysis reports (PDF/HTML)
- [ ] Social media integration (Twitter, Facebook)
- [ ] Batch processing for multiple articles

## 📞 Support

If you encounter any issues:

1. Check `config.json` has valid Groq API key
2. Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. Verify Python 3.8+ is installed
4. Check internet connection for API/Wikipedia access

For bugs or questions, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please give it a star!**

**Made with ❤️ by Muzammil Abbas | Powered by AI**
