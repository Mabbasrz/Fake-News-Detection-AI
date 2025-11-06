"""
🔍 Setup Verification Script
Checks if everything is configured correctly before running the app.
"""

import sys
import os

def print_status(message, status):
    """Print colored status message"""
    if status == "OK":
        print(f"✅ {message}")
        return True
    elif status == "ERROR":
        print(f"❌ {message}")
        return False
    else:
        print(f"⚠️  {message}")
        return None

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} detected", "OK")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor} is too old. Need 3.8+", "ERROR")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    required = [
        'customtkinter',
        'sklearn',
        'nltk',
        'requests',
        'bs4',
        'feedparser',
        'joblib'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if not missing:
        print_status("All dependencies installed", "OK")
        return True
    else:
        print_status(f"Missing packages: {', '.join(missing)}", "ERROR")
        print("   Run: pip install -r requirements.txt")
        return False

def check_config():
    """Check if config.json exists and has API key"""
    if not os.path.exists('config.json'):
        print_status("config.json not found", "ERROR")
        return False
    
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        api_key = config.get('groq_api_key', '')
        
        if not api_key or api_key == "YOUR_GROQ_API_KEY_HERE":
            print_status("API key not configured in config.json", "ERROR")
            print("   Get your free API key from: https://console.groq.com/")
            return False
        elif not api_key.startswith('gsk_'):
            print_status("API key format looks incorrect (should start with 'gsk_')", "ERROR")
            return False
        else:
            print_status(f"API key configured (starts with {api_key[:8]}...)", "OK")
            return True
            
    except Exception as e:
        print_status(f"Error reading config.json: {e}", "ERROR")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        'clean_app.py',
        'start_app.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            pass  # Silent success
        else:
            print_status(f"Missing file: {file}", "ERROR")
            all_exist = False
    
    if all_exist:
        print_status("All required files present", "OK")
    return all_exist

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🛡️  FAKE NEWS DETECTION - SETUP VERIFICATION")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_files),
        ("Dependencies", check_dependencies),
        ("API Configuration", check_config)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ ALL CHECKS PASSED!")
        print("\n🚀 You're ready to run the application:")
        print("   python start_app.py")
        print("   OR")
        print("   python clean_app.py")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("\n⚠️  Please fix the errors above before running the app.")
        print("\n📖 See SETUP_INSTRUCTIONS.md for detailed help")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print("\n" + "=" * 60)
    sys.exit(exit_code)
