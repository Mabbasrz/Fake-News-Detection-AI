# 🔑 API Key Setup - Automatic First-Time Configuration

## What Happens on First Run?

When you run the application for the first time **WITHOUT** configuring the API key, the program will:

1. **Detect Missing API Key** - Automatically checks if `config.json` has a valid Groq API key
2. **Show Setup Dialog** - Opens a beautiful, user-friendly setup window
3. **Guide You Step-by-Step** - Provides clear instructions to get your FREE API key
4. **Open Groq Console** - Click button to open https://console.groq.com/ in your browser
5. **Wait for Your Input** - Program pauses and waits for you to paste your API key
6. **Validate & Save** - Checks the key format and saves it securely
7. **Start Application** - Once configured, the main app starts automatically

## 📋 Visual Setup Flow

```
🚀 Start Program
      ↓
🔍 Check config.json
      ↓
   API Key Found? ──YES──→ ✅ Start Application
      ↓ NO
      ↓
🔑 Show Setup Dialog
      ├─ "How to Get Your API Key" instructions
      ├─ Button: "Open Groq Console"  
      ├─ Input Box: "Paste Your API Key Here"
      └─ Button: "Save & Continue"
      ↓
👤 User Actions:
   1. Clicks "Open Groq Console" button
   2. Browser opens → console.groq.com
   3. Creates FREE account (no card needed)
   4. Generates API key in console
   5. Copies key (starts with gsk_)
   6. Pastes in input box
   7. Clicks "Save & Continue"
      ↓
✅ Key Validated & Saved
      ↓
✅ Application Starts!
```

## 🎨 Setup Dialog Features

### Beautiful UI
- **Dark Theme**: Professional appearance
- **Large Fonts**: Easy to read instructions
- **Color Coded**: Important steps highlighted
- **Icons**: Visual guidance (🔑, 📋, 🌐, ✅)

### Smart Validation
- ✅ Checks if key starts with `gsk_`
- ✅ Validates minimum length
- ✅ Shows warning for suspicious formats
- ✅ Saves only valid keys

### User-Friendly
- 📝 **Step-by-Step Instructions** - No confusion
- 🌐 **One-Click Browser Open** - Direct to Groq Console
- ⌨️ **Enter Key Support** - Press Enter to save
- 🎯 **Always on Top** - Won't lose the window
- ✨ **Auto-Focus** - Input box ready for paste

## 🚀 Quick Start (For First-Time Users)

### Option 1: Let the Program Guide You (RECOMMENDED)

```bash
# Just run the program!
python start_app.py
# or
python clean_app.py

# The setup dialog will appear automatically
# Follow the on-screen instructions
```

### Option 2: Manual Configuration

```bash
# 1. Get your API key from https://console.groq.com/
# 2. Edit config.json
{
    "groq_api_key": "gsk_YOUR_ACTUAL_KEY_HERE"
}
# 3. Save and run the program
python start_app.py
```

## 📖 Detailed Setup Instructions in Dialog

When the setup dialog appears, you'll see:

### Step 1-3: Account Setup
```
1️⃣  Click 'Open Groq Console' button below
2️⃣  Create a FREE account (no credit card required)
3️⃣  Log in to your account
```

### Step 4-6: Get API Key
```
4️⃣  Find 'API Keys' section in the left sidebar
5️⃣  Click 'Create API Key' button
6️⃣  Copy the generated key (starts with 'gsk_')
```

### Step 7: Configure & Start
```
7️⃣  Paste it in the box below and click 'Save & Continue'
```

## 🔐 Security Features

- ✅ **One-Time Setup** - Never asked again after first configuration
- ✅ **Local Storage** - Key saved in `config.json` on your computer
- ✅ **No Transmission** - Key never sent anywhere except Groq API
- ✅ **Validation** - Format checked before saving
- ✅ **User Control** - You can change it anytime by editing `config.json`

## 🎯 What If I Skip It?

If you close the setup dialog without entering a key:

- ❌ Application will exit gracefully
- 📝 You can run it again anytime
- 🔄 Setup dialog will appear again on next run
- ℹ️ No data is lost or damaged

## 🔄 Changing Your API Key Later

To change your API key after initial setup:

### Method 1: Delete config.json
```bash
# Delete the file
rm config.json   # Linux/Mac
del config.json  # Windows

# Run program again - setup dialog will appear
python clean_app.py
```

### Method 2: Edit config.json
```bash
# Open config.json in any text editor
# Replace the key
{
    "groq_api_key": "gsk_YOUR_NEW_KEY_HERE"
}
# Save and run program
```

## 🆘 Troubleshooting

### "Failed to save API key"
- **Cause**: File permission issue
- **Fix**: Run terminal as administrator
- **Alternative**: Manually create `config.json` with the key

### "API key format looks incorrect"
- **Cause**: Key doesn't start with `gsk_`
- **Fix**: Copy the key again from Groq Console
- **Note**: You can still continue if you're sure it's correct

### Setup dialog doesn't appear
- **Cause**: config.json already exists with valid key
- **Fix**: Either delete config.json or check if it has correct key
- **Verify**: Open config.json and check the key value

### "Cannot continue without API key"
- **Cause**: Setup was cancelled or failed
- **Fix**: Run the program again
- **Alternative**: Manually create config.json with your key

## 📞 Need Help?

If you encounter any issues:

1. Check this file: `README.md` - Complete documentation
2. Read: `SETUP_INSTRUCTIONS.md` - Detailed setup guide
3. Run: `python verify_setup.py` - Diagnose issues
4. Open GitHub Issue - Report bugs

## ✨ Benefits of This Approach

### For Users
- ✅ **No Manual Editing** - Everything done through UI
- ✅ **Clear Instructions** - Step-by-step guidance
- ✅ **One-Click Browser** - Direct to Groq Console
- ✅ **Visual Validation** - See if key is correct
- ✅ **Safe & Secure** - Key stored locally

### For Developers/Sharers
- ✅ **No Hardcoded Keys** - Your key stays private
- ✅ **GitHub Ready** - Safe to upload publicly
- ✅ **User-Friendly** - Non-technical users can set up
- ✅ **Professional** - Polished first-run experience
- ✅ **Maintainable** - Easy to update instructions

## 🎓 Technical Details

### Files Involved
- `setup_api_key.py` - Setup dialog code
- `clean_app.py` - Main app (calls setup if needed)
- `config.json` - Stores the API key
- `start_app.py` - Quick launcher (also checks)

### Setup Logic
```python
# Pseudo-code
if config.json exists:
    if api_key is valid:
        start_application()
    else:
        show_setup_dialog()
else:
    show_setup_dialog()
```

### Validation Rules
1. Key must not be empty
2. Key should start with `gsk_` (warning if not)
3. Key must be at least 20 characters long
4. Only valid keys are saved

---

**🛡️ Created by Muzammil Abbas | November 2025**

*Making setup as easy as 1-2-3* 🚀
