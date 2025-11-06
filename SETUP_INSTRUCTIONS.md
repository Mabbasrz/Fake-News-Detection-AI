# 🚀 Complete Setup Instructions

## Step-by-Step Guide for First-Time Users

### ⚠️ IMPORTANT: You MUST complete these steps before running the application

---

## 📋 Prerequisites Check

Before starting, make sure you have:

- [ ] **Python 3.8 or higher** installed on your computer
- [ ] **pip** (Python package manager) installed
- [ ] **Internet connection** (required for initial setup)
- [ ] **10 minutes** of time for complete setup

### Check Python Installation

Open your terminal/command prompt and run:

```bash
python --version
```

You should see something like: `Python 3.8.x` or higher

If not installed, download from: https://www.python.org/downloads/

---

## 🔧 Installation Steps

### Step 1: Download the Project

**Option A - Using Git:**
```bash
git clone https://github.com/YOUR_USERNAME/github-fake-news-detection-by-Muzammil-Abbas.git
cd "github fake news detection by Muzammil Abbas"
```

**Option B - Download ZIP:**
1. Click green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file
4. Open terminal in the extracted folder

---

### Step 2: Install Required Packages

This will install all necessary Python libraries:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `customtkinter` - Modern GUI framework
- `scikit-learn` - Machine Learning models
- `nltk` - Text processing
- `requests` - API communication
- `beautifulsoup4` - Web scraping
- `feedparser` - RSS feed parsing
- `joblib` - Model saving/loading

⏱️ **This may take 2-5 minutes depending on your internet speed**

---

### Step 3: Get Your FREE Groq API Key

This is the **MOST IMPORTANT** step! The application cannot run without this.

#### 🔑 How to Get API Key:

1. **Visit Groq Console**
   - Go to: https://console.groq.com/
   - OR search "Groq API Console" in your browser

2. **Create Account** (100% FREE, no credit card needed)
   - Click "Sign Up" or "Get Started"
   - Use your email or Google account
   - Verify your email if required

3. **Generate API Key**
   - After logging in, find "API Keys" in the left sidebar
   - Click "Create API Key" button
   - Give it a name like "Fake News Detector"
   - Copy the generated key (starts with `gsk_`)

4. **IMPORTANT**: Save the key somewhere safe! You won't be able to see it again.

---

### Step 4: Configure the Application

1. **Open config.json file** in the project folder

2. **Replace the placeholder** with your actual API key:

   ```json
   {
       "groq_api_key": "gsk_YOUR_ACTUAL_KEY_HERE"
   }
   ```

   **Example (with fake key):**
   ```json
   {
       "groq_api_key": "gsk_abc123XYZ456definitelynotarealkey789"
   }
   ```

3. **Save the file** (Ctrl+S or Cmd+S)

---

### Step 5: Run the Application

You have two options:

#### Option A - Quick Start (Recommended)
```bash
python start_app.py
```
- Shows nice loading animation
- More polished startup experience

#### Option B - Direct Launch
```bash
python clean_app.py
```
- Starts immediately
- Good for quick testing

---

## ✅ Verify Installation

If everything is set up correctly, you should see:

1. ✅ Application window opens
2. ✅ No error messages about missing packages
3. ✅ UI loads with all buttons visible
4. ✅ Status shows "Ready for analysis"

### First-Time Training

⚠️ **On first launch**, the app will:
- Take 1-2 minutes to train initial ML models
- This happens in background (you can still use the app)
- Creates a `models/` folder with `model.joblib`
- You'll see this only once!

---

## 🎯 Quick Test

Try analyzing this sample text:

```
Scientists have discovered a new planet made entirely of chocolate in our solar system.
```

1. Paste the text in the input box
2. Click "🔮 SCAN & ANALYZE"
3. Wait 3-5 seconds
4. You should see verdict: **FAKE NEWS** (because it's obviously fake!)

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Problem: "Invalid API Key" or "Authentication Failed"

**Solution:**
1. Check `config.json` - make sure API key is correct
2. Verify no extra spaces before/after the key
3. Key should be inside quotes: `"gsk_..."`
4. Try generating a new API key from Groq Console

---

### Problem: Application window is blank/frozen

**Solution:**
1. Close the app completely
2. Delete the `models/` folder if it exists
3. Restart: `python clean_app.py`
4. Wait 2-3 minutes for initial model training

---

### Problem: "Connection Error" or "Network Error"

**Solution:**
1. Check your internet connection
2. Try again (API might be temporarily down)
3. Verify firewall isn't blocking Python
4. Check Groq service status: https://status.groq.com/

---

### Problem: Analysis takes too long (> 30 seconds)

**Solution:**
1. Check internet speed
2. Try with shorter text first
3. Verify API key is working (test with sample above)
4. Restart application

---

## 📁 File Structure After Setup

```
github fake news detection by Muzammil Abbas/
│
├── clean_app.py           ✅ Main app
├── start_app.py           ✅ Launcher
├── config.json            ✅ YOUR API KEY HERE
├── requirements.txt       ✅ Dependencies list
├── README.md             ✅ Documentation
├── SETUP_INSTRUCTIONS.md ✅ This file
│
├── models/                ⬅️ Created on first run
│   └── model.joblib       ⬅️ Trained ML models
│
├── learning_db.json       ⬅️ Created when you analyze first text
└── history.json           ⬅️ Created automatically
```

---

## 🎓 Usage Tips

### For Best Results:

1. **Short Claims**: Great for fact-checking headlines, tweets, rumors
2. **Long Articles**: Works best with 200+ character news articles
3. **Clear Text**: Avoid too much formatting or special characters
4. **Multiple Sources**: Cross-reference with other fact-checkers

### Features to Try:

- 🌙/☀️ **Theme Toggle**: Switch between dark/light mode
- **F Key**: Press to maximize window
- 📊 **Database Viewer**: See all previously analyzed texts
- 🌍 **Live Training**: Train on real news from BBC, CNN, Reuters
- **Right-click Delete**: Manage database entries

---

## 💡 Pro Tips

1. **First Analysis**: May take 5-10 seconds (fetching from AI)
2. **Repeated Text**: Instant results (uses cached analysis)
3. **Short Texts**: Always get fresh AI analysis
4. **Training**: Do "MEGA TRAIN" once for better accuracy
5. **Database**: Grows smarter with each analysis

---

## 🆘 Still Having Issues?

1. **Read error messages carefully** - they usually tell you what's wrong
2. **Check all steps above** - most issues are from skipped steps
3. **Verify Python version** - must be 3.8 or higher
4. **Try with sample text** - rules out API/network issues
5. **Open GitHub issue** - describe your problem with error messages

---

## 📞 Support Channels

- **GitHub Issues**: Best for bug reports
- **Email**: Include error screenshots
- **Documentation**: Check README.md for features

---

## ✨ You're All Set!

Once you see the application running, you're ready to:

- ✅ Analyze news articles
- ✅ Detect fake news claims
- ✅ Train custom models
- ✅ Build your learning database
- ✅ Fight misinformation!

**Happy fact-checking! 🛡️**

---

**Created by Muzammil Abbas | November 2025**
