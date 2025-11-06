#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fast launcher for the Fake News Detector UI.
Skips package installation checks for instant startup on systems
where dependencies are already installed.
"""

import os
import runpy
import sys

# Move to project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Enable fast start
os.environ.setdefault("FAKE_NEWS_FAST_START", "1")

# Run the main app as __main__
APP_PATH = os.path.join(BASE_DIR, "clean_app.py")
if not os.path.exists(APP_PATH):
    print("clean_app.py not found next to start_app.py")
    sys.exit(1)

try:
    runpy.run_path(APP_PATH, run_name="__main__")
except ImportError as e:
    print("\n❌ Missing dependency:", e)
    print("Tip: Run clean_app.py once (without fast start) to auto-install packages,")
    print("or activate your venv and install requirements manually.")
    sys.exit(1)
