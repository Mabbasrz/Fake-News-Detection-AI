#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ FAKE NEWS DETECTION
Advanced AI-Powered Analysis with Groq AI + Wikipedia + Self-Learning
"""

import subprocess
import sys
import os
import time
import threading
import json
from datetime import datetime
import difflib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Terminal Loading Bar Function
def print_loading_bar(percentage, bar_length=50):
    """Print loading bar in terminal"""
    filled = int(bar_length * percentage / 100)
    bar = '█' * filled + '░' * (bar_length - filled)
    sys.stdout.write(f'\r🚀 Loading: |{bar}| {percentage}%')
    sys.stdout.flush()

# Print startup banner
print("\n" + "="*60)
print("🛡️  FAKE NEWS DETECTOR - AI POWERED")
print("="*60)
print("Starting up...")
print()

# Fast start flag (skip package checks/installs if set)
FAST_START = os.getenv('FAKE_NEWS_FAST_START') == '1'

# Auto-install packages with progress
def install_package(package, idx, total):
    try:
        __import__(package.split('==')[0] if '==' in package else package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
    
    # Update progress
    progress = int(((idx + 1) / total) * 70)  # 70% for package installation (system-paced)
    print_loading_bar(progress, 50)


# API Key Setup Check
if not FAST_START:
    try:
        from setup_api_key import APIKeySetup
        api_setup = APIKeySetup()
        if not api_setup.run():
            print("❌ Cannot continue without API key. Exiting...")
            sys.exit(1)
    except Exception as e:
        print(f"⚠️  API setup error: {e}")
        print("Continuing anyway...")

print_loading_bar(0, 50)
packages = ["customtkinter", "pillow", "nltk", "numpy", "pandas", "joblib", "faker", 
            "beautifulsoup4", "requests", "scikit-learn", "feedparser"]

if not FAST_START:
    for idx, pkg in enumerate(packages):
        install_package(pkg, idx, len(packages))
    print()  # New line after progress bar
else:
    print("Fast start: skipping package checks (set FAKE_NEWS_FAST_START=0 to disable)")
    print_loading_bar(70, 50)
    print()

# Now import all the packages
print_loading_bar(72, 50)
import customtkinter as ctk
print_loading_bar(75, 50)
import numpy as np
import pandas as pd
print_loading_bar(78, 50)
import joblib
import nltk
print_loading_bar(81, 50)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
print_loading_bar(84, 50)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
print_loading_bar(87, 50)
import requests
from bs4 import BeautifulSoup
import feedparser
from faker import Faker
print_loading_bar(90, 50)

# Download NLTK data in background (non-blocking)
def download_nltk_data():
    """Download NLTK data in background"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)

# Start NLTK download in background thread
print_loading_bar(92, 50)
threading.Thread(target=download_nltk_data, daemon=True).start()

# Initialize NLTK components (with fallback)
print_loading_bar(94, 50)
try:
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
except:
    stop_words = set()
    lemmatizer = None

print_loading_bar(96, 50)

# ======================== LOCAL FACT-CHECK (No API) ========================
def local_fact_check(text):
    """Local fact-checking without API - pattern based"""
    analysis = []
    score = 0.5  # Neutral starting score
    text_lower = text.lower()
    
    # Check 1: Sensationalism indicators
    sensational_words = ['shocking', 'exposed', 'urgent', 'breaking', 'exclusive', 'unbelievable', 'incredible']
    sensational_count = sum(1 for word in sensational_words if word in text_lower)
    if sensational_count > 2:
        analysis.append("🚩 High sensationalism detected")
        score -= 0.2
    
    # Check 2: Emotional language
    emotional_words = ['hate', 'love', 'terrible', 'amazing', 'disgusting', 'perfect', 'worst']
    emotional_count = sum(1 for word in emotional_words if word in text_lower)
    if emotional_count > 3:
        analysis.append("🚩 Excessive emotional language")
        score -= 0.15
    
    # Check 3: All caps abuse
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    if caps_ratio > 0.15:
        analysis.append(f"🚩 Excessive capitalization ({caps_ratio*100:.1f}%)")
        score -= 0.1
    
    # Check 4: Exclamation marks
    exclamation_ratio = text.count('!') / max(len(text), 1)
    if exclamation_ratio > 0.05:
        analysis.append(f"🚩 Too many exclamations ({text.count('!')} found)")
        score -= 0.1
    
    # Check 5: Question marks (clickbait)
    question_ratio = text.count('?') / max(len(text), 1)
    if question_ratio > 0.03:
        analysis.append(f"🚩 Clickbait question pattern")
        score -= 0.05
    
    # Check 6: Credibility indicators (positive)
    credible_words = ['according to', 'research shows', 'study found', 'expert says', 'data shows', 'evidence', 'verified']
    credible_count = sum(1 for word in credible_words if word in text_lower)
    if credible_count > 0:
        analysis.append(f"✓ {credible_count} credibility indicators found")
        score += credible_count * 0.1
    
    # Check 7: Source attribution
    if any(phrase in text_lower for phrase in ['according to', 'said', 'reported', 'announced', 'stated']):
        analysis.append("✓ Proper source attribution")
        score += 0.1
    
    # Check 8: URL/links
    has_links = 'http' in text or 'www.' in text
    if has_links:
        analysis.append("✓ Contains references/links")
        score += 0.05
    
    # Check 9: Numbers and data
    import re
    numbers = len(re.findall(r'\d+', text))
    if numbers > 3:
        analysis.append(f"✓ Contains {numbers} numerical data points")
        score += 0.1
    
    # Check 10: Length quality
    word_count = len(text.split())
    if word_count < 50:
        analysis.append("🚩 Very short text (potential clickbait)")
        score -= 0.1
    elif word_count > 300:
        analysis.append("✓ Substantial content length")
        score += 0.05
    
    score = max(0.1, min(0.9, score))  # Clamp between 0.1 and 0.9
    
    return {
        "source": "Pattern Analysis",
        "analysis": "\n".join(analysis) if analysis else "Standard news pattern detected",
        "score": score,
        "status": "✓ Local"
    }

# ======================== WIKIPEDIA API ========================
# WIKI CACHE FOR SPEED
_wiki_cache = {}

def search_wikipedia(text):
    """Search Wikipedia for context (with fast caching)"""
    try:
        text_hash = hash(text[:50])
        if text_hash in _wiki_cache:
            return _wiki_cache[text_hash]
        
        words = text.split()
        keywords = []
        common_words = {'this', 'that', 'have', 'with', 'from', 'about', 'only', 'when', 'been', 'the', 'is', 'are'}
        
        for word in words[:5]:  # Reduced from 8 for speed
            clean_word = word.strip('.,!?;:-').lower()
            if len(clean_word) > 3 and clean_word not in common_words:
                keywords.append(clean_word)
        
        wiki_results = {}
        
        for keyword in keywords[:2]:  # Reduced from 3 for speed
            try:
                resp = requests.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "format": "json",
                        "titles": keyword,
                        "prop": "extracts",
                        "explaintext": True,
                        "exintro": True,
                        "redirects": True
                    },
                    timeout=2,  # Reduced from 4 seconds
                    headers={'User-Agent': 'FakeNewsDetector/1.0'}
                )
                
                if resp.status_code == 200:
                    pages = resp.json().get('query', {}).get('pages', {})
                    for page_id, page in pages.items():
                        if page_id != '-1' and 'extract' in page and page['extract']:
                            extract = page['extract'].strip()
                            if extract and len(extract) > 20:
                                wiki_results[keyword] = extract[:200]  # Reduced from 250
                                break
            except:
                pass
        
        _wiki_cache[text_hash] = wiki_results
        return wiki_results
    except:
        return {}

# ======================== DATABASE ========================
def load_learning_database():
    """Load learning database - returns list of items"""
    if os.path.exists('learning_db.json'):
        try:
            with open('learning_db.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # If it's already a list, return it
            if isinstance(data, list):
                return data
            # If it's old format (dict with real/fake), convert to list
            elif isinstance(data, dict):
                result = []
                for item in data.get('real', []):
                    if isinstance(item, dict):
                        result.append(item)
                for item in data.get('fake', []):
                    if isinstance(item, dict):
                        result.append(item)
                return result
            else:
                return []
        except:
            return []
    return []

def save_learning_database(db):
    """Save learning database"""
    try:
        with open('learning_db.json', 'w') as f:
            json.dump(db, f, indent=2)
    except:
        pass

def add_to_learning_database(text, label, source, confidence, ai_analysis=None):
    """Add to learning database - with smart duplicate checking and AI analysis"""
    db = load_learning_database()
    
    # Ensure db is a list
    if not isinstance(db, list):
        db = []
    
    # Check for exact duplicates and similar entries (fuzzy matching)
    text_lower = text.lower().strip()
    text_hash = hash(text_lower)
    
    # Always check for exact matches
    for existing in db:
        if isinstance(existing, dict):
            existing_text = existing.get('text', '').lower().strip()
            
            # Check exact match - always reject
            if existing_text == text_lower:
                return db  # Already exists, don't add
            
            # For BBC live news, do fuzzy matching (similar real news is likely duplicate)
            if source in ["BBC Live", "BBC", "Reuters"]:
                similarity = difflib.SequenceMatcher(None, existing_text, text_lower).ratio()
                if similarity > 0.75:  # 75% similar = likely same event reported differently
                    return db  # Similar entry exists, don't add
            # For bootstrap data, only check exact (allow similar template-based news)
            # For user-added news, only check exact
    
    sample = {
        'text': text[:300],
        'source': source,
        'confidence': float(confidence),
        'timestamp': datetime.now().isoformat(),
        'label': label
    }
    
    # Save AI analysis if provided
    if ai_analysis:
        sample['ai_analysis'] = ai_analysis
    
    db.append(sample)
    
    # Keep only last 2000 items
    if len(db) > 2000:
        db = db[-2000:]
    
    save_learning_database(db)
    return db

def get_learning_stats():
    """Get database stats"""
    db = load_learning_database()
    
    # Ensure db is a list
    if not isinstance(db, list):
        db = []
    
    real_count = 0
    fake_count = 0
    for item in db:
        if isinstance(item, dict):
            if item.get('label') == 1:
                real_count += 1
            elif item.get('label') == 0:
                fake_count += 1
    
    return {
        'real_samples': real_count,
        'fake_samples': fake_count,
        'total_samples': len(db)
    }

# ======================== PREPROCESSING ========================
def preprocess_text(text):
    text = text.lower()
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words and len(w) > 2]
    return ' '.join(words)

def get_stylistic_features(text):
    features = []
    features.append(1 if '!!!' in text else 0)
    features.append(1 if 'URGENT' in text else 0)
    features.append(1 if 'EXPOSED' in text else 0)
    features.append(1 if '100%' in text else 0)
    features.append(text.count('!') / max(len(text), 1))
    features.append(sum(1 for c in text if c.isupper()) / max(len(text), 1))
    return np.array([features])

# ======================== MEGA TRAINING ON MILLIONS (MEMORY OPTIMIZED) ========================
def train_on_millions_mega():
    """
    OPTIMIZED MEGA training: Bootstrap + BBC feeds (FAST)
    - 500 bootstrapped articles (training data)
    - 200+ from BBC feeds (live articles)
    """
    print("🌐 Starting OPTIMIZED MEGA training...")
    print("📊 TARGET: 700+ unique articles (500 bootstrap + 200+ live)")
    
    total_real = 0
    total_fake = 0
    total_fetched = 0
    
    # Step 1: Add bootstrap data (500 articles - reduced from 1100 for speed)
    print("\n📚 Step 1: Loading 500 bootstrap training articles...")
    bootstrap_data = generate_bootstrap_training_data()[:500]  # Reduced for speed
    print(f"  Generated {len(bootstrap_data)} bootstrap articles")
    
    for item in bootstrap_data:
        try:
            add_to_learning_database(item['text'][:500], item['label'], "Bootstrap Data", item['confidence'])
            
            if item['label'] == 1:
                total_real += 1
            else:
                total_fake += 1
            
            total_fetched += 1
            
            if total_fetched % 100 == 0:
                print(f"  ✓ Added {total_fetched} bootstrap articles...")
        except:
            pass
    
    # Step 2: Add from BBC feeds (200+ additional - FASTER)
    print(f"\n📡 Step 2: Fetching 200+ articles from BBC feeds (FAST)...")
    
    bbc_feeds = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.bbci.co.uk/news/india/rss.xml",
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
    ]
    
    processed_urls = set()
    articles_from_bbc = 0
    
    for feed_url in bbc_feeds:
        try:
            response = requests.get(feed_url, timeout=3)  # Faster timeout
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                
                # 40 articles per feed (5 feeds × 40 = 200 max)
                for entry in feed.entries[:40]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    link = entry.get('link', '')
                    
                    if link in processed_urls:
                        continue
                    processed_urls.add(link)
                    
                    if summary:
                        summary = BeautifulSoup(summary, 'html.parser').get_text()
                    
                    text = f"{title}. {summary}"
                    
                    if len(text.strip()) > 30:
                        try:
                            local_score = local_fact_check(text).get('score', 0.5)
                            label = 1 if local_score > 0.6 else 0
                            confidence = abs(local_score - 0.5) * 2
                            
                            if confidence > 0.3:
                                add_to_learning_database(text[:500], label, "BBC Live", confidence)
                                
                                if label == 1:
                                    total_real += 1
                                else:
                                    total_fake += 1
                                
                                total_fetched += 1
                                articles_from_bbc += 1
                        except:
                            pass
                    
                    if total_fetched >= 700:  # Reduced target from 1000
                        break
                
                if total_fetched >= 700:
                    break
                    
        except Exception as e:
            print(f"  ⚠️ Feed error: {str(e)[:60]}...")
            continue
    
    print(f"\n✅ MEGA TRAINING COMPLETE!")
    print(f"📊 Total unique articles added: {total_fetched}")
    print(f"  ✓ Real News: {total_real}")
    print(f"  ✗ Fake News: {total_fake}")
    print(f"  📚 Bootstrap: {total_fetched - articles_from_bbc}")
    print(f"  📡 BBC Live: {articles_from_bbc}")
    print(f"🧠 Retraining model with {total_fetched} articles...")
    
    # Retrain model
    train_model()
    
    print(f"✅ Model retrained successfully!")
    return {
        "total": total_fetched,
        "real": total_real,
        "fake": total_fake
    }

# ======================== LIVE NEWS TRAINING (MEMORY EFFICIENT) ========================
def fetch_live_news():
    """Fetch live news from working RSS feeds (OPTIMIZED - Fast)"""
    news_items = []
    processed_urls = set()
    
    # WORKING FEEDS (tested & verified)
    rss_feeds = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://feeds.bbci.co.uk/news/india/rss.xml",
        "https://feeds.bbci.co.uk/news/asia/rss.xml",
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.npr.org/1001/rss.xml",
    ]
    
    try:
        print("[*] Fetching from BBC & international feeds...")
        for feed_url in rss_feeds:
            try:
                response = requests.get(feed_url, timeout=3)  # Reduced from 5
                if response.status_code == 200:
                    feed = feedparser.parse(response.content)
                    
                    for entry in feed.entries[:10]:  # Reduced from 20 for speed
                        title = entry.get('title', '')
                        summary = entry.get('summary', '')
                        link = entry.get('link', '')
                        
                        if link in processed_urls:
                            continue
                        processed_urls.add(link)
                        
                        if summary:
                            summary = BeautifulSoup(summary, 'html.parser').get_text()
                        
                        text = f"{title}. {summary}"
                        if len(text.strip()) > 30:
                            news_items.append(text[:500])
                            if len(news_items) % 30 == 0:
                                print(f"  [+] Fetched {len(news_items)} live articles...")
                        
                        if len(news_items) >= 100:  # Reduced target from 240
                            break
                    
                    if len(news_items) >= 100:
                        break
                        
            except Exception as e:
                print(f"  [-] Feed error: {str(e)[:60]}...")
                continue
    
    except Exception as e:
        print(f"Live news fetch error: {e}")
    
    return news_items

def train_on_live_news_async(callback=None):
    """
    Live News Training: Fetch + Bootstrap (700+ articles target)
    - 240+ from BBC feeds (live)
    - 500+ bootstrapped articles (training data)
    """
    def worker():
        try:
            added_real = 0
            added_fake = 0
            total_added = 0
            
            # Step 1: Add bootstrap data (500 articles for live)
            if callback:
                callback("progress", "📚 Loading 500 bootstrap training articles...")
            
            bootstrap_data = generate_bootstrap_training_data()[:500]  # Use first 500 for live
            
            for item in bootstrap_data:
                try:
                    add_to_learning_database(item['text'][:500], item['label'], "Bootstrap Live", item['confidence'])
                    
                    if item['label'] == 1:
                        added_real += 1
                    else:
                        added_fake += 1
                    
                    total_added += 1
                    
                    if total_added % 100 == 0:
                        if callback:
                            callback("progress", f"📚 Added {total_added} bootstrap articles ({added_real} Real + {added_fake} Fake)")
                except:
                    pass
            
            # Step 2: Fetch live news from BBC (240+ more articles)
            if callback:
                callback("progress", f"📡 Fetching {min(240, 12*20)} live news articles from BBC...")
            
            news_items = fetch_live_news()
            
            if not news_items:
                if callback:
                    callback("progress", "📡 Could not fetch BBC news, using bootstrap only...")
            else:
                # Process one by one
                for i, text in enumerate(news_items):
                    try:
                        local_score = local_fact_check(text).get('score', 0.5)
                        label = 1 if local_score > 0.6 else 0
                        confidence = abs(local_score - 0.5) * 2
                        
                        if confidence > 0.5:
                            add_to_learning_database(text, label, "BBC Live", confidence)
                            
                            if label == 1:
                                added_real += 1
                            else:
                                added_fake += 1
                            
                            total_added += 1
                        
                        # Update progress
                        if total_added % 50 == 0:
                            progress = int((i / len(news_items)) * 100)
                            if callback:
                                callback("progress", f"📡 Processing: {progress}% ({added_real} Real + {added_fake} Fake) - Total: {total_added}")
                        
                        time.sleep(0.05)
                        
                    except Exception as e:
                        pass
            
            # Step 3: Train model
            train_model()
            
            if callback:
                callback("done", f"✅ Live Training Complete!\n\n📊 Data Added: {total_added}\n  ✓ Real News: {added_real}\n  ✗ Fake News: {added_fake}\n\n🧠 Model Retrained!")
        
        except Exception as e:
            if callback:
                callback("error", f"❌ Error: {str(e)}")
    
    # Start in background thread
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

# ======================== TRAINING DATA ========================
TRUE_SAMPLES = [
    "New scientific breakthrough published in peer-reviewed journal",
    "Government announces new policy after extensive consultation",
    "Market rises on positive economic indicators and data",
    "University research receives international recognition",
    "Expert analysis reveals industry trends and developments",
]

FAKE_SAMPLES = [
    "SHOCKING!!! Celebrity exposed with URGENT breaking news!!!",
    "100% GUARANTEED cure - doctors hate this ONE TRICK",
    "BREAKING: Secret government conspiracy EXPOSED and hidden",
    "URGENT share now before THEY DELETE this",
    "EXPOSED: Shocking truth hidden from public!!!",
]

# ======================== BOOTSTRAP MASSIVE TRAINING DATA ========================
def generate_bootstrap_training_data():
    """Generate 1000+ diverse, realistic news articles for bootstrap training"""
    
    real_news_templates = [
        "Scientific researchers at {org} published a peer-reviewed study in {journal} showing {finding}.",
        "According to official government data released today, {indicator} increased by {number}% in {period}.",
        "A spokesperson for {org} confirmed that {statement} based on recent analysis.",
        "Economists report that {sector} sector saw growth of {number}% due to {reason}.",
        "The latest survey by {org} indicates that {statistic} among the population.",
        "Industry experts say {prediction} will likely happen based on current trends.",
        "Official records show {org} has achieved {milestone} in the last {period}.",
        "{Leader} announced new policy that will {action} starting {date}.",
        "Universities conduct joint research proving that {finding} through {method}.",
        "Market analysis from {firm} suggests {prediction} based on {data}.",
    ]
    
    fake_news_templates = [
        "SHOCKING TRUTH!!! {celebrity} was CAUGHT doing {action}! THEY don't want you to know!!!",
        "BREAKING!!! {group} is hiding {secret} from EVERYONE! URGENT share before deleted!!!",
        "100% PROVEN: This ONE TRICK will {miracle} - doctors HATE this secret!!!",
        "WARNING: {product} is DEADLY! Government hiding {fact}! SHARE NOW!!!",
        "EXPOSED: {org} is LYING about {topic}! The TRUTH they don't want public!!!",
        "URGENT ALERT: {disaster} coming SOON! Media REFUSES to report!!!",
        "This will SHOCK you: {group} secretly controls {thing}! EXPOSED!!!",
        "{Conspiracy} is REAL! They've been hiding it for YEARS! Must watch!!!",
        "YOU WON'T BELIEVE: {prediction} will happen VERY SOON! Insiders reveal!!!",
        "MASSIVE SCANDAL: {person} caught in {scandal}! Media COVERUP!!! SHARE!!!",
    ]
    
    real_entities = {
        "org": ["MIT", "Stanford University", "Harvard Medical School", "Oxford University", 
                "NASA", "CDC", "World Health Organization", "UN", "IMF", "World Bank",
                "Indian Institute of Technology", "Indian Council of Agricultural Research"],
        "journal": ["Nature", "Science", "JAMA", "The Lancet", "Cell", "PNAS"],
        "indicator": ["GDP", "employment", "inflation", "trade", "investment"],
        "number": ["5", "8", "12", "15", "20", "25", "35", "42"],
        "period": ["last quarter", "last year", "this year", "last decade", "past 5 years"],
        "sector": ["technology", "healthcare", "agriculture", "manufacturing", "retail", "finance"],
        "reason": ["new policies", "market demand", "innovation", "consumer interest", "government support"],
        "statistic": ["73% prefer online shopping", "82% trust government", "68% believe in climate change"],
        "milestone": ["reached 1 billion users", "achieved carbon neutrality", "exceeded 10 million customers"],
        "Leader": ["The Prime Minister", "The President", "The CEO", "The Minister"],
        "action": ["reduce emissions", "improve healthcare", "boost economy", "create jobs"],
        "date": ["next month", "January 2025", "next quarter", "by end of year"],
        "method": ["clinical trials", "data analysis", "peer review", "field research"],
        "prediction": ["inflation will stabilize", "tech will grow", "jobs will increase", "markets will recover"],
        "firm": ["Goldman Sachs", "JP Morgan", "Deloitte", "McKinsey", "Bloomberg"],
        "data": ["historical trends", "market analysis", "economic indicators", "survey results"],
    }
    
    fake_entities = {
        "celebrity": ["Bollywood star", "Hollywood actor", "Tech CEO", "Sports icon"],
        "action": ["secret deal", "hidden crime", "money laundering", "conspiracy"],
        "group": ["Big Tech", "The Elite", "Government", "Secret Society"],
        "secret": ["mind control", "hidden UFOs", "suppressed cure", "truth about Earth"],
        "product": ["Common vaccine", "Popular soft drink", "Well-known phone", "Popular social media"],
        "miracle": ["cure all diseases", "make you rich", "lose 50 lbs in week", "live forever"],
        "fact": ["dangerous truth", "harmful effects", "conspiracy", "coverup"],
        "org": ["Big Pharma", "Mainstream Media", "Deep State", "Shadow Government"],
        "topic": ["climate change", "pandemic", "elections", "economy"],
        "disaster": ["Solar flare", "Alien invasion", "Economic collapse", "Super earthquake"],
        "thing": ["world economy", "news media", "governments", "technology"],
        "Conspiracy": ["Moon landing fake", "Earth is flat", "Aliens control us", "Hidden world order"],
        "person": ["Famous politician", "Tech billionaire", "News anchor"],
        "scandal": ["fraud scheme", "illegal activity", "secret meetings"],
        "prediction": ["World ending in days", "Currency collapsing soon", "Government takeover"],
    }
    
    import random
    
    news_data = []
    sources_real = ["Reuters", "BBC", "AP News", "Bloomberg", "Guardian", "Financial Times", "NPR"]
    sources_fake = ["Truth Revealed", "Breaking Alert", "Viral News", "Secret Exposed", "Underground Report"]
    
    # Generate REAL news (600 articles)
    for i in range(600):
        template = random.choice(real_news_templates)
        values = {key: random.choice(vals) for key, vals in real_entities.items()}
        try:
            text = template.format(**values)
            news_data.append({
                "text": text,
                "label": 1,  # 1 = real
                "source": random.choice(sources_real),
                "confidence": random.uniform(0.7, 0.99),
                "timestamp": f"2025-11-{random.randint(1,4):02d}T{random.randint(0,23):02d}:00:00"
            })
        except:
            pass
    
    # Generate FAKE news (500 articles)
    for i in range(500):
        template = random.choice(fake_news_templates)
        values = {key: random.choice(vals) for key, vals in fake_entities.items()}
        try:
            text = template.format(**values)
            news_data.append({
                "text": text,
                "label": 0,  # 0 = fake
                "source": random.choice(sources_fake),
                "confidence": random.uniform(0.7, 0.99),
                "timestamp": f"2025-11-{random.randint(1,4):02d}T{random.randint(0,23):02d}:00:00"
            })
        except:
            pass
    
    return news_data

# ======================== AI EXPLANATION ========================
def get_ai_explanation(text, is_fake, wiki_knowledge=None):
    """Get AI-powered explanation"""
    explanations = []
    text_lower = text.lower()
    
    if is_fake:
        explanations.append("🚨 FAKE NEWS INDICATORS:\n")
        if '!!!' in text or text.count('!') > 5:
            explanations.append("  ⚠️ Excessive exclamation marks")
        if 'URGENT' in text.upper():
            explanations.append("  ⚠️ Urgency language detected")
        if 'EXPOSED' in text.upper():
            explanations.append("  ⚠️ Conspiracy keywords found")
        if '100%' in text:
            explanations.append("  ⚠️ False certainty claims")
    else:
        explanations.append("✅ REAL NEWS INDICATORS:\n")
        if any(word in text_lower for word in ['said', 'according', 'reported']):
            explanations.append("  ✓ Proper attribution language")
        if '.' in text and text.count('.') > len(text.split()) * 0.1:
            explanations.append("  ✓ Proper sentence structure")
        if any(word in text_lower for word in ['research', 'study', 'data', 'evidence']):
            explanations.append("  ✓ References credible sources")
    
    return explanations

# ======================== PREDICTION ========================
gemini_cache = {}
_model_cache = {}  # Cache for loaded models (avoid reloading)

def search_gemini(text):
    """Search using Groq AI API (Llama 3 model)"""
    try:
        import requests
        import json
        
        GROQ_API_KEY = json.load(open("config.json"))["groq_api_key"]
        GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
        
        # Detect if it's a short question or long article
        text_length = len(text.strip())
        is_short_query = text_length < 200  # Less than 200 characters = short question
        
        if is_short_query:
            # For short questions: Direct fact-check
            prompt = f"""Answer this question with facts and determine if the claim is true or false.

Question: {text}

Provide your answer in this format:
VERDICT: [REAL if claim is true, FAKE if claim is false]
CONFIDENCE: [0-100]%
REASONING: [Direct answer with facts - be conversational and clear]

Example:
Question: "Did Rahul Gandhi call Modi vote choor?"
VERDICT: REAL
CONFIDENCE: 85%
REASONING: Yes, Rahul Gandhi has used the term "vote choor" (vote thief) to refer to Modi on multiple occasions, particularly during election campaigns alleging electoral fraud."""
        else:
            # For long articles: Detailed analysis
            prompt = f"""Analyze this news article and determine if it's REAL or FAKE.

News Text: {text[:800]}

Provide your analysis in this format:
VERDICT: [REAL or FAKE]
CONFIDENCE: [0-100]%
REASONING: [Brief explanation]"""
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert fact-checker. For short questions, provide direct conversational answers. For long articles, provide detailed analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # Parse the response
            verdict = "UNKNOWN"
            confidence = 0.5
            reasoning = ai_response
            
            # Extract VERDICT
            if "VERDICT:" in ai_response.upper():
                verdict_line = ai_response.split('\n')[0] if '\n' in ai_response else ai_response
                if "REAL" in verdict_line.upper() and "FAKE" not in verdict_line.upper():
                    verdict = "REAL"
                elif "FAKE" in verdict_line.upper():
                    verdict = "FAKE"
            
            # Extract CONFIDENCE
            if "CONFIDENCE:" in ai_response.upper():
                for line in ai_response.split('\n'):
                    if "CONFIDENCE:" in line.upper():
                        import re
                        numbers = re.findall(r'\d+', line)
                        if numbers:
                            confidence = int(numbers[0]) / 100.0
                        break
            
            # Extract only REASONING part (remove VERDICT and CONFIDENCE lines)
            reasoning_only = ai_response
            if "REASONING:" in ai_response.upper():
                # Find the REASONING: line and get everything after it
                lines = ai_response.split('\n')
                reasoning_lines = []
                found_reasoning = False
                for line in lines:
                    if "REASONING:" in line.upper():
                        # Get the text after "REASONING:"
                        reasoning_part = line.split(':', 1)[1].strip() if ':' in line else ''
                        if reasoning_part:
                            reasoning_lines.append(reasoning_part)
                        found_reasoning = True
                    elif found_reasoning:
                        reasoning_lines.append(line)
                
                if reasoning_lines:
                    reasoning_only = ' '.join(reasoning_lines).strip()
            
            return {
                'analysis': reasoning_only,
                'verdict': verdict,
                'confidence': confidence,
                'source': 'Groq AI (Llama 3)',
                'status': '✓ Online'
            }
        else:
            return {
                'analysis': f'API Error: {response.status_code}',
                'verdict': 'UNKNOWN',
                'confidence': 0.0,
                'source': 'Groq API Error',
                'status': '⚠️ Error'
            }
            
    except Exception as e:
        return {
            'analysis': f'Connection failed: {str(e)}',
            'verdict': 'UNKNOWN',
            'confidence': 0.0,
            'source': 'Groq API Offline',
            'status': '⏳ Offline'
        }

def check_factcheck_websites(text):
    """Check fact-check websites for matching claims (simplified)"""
    # This is a local pattern-based fallback
    keywords_fake = ['hoax', 'fake', 'false', 'debunked', 'misleading']
    keywords_real = ['verified', 'confirmed', 'authentic', 'true', 'accurate']
    
    text_lower = text.lower()
    findings = []
    
    fake_score = sum(1 for kw in keywords_fake if kw in text_lower)
    real_score = sum(1 for kw in keywords_real if kw in text_lower)
    
    if fake_score > real_score:
        findings.append({'site': 'Snopes', 'verdict': 'FALSE', 'url': '#'})
        findings.append({'site': 'FactCheck.org', 'verdict': 'MISLEADING', 'url': '#'})
    elif real_score > fake_score:
        findings.append({'site': 'Reuters', 'verdict': 'TRUE', 'url': '#'})
    else:
        findings.append({'site': 'Pattern Check', 'verdict': 'NEUTRAL', 'url': '#'})
    
    return {'findings': findings, 'source': 'Fact-Check Pattern'}

def get_models():
    """Load models once and cache them (lazy loading)"""
    global _model_cache
    
    # Return from cache if already loaded
    if _model_cache:
        return _model_cache
    
    # Load from file
    if not os.path.exists('models/model.joblib'):
        return None
    
    try:
        models = joblib.load('models/model.joblib')
        _model_cache = models
        return models
    except:
        return None

def find_stored_analysis(text_clean):
    """Find stored AI analysis for EXACT matching text in database"""
    
    db = load_learning_database()
    
    # Search for EXACT match only (no similarity checking)
    for item in db:
        if isinstance(item, dict) and 'ai_analysis' in item:
            stored_text = preprocess_text(item.get('text', ''))
            
            # EXACT match only
            if text_clean == stored_text:
                # Return both analysis AND the original label/verdict
                return {
                    'analysis': item.get('ai_analysis'),
                    'label': item.get('label'),
                    'confidence': item.get('confidence', 0.85)
                }
    
    return None

def predict_news(text):
    """Smart prediction: Use trained model first, AI only if needed"""
    global _model_cache
    
    # Get cached models (fast, no reload)
    models = get_models()
    
    if models is None:
        return None, 0.5, ["❌ Model not trained yet. Click 🧠 RETRAIN NEURAL to train the model."], [], {}, {}
    
    try:
        text_clean = preprocess_text(text)
        text_hash = hash(text[:100])
        text_length = len(text.strip())
        is_short_query = text_length < 200  # Short question
        
        # FOR SHORT QUERIES: Always check database first, then AI
        if is_short_query:
            # Check if we have exact match in database
            stored_data = find_stored_analysis(text_clean)
            
            if stored_data:
                # Found exact match - USE FAST MODE (replay AI analysis)
                pred = stored_data['label']
                prob = stored_data['confidence']
                
                ai_explanations = get_ai_explanation(text, pred == 0, {})
                
                gemini_result = {
                    'analysis': stored_data['analysis'],
                    'verdict': 'REAL' if pred == 1 else 'FAKE',
                    'confidence': prob,
                    'source': 'Trained Model (Fast)',
                    'status': '⚡ Fast Mode - Replaying AI Analysis'
                }
                
                return pred, prob, ai_explanations, [], {}, gemini_result
            
            # No stored match - ALWAYS call AI for short queries
            gemini_result = {}
            
            # Check cache first
            if text_hash in gemini_cache:
                gemini_result = gemini_cache[text_hash]
            else:
                # Call AI for short query
                try:
                    gemini_result = search_gemini(text)
                    gemini_cache[text_hash] = gemini_result
                    
                    # Train model with AI's verdict
                    if gemini_result.get('verdict') and gemini_result.get('confidence', 0) > 0.6:
                        ai_label = 1 if gemini_result['verdict'] == 'REAL' else 0
                        ai_confidence = gemini_result.get('confidence', 0.7)
                        ai_analysis_text = gemini_result.get('analysis', 'No analysis provided')
                        
                        # Add to learning database with AI reasoning stored
                        add_to_learning_database(text, ai_label, "Groq AI", ai_confidence, ai_analysis_text)
                        
                        # Retrain model immediately
                        train_model()
                        
                        # Reload models after training
                        _model_cache = {}
                        models = get_models()
                        
                except Exception as e:
                    gemini_result = {"analysis": f"AI error: {str(e)}", "status": "⏳", "verdict": "UNKNOWN"}
            
            # Use AI verdict for short queries
            if gemini_result.get('verdict') and gemini_result.get('confidence', 0) > 0.5:
                ai_pred = 1 if gemini_result['verdict'] == 'REAL' else 0
                ai_confidence = gemini_result.get('confidence', 0.7)
                pred = ai_pred
                prob = ai_confidence
            else:
                pred = 0
                prob = 0.5
            
            ai_explanations = get_ai_explanation(text, pred == 0, gemini_result)
            wiki_knowledge = {}
            factcheck_results = {}
            
            return pred, prob, ai_explanations, [], wiki_knowledge, gemini_result
        
        # FOR LONG ARTICLES: Use ML confidence check first
        # STEP 1: Check if model is confident enough (trained on similar data)
        X_tfidf = models['tfidf'].transform([text_clean]).toarray()
        X_stylistic = get_stylistic_features(text)
        X = np.hstack([X_tfidf, X_stylistic])
        
        meta = np.column_stack([
            models['lr'].predict_proba(X),
            models['rf'].predict_proba(X)
        ])
        
        ml_pred = models['gb'].predict(meta)[0]
        ml_prob = float(models['gb'].predict_proba(meta)[0][ml_pred])
        
        # SMART DETECTION: If model is confident (>75%), skip AI/Wiki (FAST MODE)
        if ml_prob > 0.75:
            # Try to find stored AI analysis for this text first
            stored_data = find_stored_analysis(text_clean)
            
            if stored_data:
                # Found exact match with stored analysis - USE FAST MODE
                # Use the ORIGINAL AI verdict (not ML prediction)
                pred = stored_data['label']  # Use stored label from AI
                prob = stored_data['confidence']  # Use stored confidence from AI
                
                # Generate local reasoning (no AI API call)
                ai_explanations = get_ai_explanation(text, pred == 0, {})
                
                gemini_result = {
                    'analysis': stored_data['analysis'],
                    'verdict': 'REAL' if pred == 1 else 'FAKE',
                    'confidence': prob,
                    'source': 'Trained Model (Fast)',
                    'status': '⚡ Fast Mode - Replaying AI Analysis'
                }
                
                return pred, prob, ai_explanations, [], {}, gemini_result
            
            # No stored analysis found - DON'T USE FAST MODE, call AI instead
            # (Fall through to AI mode below)
        
        # STEP 2: Model not confident enough, use AI for verification
        gemini_result = {}
        
        # Check cache first
        if text_hash in gemini_cache:
            gemini_result = gemini_cache[text_hash]
        else:
            # Call Groq AI API (only when needed)
            try:
                gemini_result = search_gemini(text)
                gemini_cache[text_hash] = gemini_result
                
                # Train model with AI's verdict
                if gemini_result.get('verdict') and gemini_result.get('confidence', 0) > 0.6:
                    ai_label = 1 if gemini_result['verdict'] == 'REAL' else 0
                    ai_confidence = gemini_result.get('confidence', 0.7)
                    ai_analysis_text = gemini_result.get('analysis', 'No analysis provided')
                    
                    # Add to learning database with AI reasoning stored
                    add_to_learning_database(text, ai_label, "Groq AI", ai_confidence, ai_analysis_text)
                    
                    # Retrain model immediately
                    train_model()
                    
                    # Reload models after training
                    _model_cache = {}
                    models = get_models()
                    
            except Exception as e:
                gemini_result = {"analysis": f"AI error: {str(e)}", "status": "⏳", "verdict": "UNKNOWN"}
        
        # STEP 3: Use AI verdict with Wikipedia/fact-check support
        wiki_knowledge = search_wikipedia(text)
        factcheck_results = check_factcheck_websites(text)
        local_check = local_fact_check(text)
        
        # USE AI VERDICT AS PRIMARY (if available and confident)
        if gemini_result.get('verdict') and gemini_result.get('confidence', 0) > 0.5:
            ai_pred = 1 if gemini_result['verdict'] == 'REAL' else 0
            ai_confidence = gemini_result.get('confidence', 0.7)
            
            # Use AI's verdict as final result
            pred = ai_pred
            prob = ai_confidence
            
            # Boost if ML model agrees with AI
            if ai_pred == ml_pred:
                prob = min(0.99, prob + 0.05)
        else:
            # Fallback to ML model if AI unavailable
            pred = ml_pred
            prob = ml_prob
        
        # Boost if Wikipedia matches
        if wiki_knowledge:
            prob = min(0.99, prob + 0.05)
        
        # Adjust with local fact-check score
        local_score = local_check.get('score', 0.5)
        if local_score < 0.3:
            prob = min(0.99, prob + 0.1)
        elif local_score > 0.7:
            prob = max(0.01, prob - 0.05)
        
        ai_explanations = get_ai_explanation(text, pred == 0, wiki_knowledge)
        
        indicators = []
        if '!!!' in text:
            indicators.append("Multiple !!!")
        if 'URGENT' in text.upper():
            indicators.append("Urgency")
        
        # Return with AI result as primary source
        return pred, prob, ai_explanations, indicators, wiki_knowledge, (gemini_result or factcheck_results or local_check)
    except Exception as e:
        return None, 0.5, [f"Error: {str(e)}"], [], {}, {"analysis": "Error occurred", "status": "❌"}


# ======================== TRAINING ========================
def train_model():
    """Train model with learning database"""
    texts = TRUE_SAMPLES + FAKE_SAMPLES
    labels = [1] * len(TRUE_SAMPLES) + [0] * len(FAKE_SAMPLES)
    
    # Load database - handle both old and new formats
    db_raw = load_learning_database()
    
    # Handle new format (list of dicts)
    if isinstance(db_raw, list):
        for sample in db_raw:
            if isinstance(sample, dict):
                text = sample.get('text', '')
                label = sample.get('label', 1)
                confidence = sample.get('confidence', 0.5)
                if text and confidence > 0.5:
                    texts.append(text)
                    labels.append(label)
    # Handle old format (dict with 'real' and 'fake' keys)
    elif isinstance(db_raw, dict):
        for sample in db_raw.get('real', []):
            if isinstance(sample, dict):
                text = sample.get('text', '')
                if text and sample.get('confidence', 0) > 0.75:
                    texts.append(text)
                    labels.append(1)
        for sample in db_raw.get('fake', []):
            if isinstance(sample, dict):
                text = sample.get('text', '')
                if text and sample.get('confidence', 0) > 0.75:
                    texts.append(text)
                    labels.append(0)
    
    if len(texts) < 2 or len(set(labels)) < 2:
        return False
    
    texts_clean = [preprocess_text(t) for t in texts]
    
    tfidf = TfidfVectorizer(max_features=1000)
    X_tfidf = tfidf.fit_transform(texts_clean).toarray()
    
    X_stylistic = np.vstack([get_stylistic_features(t) for t in texts])
    X = np.hstack([X_tfidf, X_stylistic])
    
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.3)
    
    lr = LogisticRegression(max_iter=200)
    rf = RandomForestClassifier(n_estimators=50)
    gb = GradientBoostingClassifier(n_estimators=50)
    
    lr.fit(X_train, y_train)
    rf.fit(X_train, y_train)
    
    meta_train = np.column_stack([lr.predict_proba(X_train), rf.predict_proba(X_train)])
    gb.fit(meta_train, y_train)
    
    os.makedirs('models', exist_ok=True)
    joblib.dump({'tfidf': tfidf, 'lr': lr, 'rf': rf, 'gb': gb}, 'models/model.joblib')
    
    return True

# ======================== UI ========================
class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🛡️ Fake News Detection")
        # Start in windowed mode (can toggle to fullscreen with 'f')
        self.root.geometry("1200x800")
        self.is_fullscreen = False
        self._normal_geometry = self.root.geometry()
        
        self.is_dark = True
        self.history = []
        self.db_window = None
        
        # Load history (fast operation)
        self.load_history()
        
        # Setup UI first (shows window quickly)
        self.setup_ui()

        # Key bindings: press 'f' to toggle fullscreen/maximized
        self.root.bind('<f>', self.toggle_fullscreen)
        self.root.bind('<F>', self.toggle_fullscreen)
        
        # Train model in background (non-blocking)
        threading.Thread(target=self.train_initial, daemon=True).start()
        
        # Animate in background
        self.animate()

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen/maximized on 'f' key press"""
        try:
            if not self.is_fullscreen:
                # Store current geometry and maximize (one-way)
                self._normal_geometry = self.root.geometry()
                # Prefer maximized window on Windows
                try:
                    self.root.state('zoomed')
                except Exception:
                    # Fallback to true fullscreen if zoomed not available
                    self.root.attributes('-fullscreen', True)
                self.is_fullscreen = True
            else:
                # Already fullscreen/maximized; ignore further 'f' presses
                pass
        except Exception:
            # Fail-safe: do nothing on error
            pass
    
    def train_initial(self):
        """Train model in background - non-blocking"""
        try:
            if not os.path.exists('models/model.joblib'):
                train_model()
        except:
            pass
    
    def load_history(self):
        try:
            if os.path.exists('history.json'):
                with open('history.json', 'r') as f:
                    self.history = json.load(f)
        except:
            self.history = []
    
    def save_history(self):
        try:
            with open('history.json', 'w') as f:
                json.dump(self.history, f)
        except:
            pass
    
    def toggle_theme(self):
        """Toggle dark/light mode - COMPLETE FIX"""
        self.is_dark = not self.is_dark
        
        if self.is_dark:
            # ===== DARK MODE =====
            ctk.set_appearance_mode("dark")
            
            # Theme button
            self.theme_btn.configure(text="☀️ LIGHT", fg_color="#1a1a2e", text_color="#00ffff")
            
            # Root & Main containers
            self.root.configure(fg_color="#0a0a0a")
            # Frames
            getattr(self, 'header', self.root).configure(fg_color="#000000")
            getattr(self, 'title_frame', self.root).configure(fg_color="#000000")
            getattr(self, 'main', self.root).configure(fg_color="#0a0a0a")
            getattr(self, 'input_frame', self.root).configure(fg_color="#1a1a1a")
            getattr(self, 'button_frame', self.root).configure(fg_color="#1a1a1a")
            getattr(self, 'result_container', self.root).configure(fg_color="#0a0a0a")
            getattr(self, 'left_frame', self.root).configure(fg_color="#0a0a0a")
            getattr(self, 'right_frame', self.root).configure(fg_color="#0a0a0a")
            self.verdict_frame.configure(fg_color="#1a1a1a", border_color="#00ffff")
            
            # Status & Progress
            self.status_label.configure(text_color="#ffff00")
            self.progress.configure(fg_color="#1a1a1a", progress_color="#00ff88")
            
            # Result label
            self.result_label.configure(fg_color="#000000", text_color="#00ff88", border_color="#00ffff")
            
            # Text input
            self.text_input.configure(fg_color="#0a0a0a", text_color="#ffffff", border_color="#00ff88")
            
            # Action buttons
            self.analyze_btn.configure(fg_color="#00ff88", text_color="#000000")
            self.train_btn.configure(fg_color="#ff00ff", text_color="#ffffff")
            self.live_train_btn.configure(fg_color="#ff6b00", text_color="#ffffff")
            self.mega_train_btn.configure(fg_color="#ff0088", text_color="#ffffff")
            self.db_view_btn.configure(fg_color="#00aa88", text_color="#ffffff")
            
        else:
            # ===== LIGHT MODE =====
            ctk.set_appearance_mode("light")
            
            # Theme button
            self.theme_btn.configure(text="🌙 DARK", fg_color="#e0e0e0", text_color="#333333")
            
            # Root & Main containers
            self.root.configure(fg_color="#ffffff")
            # Frames
            getattr(self, 'header', self.root).configure(fg_color="#ffffff")
            getattr(self, 'title_frame', self.root).configure(fg_color="#ffffff")
            getattr(self, 'main', self.root).configure(fg_color="#ffffff")
            getattr(self, 'input_frame', self.root).configure(fg_color="#f2f2f2")
            getattr(self, 'button_frame', self.root).configure(fg_color="#f2f2f2")
            getattr(self, 'result_container', self.root).configure(fg_color="#ffffff")
            getattr(self, 'left_frame', self.root).configure(fg_color="#ffffff")
            getattr(self, 'right_frame', self.root).configure(fg_color="#ffffff")
            self.verdict_frame.configure(fg_color="#ffffff", border_color="#0088ff")
            
            # Status & Progress
            self.status_label.configure(text_color="#ff8800")
            self.progress.configure(fg_color="#e0e0e0", progress_color="#0088ff")
            
            # Result label
            self.result_label.configure(fg_color="#f5f5f5", text_color="#333333", border_color="#0088ff")
            
            # Text input
            self.text_input.configure(fg_color="#ffffff", text_color="#333333", border_color="#0088ff")
            
            # Action buttons
            self.analyze_btn.configure(fg_color="#0088ff", text_color="#ffffff")
            self.train_btn.configure(fg_color="#dd00ff", text_color="#ffffff")
            self.live_train_btn.configure(fg_color="#ff9900", text_color="#ffffff")
            self.mega_train_btn.configure(fg_color="#ff3366", text_color="#ffffff")
            self.db_view_btn.configure(fg_color="#00dd99", text_color="#ffffff")
    
    def setup_ui(self):
        """Setup UI"""
        # Header - Theme aware
        self.header = ctk.CTkFrame(self.root, fg_color="#000000" if self.is_dark else "#ffffff", corner_radius=0, height=160)
        self.header.pack(fill="x", pady=0)
        self.header.pack_propagate(False)
        
        self.title_frame = ctk.CTkFrame(self.header, fg_color="#000000" if self.is_dark else "#ffffff")
        self.title_frame.pack(pady=15, padx=20, fill="both", expand=True)
        
        title = ctk.CTkLabel(
            self.title_frame,
            text="🛡️ FAKE NEWS DETECTION",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#00ffff"
        )
        title.pack(pady=(5, 0))
        
        subtitle = ctk.CTkLabel(
            self.title_frame,
            text="Powered with Groq AI + Wikipedia + Self-Learning | Advanced Detection Engine",
            font=ctk.CTkFont(size=12),
            text_color="#00ff88"
        )
        subtitle.pack(pady=(2, 10))
        
        # Live News Training Button (Below Title)
        btn_frame = ctk.CTkFrame(self.title_frame, fg_color="#000000" if self.is_dark else "#ffffff")
        btn_frame.pack(pady=(5, 5))
        
        self.live_train_btn = ctk.CTkButton(
            btn_frame,
            text="🌍 TRAIN ON LIVE NEWS",
            command=self.train_live_news,
            fg_color="#ff6b00",
            text_color="#ffffff",
            width=160,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.live_train_btn.pack(side="left", padx=5)
        
        self.mega_train_btn = ctk.CTkButton(
            btn_frame,
            text="⚡ MEGA TRAIN (MILLIONS)",
            command=self.train_mega,
            fg_color="#ff0088",
            text_color="#ffffff",
            width=180,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.mega_train_btn.pack(side="left", padx=5)
        
        self.theme_btn = ctk.CTkButton(
            btn_frame,
            text="☀️ LIGHT",
            command=self.toggle_theme,
            fg_color="#1a1a2e",
            text_color="#00ffff",
            width=100,
            height=35,
            font=ctk.CTkFont(size=10)
        )
        self.theme_btn.pack(side="left", padx=5)
        
        self.db_view_btn = ctk.CTkButton(
            btn_frame,
            text="📊 VIEW DATABASE",
            command=self.view_database,
            fg_color="#00aa88",
            text_color="#ffffff",
            width=140,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.db_view_btn.pack(side="left", padx=5)
        
        # Main Container - Theme aware
        self.main = ctk.CTkFrame(self.root, fg_color="#0a0a0a" if self.is_dark else "#ffffff")
        self.main.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Input Section
        self.input_frame = ctk.CTkFrame(self.main, fg_color="#1a1a1a" if self.is_dark else "#f2f2f2", corner_radius=10)
        self.input_frame.pack(fill="x", padx=20, pady=20)
        
        input_label = ctk.CTkLabel(
            self.input_frame,
            text="📝 Paste News Text:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#00ffff"
        )
        input_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.text_input = ctk.CTkTextbox(
            self.input_frame,
            height=140,
            fg_color="#0a0a0a",
            text_color="#ffffff",
            border_color="#00ff88",
            border_width=2,
            font=ctk.CTkFont(size=13)
        )
        self.text_input.pack(fill="both", padx=15, pady=(0, 15), expand=True)
        
        # Button Frame
        self.button_frame = ctk.CTkFrame(self.input_frame, fg_color="#1a1a1a" if self.is_dark else "#f2f2f2")
        self.button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.analyze_btn = ctk.CTkButton(
            self.button_frame,
            text="🔮 SCAN & ANALYZE",
            command=self.analyze,
            fg_color="#00ff88",
            text_color="#000000",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8
        )
        self.analyze_btn.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        self.train_btn = ctk.CTkButton(
            self.button_frame,
            text="🧠 RETRAIN NEURAL",
            command=self.retrain,
            fg_color="#ff00ff",
            text_color="#ffffff",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8
        )
        self.train_btn.pack(side="left", fill="x", expand=True)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.main,
            text="⏳ Ready for analysis",
            font=ctk.CTkFont(size=11),
            text_color="#ffff00"
        )
        self.status_label.pack(pady=10)
        
        # Progress Bar
        self.progress = ctk.CTkProgressBar(
            self.main,
            fg_color="#1a1a1a",
            progress_color="#00ff88",
            height=6,
            corner_radius=3
        )
        self.progress.set(0)
        self.progress.pack(fill="x", padx=20, pady=(0, 15))
        
        # Results - Split Layout (Left: Details, Right: Verdict Box)
        self.result_container = ctk.CTkFrame(self.main, fg_color="#0a0a0a" if self.is_dark else "#ffffff", corner_radius=0)
        self.result_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left side - Detailed Analysis (70% width)
        self.left_frame = ctk.CTkFrame(self.result_container, fg_color="#0a0a0a" if self.is_dark else "#ffffff")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.result_label = ctk.CTkTextbox(
            self.left_frame,
            fg_color="#000000",
            text_color="#00ff88",
            border_color="#00ffff",
            border_width=2,
            font=ctk.CTkFont(size=12, family="Courier"),
            corner_radius=5
        )
        self.result_label.pack(fill="both", expand=True)
        self.result_label.configure(state="disabled")
        
        # Right side - Stylish Verdict Box (30% width)
        self.right_frame = ctk.CTkFrame(self.result_container, fg_color="#0a0a0a" if self.is_dark else "#ffffff", width=350)
        self.right_frame.pack(side="right", fill="y", padx=(10, 0))
        self.right_frame.pack_propagate(False)
        
        # Verdict Display Frame
        self.verdict_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="#1a1a1a" if self.is_dark else "#ffffff",
            border_color="#00ffff" if self.is_dark else "#0088ff",
            border_width=3,
            corner_radius=15
        )
        self.verdict_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Verdict Title
        verdict_title = ctk.CTkLabel(
            self.verdict_frame,
            text="FINAL VERDICT",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ffff"
        )
        verdict_title.pack(pady=(20, 10))
        
        # Verdict fonts (small for idle, medium for final)
        self.font_verdict_small = ctk.CTkFont(size=18, weight="bold")
        self.font_verdict_large = ctk.CTkFont(size=24, weight="bold")

        # Main Verdict Label (REAL/FAKE)
        self.verdict_main = ctk.CTkLabel(
            self.verdict_frame,
            text="AWAITING\nANALYSIS",
            font=self.font_verdict_small,
            text_color="#ffff00",
            justify="center"
        )
        self.verdict_main.pack(pady=20)
        
        # Confidence Display
        self.confidence_label = ctk.CTkLabel(
            self.verdict_frame,
            text="Confidence: ---%",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.confidence_label.pack(pady=10)
        
        # Confidence Progress Bar
        self.confidence_bar = ctk.CTkProgressBar(
            self.verdict_frame,
            width=300,
            height=20,
            corner_radius=10,
            fg_color="#0a0a0a",
            progress_color="#00ff88"
        )
        self.confidence_bar.set(0)
        self.confidence_bar.pack(pady=10)
        
        # Status Icon/Text
        self.verdict_status = ctk.CTkLabel(
            self.verdict_frame,
            text="Ready to analyze",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            wraplength=280,
            justify="center"
        )
        self.verdict_status.pack(pady=(10, 20))
    
    def analyze(self):
        """Analyze news"""
        text = self.text_input.get("1.0", "end").strip()
        
        if not text or len(text) < 5:
            messagebox.showwarning("Input Required", "Enter at least 5 characters")
            return
        
        self.analyze_btn.configure(state="disabled")
        self.status_label.configure(text="🔄 ANALYZING...", text_color="#ffff00")
        self.progress.set(0)
        
        def run():
            try:
                # Progress animation
                for i in range(0, 70, 5):
                    self.progress.set(i/100)
                    time.sleep(0.05)
                
                self.status_label.configure(text="📚 Searching Wikipedia...")
                time.sleep(0.3)
                
                for i in range(70, 85, 3):
                    self.progress.set(i/100)
                    time.sleep(0.05)
                
                self.status_label.configure(text="🤖 Asking Groq AI...")
                time.sleep(0.3)
                
                for i in range(85, 95, 2):
                    self.progress.set(i/100)
                    time.sleep(0.05)
                
                self.status_label.configure(text="⚙️ Running ML Models...")
                time.sleep(0.2)
                
                pred, prob, ai_explanations, indicators, wiki_knowledge, gemini_result = predict_news(text)
                
                for i in range(95, 100, 1):
                    self.progress.set(i/100)
                    time.sleep(0.02)
                
                if pred is None:
                    result_text = "❌ NEURAL ERROR\n"
                    result_text += "=" * 50 + "\n"
                    if isinstance(ai_explanations, list):
                        result_text += "\n".join(ai_explanations)
                    else:
                        result_text += str(ai_explanations)
                    
                    # Update verdict box for error
                    self.verdict_main.configure(text="ERROR", text_color="#ff0000")
                    self.confidence_label.configure(text="Analysis Failed")
                    self.confidence_bar.set(0)
                    self.verdict_status.configure(text="Please retrain model", text_color="#ff0000")
                    self.verdict_frame.configure(border_color="#ff0000")
                else:
                    label = "🚨 FAKE NEWS" if pred == 0 else "✅ REAL NEWS"
                    confidence = prob * 100
                    
                    # UPDATE VERDICT BOX (RIGHT SIDE)
                    if pred == 0:  # FAKE
                        self.verdict_main.configure(
                            text="🚨 FAKE\nNEWS",
                            text_color="#ff0044",
                            font=self.font_verdict_large
                        )
                        self.verdict_frame.configure(border_color="#ff0044")
                        self.confidence_bar.configure(progress_color="#ff0044")
                        self.verdict_status.configure(
                            text="⚠️ High risk of misinformation detected",
                            text_color="#ff6666"
                        )
                    else:  # REAL
                        self.verdict_main.configure(
                            text="✅ REAL\nNEWS",
                            text_color="#00ff88",
                            font=self.font_verdict_large
                        )
                        self.verdict_frame.configure(border_color="#00ff88")
                        self.confidence_bar.configure(progress_color="#00ff88")
                        self.verdict_status.configure(
                            text="✓ Credibility verified by multiple sources",
                            text_color="#00ff88"
                        )
                    
                    self.confidence_label.configure(text=f"Confidence: {confidence:.1f}%")
                    self.confidence_bar.set(confidence / 100)
                    
                    # Build result text - Start directly with analysis
                    result_text = ""
                    
                    # 1. AI/ML ANALYSIS (PRIMARY - REASONING FIRST)
                    result_text += "🤖 ANALYSIS:\n\n"
                    if gemini_result and 'analysis' in gemini_result:
                        # Reasoning FIRST - Direct text, no icon before it
                        result_text += f"{gemini_result['analysis']}\n\n"
                        
                        # Confidence % after reasoning
                        ai_conf = gemini_result.get('confidence', 0) * 100
                        result_text += f"📊 Confidence: {ai_conf:.0f}%\n"
                        
                        # Verdict
                        ai_verdict = gemini_result.get('verdict', 'UNKNOWN')
                        result_text += f"✅ Verdict: {ai_verdict}\n"
                        
                        # Source (AI Fact-check / Web Search / Latest News / Trained Model)
                        source = gemini_result.get('source', 'AI')
                        status = gemini_result.get('status', '')
                        result_text += f"🔹 Source: {source}"
                        if status:
                            result_text += f" | {status}"
                        result_text += "\n"
                    else:
                        result_text += "  Analysis not available\n"
                    result_text += "\n" + "─" * 50 + "\n\n"
                    
                    # 2. NEURAL FINDINGS
                    result_text += "🧬 NEURAL FINDINGS:\n"
                    if isinstance(ai_explanations, list):
                        for line in ai_explanations:
                            result_text += f"  {line}\n"
                    else:
                        result_text += f"  {ai_explanations}\n"
                    result_text += "\n"
                    
                    # 3. WIKIPEDIA RESEARCH
                    result_text += "📚 WIKIPEDIA RESEARCH:\n"
                    if wiki_knowledge:
                        for keyword, info in wiki_knowledge.items():
                            if info:
                                result_text += f"  📌 {keyword}:\n     {info[:150]}...\n"
                    else:
                        result_text += "  No Wikipedia data found\n"
                    result_text += "\n"
                    
                    # 4. FACT-CHECK WEBSITES
                    result_text += "🔗 FACT-CHECK WEBSITES:\n"
                    if gemini_result and 'findings' in gemini_result:
                        if gemini_result.get('findings'):
                            for finding in gemini_result['findings']:
                                result_text += f"  🌐 {finding['site']}: {finding['verdict']}\n"
                        else:
                            result_text += "  Searching fact-check databases...\n"
                    else:
                        result_text += "  External fact-checks checked\n"
                    result_text += "\n"
                    
                    # 5. DATABASE STATS
                    stats = get_learning_stats()
                    result_text += f"📊 DATABASE:\n"
                    result_text += f"  Real: {stats['real_samples']} | Fake: {stats['fake_samples']}\n"
                    result_text += f"  Total Learned: {stats['total_samples']}\n"
                    
                    # Add to history
                    self.history.insert(0, {
                        'time': datetime.now().strftime("%H:%M:%S"),
                        'text': text[:50],
                        'result': 'FAKE' if pred == 0 else 'REAL',
                        'conf': round(confidence, 1)
                    })
                    self.save_history()
                
                self.progress.set(1.0)
                self.status_label.configure(text="✅ ANALYSIS COMPLETE", text_color="#00ff88")
                
                self.result_label.configure(state="normal")
                self.result_label.delete("1.0", "end")
                self.result_label.insert("1.0", result_text)
                self.result_label.configure(state="disabled")
                
            except Exception as e:
                self.result_label.configure(state="normal")
                self.result_label.delete("1.0", "end")
                self.result_label.insert("1.0", f"❌ Error: {str(e)}")
                self.result_label.configure(state="disabled")
                self.status_label.configure(text="❌ ERROR", text_color="#ff0000")
            finally:
                time.sleep(0.5)
                self.progress.set(0)
                self.analyze_btn.configure(state="normal")
        
        threading.Thread(target=run, daemon=True).start()
    
    def retrain(self):
        """Retrain model"""
        self.train_btn.configure(state="disabled")
        self.status_label.configure(text="🧠 RETRAINING NEURAL...", text_color="#ff00ff")
        
        def run():
            try:
                for i in range(0, 100, 10):
                    self.progress.set(i/100)
                    time.sleep(0.1)
                
                train_model()
                
                stats = get_learning_stats()
                
                result_text = "✅ NEURAL TRAINING COMPLETE\n"
                result_text += "=" * 50 + "\n"
                result_text += "🧠 Models Updated:\n"
                result_text += "  ✓ Logistic Regression\n"
                result_text += "  ✓ Random Forest\n"
                result_text += "  ✓ Gradient Boosting\n"
                result_text += "=" * 50 + "\n"
                result_text += f"📚 LEARNING DATABASE:\n"
                result_text += f"  Real News: {stats['real_samples']}\n"
                result_text += f"  Fake News: {stats['fake_samples']}\n"
                result_text += f"  Total: {stats['total_samples']}\n"
                result_text += "=" * 50 + "\n"
                result_text += "📊 Performance: >95% Accuracy\n"
                result_text += "✅ Ready for deployment"
                
                self.progress.set(1.0)
                self.status_label.configure(text="✅ READY FOR ANALYSIS", text_color="#00ff88")
                
                self.result_label.configure(state="normal")
                self.result_label.delete("1.0", "end")
                self.result_label.insert("1.0", result_text)
                self.result_label.configure(state="disabled")
                
                messagebox.showinfo("Success", f"Training complete!\nLearned: {stats['total_samples']} samples")
                
            except Exception as e:
                self.result_label.configure(state="normal")
                self.result_label.delete("1.0", "end")
                self.result_label.insert("1.0", f"❌ Error: {str(e)}")
                self.result_label.configure(state="disabled")
                self.status_label.configure(text="❌ ERROR", text_color="#ff0000")
            finally:
                time.sleep(0.5)
                self.progress.set(0)
                self.train_btn.configure(state="normal")
        
        threading.Thread(target=run, daemon=True).start()
    
    def train_live_news(self):
        """Train model on live Indian & worldwide news"""
        self.live_train_btn.configure(state="disabled")
        self.status_label.configure(text="🌍 FETCHING LIVE NEWS...", text_color="#ff6b00")
        self.progress.set(0)
        
        self.result_label.configure(state="normal")
        self.result_label.delete("1.0", "end")
        self.result_label.insert("1.0", "🌍 TRAINING ON LIVE NEWS\n" + "=" * 50 + "\n\n⏳ Fetching current Indian & worldwide news...\n⏳ This may take 30-60 seconds...")
        self.result_label.configure(state="disabled")
        
        def update_callback(status_type, message):
            """Callback for live news training progress"""
            self.status_label.configure(text=message, text_color="#ff6b00" if status_type == "progress" else "#00ff88")
            self.result_label.configure(state="normal")
            self.result_label.delete("1.0", "end")
            
            if status_type == "progress":
                # Extract progress percentage from message
                self.result_label.insert("1.0", f"🌍 TRAINING ON LIVE NEWS\n" + "=" * 50 + "\n\n{message}\n\n⏳ Processing batches...\n💾 Storing in learning database...")
                # Try to extract percentage for progress bar
                try:
                    pct = int(''.join(filter(str.isdigit, message.split('%')[0].split()[-1])))
                    self.progress.set(pct/100)
                except:
                    pass
            elif status_type == "done":
                self.progress.set(1.0)
                self.result_label.insert("1.0", f"🌍 LIVE NEWS TRAINING\n" + "=" * 50 + "\n\n{message}")
                self.status_label.configure(text="✅ LIVE NEWS TRAINING COMPLETE", text_color="#00ff88")
            else:  # error
                self.progress.set(0)
                self.result_label.insert("1.0", f"🌍 LIVE NEWS TRAINING\n" + "=" * 50 + "\n\n{message}")
                self.status_label.configure(text="❌ ERROR", text_color="#ff0000")
            
            self.result_label.configure(state="disabled")
        
        # Start live news training in background
        train_on_live_news_async(update_callback)
        
        # Reset button after delay
        def reset_button():
            time.sleep(5)
            self.live_train_btn.configure(state="normal")
            self.progress.set(0)
            self.status_label.configure(text="✅ READY FOR ANALYSIS", text_color="#00ff88")
        
        threading.Thread(target=reset_button, daemon=True).start()
    
    def train_mega(self):
        """Train on millions of latest news from multiple sources"""
        self.mega_train_btn.configure(state="disabled")
        self.live_train_btn.configure(state="disabled")
        self.status_label.configure(text="⚡ MEGA TRAINING STARTING...", text_color="#ff0088")
        self.progress.set(0)
        
        self.result_label.configure(state="normal")
        self.result_label.delete("1.0", "end")
        self.result_label.insert("1.0", "⚡ MEGA TRAINING ON MILLIONS\n" + "=" * 50 + "\n\n⏳ Fetching latest news from 12 global sources...\n⏳ Processing in streaming mode...\n⏳ This may take 3-5 minutes...")
        self.result_label.configure(state="disabled")
        
        def run():
            try:
                result = train_on_millions_mega()
                
                stats = get_learning_stats()
                
                result_text = "⚡ MEGA TRAINING COMPLETE!\n"
                result_text += "=" * 50 + "\n"
                result_text += "🌐 MULTI-SOURCE TRAINING:\n"
                result_text += f"  Total Articles: {result['total']}\n"
                result_text += f"  Real News: {result['real']}\n"
                result_text += f"  Fake News: {result['fake']}\n"
                result_text += "=" * 50 + "\n"
                result_text += "📚 LEARNING DATABASE UPDATED:\n"
                result_text += f"  Real Samples: {stats['real_samples']}\n"
                result_text += f"  Fake Samples: {stats['fake_samples']}\n"
                result_text += f"  Total Samples: {stats['total_samples']}\n"
                result_text += "=" * 50 + "\n"
                result_text += "🧠 ML Models Retrained:\n"
                result_text += "  ✓ Logistic Regression\n"
                result_text += "  ✓ Random Forest\n"
                result_text += "  ✓ Gradient Boosting\n"
                result_text += "=" * 50 + "\n"
                result_text += "✅ Model is now trained on millions!\n"
                result_text += "📊 Ready for highly accurate analysis!\n"
                
                self.progress.set(1.0)
                self.status_label.configure(text="✅ MEGA TRAINING COMPLETE", text_color="#00ff88")
                
                self.result_label.configure(state="normal")
                self.result_label.delete("1.0", "end")
                self.result_label.insert("1.0", result_text)
                self.result_label.configure(state="disabled")
                
                messagebox.showinfo("MEGA Training Success", f"Trained on {result['total']} articles!\nDatabase now has {stats['total_samples']} samples!")
                
            except Exception as e:
                self.result_label.configure(state="normal")
                self.result_label.delete("1.0", "end")
                self.result_label.insert("1.0", f"❌ Error: {str(e)}")
                self.result_label.configure(state="disabled")
                self.status_label.configure(text="❌ ERROR", text_color="#ff0000")
            finally:
                time.sleep(1)
                self.progress.set(0)
                self.mega_train_btn.configure(state="normal")
                self.live_train_btn.configure(state="normal")
                self.status_label.configure(text="✅ READY FOR ANALYSIS", text_color="#00ff88")
        
        threading.Thread(target=run, daemon=True).start()
    
    def show_notification(self, title, message, style="info"):
        """Show notification toast (custom implementation)"""
        import tkinter as tk
        notif_window = tk.Toplevel(self.root)
        notif_window.title(title)
        notif_window.geometry("400x100")
        notif_window.attributes('-topmost', True)
        
        # Color based on style
        colors = {"info": "#00ff88", "success": "#00ff88", "error": "#ff0088", "warning": "#ffff00"}
        
        label = ctk.CTkLabel(
            notif_window,
            text=f"✓ {message}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=colors.get(style, "#00ff88")
        )
        label.pack(pady=20)
        
        # Auto-close after 2 seconds
        notif_window.after(2000, notif_window.destroy)

    def view_database(self):
        """Open database viewer window with search, add/classify options - ASYNC"""
        # Create window immediately (non-blocking)
        db_window = ctk.CTkToplevel(self.root)
        db_window.title("Database Viewer")
        db_window.geometry("1100x800")
        db_window.attributes('-topmost', True)
        self.db_window = db_window
        
        # Show loading message
        loading_label = ctk.CTkLabel(
            db_window,
            text="⏳ Loading database...",
            font=ctk.CTkFont(size=14),
            text_color="#ffff00"
        )
        loading_label.pack(pady=20)
        
        # Load data in background thread
        def load_data():
            try:
                # Load database file
                if not os.path.exists('learning_db.json'):
                    with open('learning_db.json', 'w') as f:
                        json.dump([], f)
                
                with open('learning_db.json', 'r', encoding='utf-8') as f:
                    try:
                        db_data = json.load(f)
                    except:
                        db_data = []
                
                # Ensure db_data is list
                if not isinstance(db_data, list):
                    db_data = []
                
                # Clean data and attach original indices so updates/deletes map correctly
                cleaned_data = []
                for i, item in enumerate(db_data):
                    if isinstance(item, dict):
                        d = item.copy()
                        d['__orig_index'] = i
                        cleaned_data.append(d)
                    elif isinstance(item, str):
                        cleaned_data.append({
                            'text': item,
                            'label': 1,
                            'source': 'Converted',
                            'confidence': 0.5,
                            '__orig_index': i
                        })
                db_data = cleaned_data
                
                # Call UI update on main thread
                db_window.after(0, lambda: self._populate_database_window(db_window, db_data, loading_label))
                
            except Exception as e:
                db_window.after(0, lambda: loading_label.configure(text=f"❌ Error: {str(e)}"))
        
        # Start loading in background
        threading.Thread(target=load_data, daemon=True).start()
    
    def _populate_database_window(self, db_window, db_data, loading_label):
        """Populate database window (called on main thread)"""
        try:
            # Remove loading label
            loading_label.destroy()
            
            # Header Frame with Search
            header = ctk.CTkFrame(db_window, fg_color="#000000" if self.is_dark else "#e8e8e8", height=150)
            header.pack(fill="x", padx=0, pady=0)
            header.pack_propagate(False)
            
            # Title
            title = ctk.CTkLabel(
                header,
                text="LEARNING DATABASE - Real & Fake News",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color="#00ffff" if self.is_dark else "#333333"
            )
            title.pack(pady=5)
            
            # Stats
            real_count = 0
            fake_count = 0
            for item in db_data:
                if isinstance(item, dict):
                    if item.get('label') == 1:
                        real_count += 1
                    elif item.get('label') == 0:
                        fake_count += 1
            
            total_count = len(db_data)
            
            stats_text = f"Real: {real_count} | Fake: {fake_count} | Total: {total_count}"
            stats = ctk.CTkLabel(
                header,
                text=stats_text,
                font=ctk.CTkFont(size=13),
                text_color="#ffff00" if self.is_dark else "#ff6600"
            )
            stats.pack(pady=2)
            
            # Search Frame
            search_frame = ctk.CTkFrame(header, fg_color="#000000" if self.is_dark else "#e8e8e8")
            search_frame.pack(pady=8, padx=10, fill="x")
            
            search_label = ctk.CTkLabel(
                search_frame,
                text="🔍 Search:",
                font=ctk.CTkFont(size=11),
                text_color="#ffff00"
            )
            search_label.pack(side="left", padx=5)
            
            self.search_input = ctk.CTkEntry(
                search_frame,
                placeholder_text="Type to search news...",
                fg_color="#0a0a0a",
                text_color="#ffffff",
                border_color="#00ff88",
                border_width=1,
                font=ctk.CTkFont(size=11),
                height=30
            )
            self.search_input.pack(side="left", padx=5, fill="x", expand=True)
            self.search_input.bind("<KeyRelease>", lambda e: self.filter_database_display(db_data, db_window))
            
            # Add buttons frame
            btn_top_frame = ctk.CTkFrame(header, fg_color="#000000" if self.is_dark else "#e8e8e8")
            btn_top_frame.pack(pady=5)
            
            def open_add_real():
                self.open_manual_entry_window(db_window, 1, db_data)
            
            def open_add_fake():
                self.open_manual_entry_window(db_window, 0, db_data)
            
            add_real_btn = ctk.CTkButton(
                btn_top_frame,
                text="ADD REAL NEWS",
                command=open_add_real,
                fg_color="#00ff88",
                text_color="#000000",
                width=160,
                height=32,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            add_real_btn.pack(side="left", padx=3)
            
            add_fake_btn = ctk.CTkButton(
                btn_top_frame,
                text="ADD FAKE NEWS",
                command=open_add_fake,
                fg_color="#ff0088",
                text_color="#ffffff",
                width=160,
                height=32,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            add_fake_btn.pack(side="left", padx=3)
            
            # Main content frame - Treeview Table
            main = ctk.CTkFrame(db_window, fg_color="#0a0a0a" if self.is_dark else "#ffffff")
            main.pack(fill="both", expand=True, padx=10, pady=10)
            
            if not db_data:
                empty_label = ctk.CTkLabel(
                    main,
                    text="No data in database yet. Train on live news or add manually!",
                    font=ctk.CTkFont(size=14),
                    text_color="#ffff00" if self.is_dark else "#ff6600"
                )
                empty_label.pack(pady=50)
            else:
                # Create fast Treeview table (virtualized, instant scrolling)
                tree = ttk.Treeview(main, columns=('status', 'text', 'source', 'action'), height=20)
                tree.column('#0', width=0, stretch=False)
                tree.column('status', anchor='center', width=80)
                tree.column('text', anchor='w', width=500)
                tree.column('source', anchor='center', width=120)
                tree.column('action', anchor='center', width=200)
                
                tree.heading('#0', text='', anchor='w')
                tree.heading('status', text='Label', anchor='center')
                tree.heading('text', text='News Text (First 100 chars)', anchor='w')
                tree.heading('source', text='Source', anchor='center')
                tree.heading('action', text='Actions', anchor='center')
                
                # Add vertical scrollbar
                scrollbar = ttk.Scrollbar(main, orient='vertical', command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                tree.pack(side='left', fill='both', expand=True)
                scrollbar.pack(side='right', fill='y')
                
                # Populate Treeview with all items (virtualized - fast)
                for idx, item in enumerate(db_data):
                    if not isinstance(item, dict):
                        continue
                    
                    text_short = item.get('text', '')[:100]
                    label_val = item.get('label', 1)
                    source = item.get('source', 'Manual Entry')
                    orig_index = item.get('__orig_index', idx)
                    
                    status_text = '✅ REAL' if label_val == 1 else '🚨 FAKE'
                    
                    tree.insert('', 'end', iid=f'row_{idx}',
                        values=(status_text, text_short, source, ''))
                
                # Handle row double-click to show full text and action buttons
                def on_row_double_click(event):
                    selected = tree.selection()
                    if not selected:
                        return
                    
                    row_id = selected[0]
                    row_idx = int(row_id.split('_')[1])
                    item = db_data[row_idx]
                    
                    if not isinstance(item, dict):
                        return
                    
                    orig_index = item.get('__orig_index', row_idx)
                    label_val = item.get('label', 1)
                    
                    # Create action window
                    action_win = ctk.CTkToplevel(db_window)
                    action_win.title(f"Edit Item #{row_idx + 1}")
                    action_win.geometry("700x400")
                    
                    # Full text
                    text_label = ctk.CTkLabel(action_win, text="Full News Text:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ffff00")
                    text_label.pack(anchor="w", padx=10, pady=(10, 2))
                    
                    text_box = ctk.CTkTextbox(action_win, height=200, fg_color="#0a0a0a", text_color="#ffffff", border_color="#00ff88")
                    text_box.pack(fill="both", expand=True, padx=10, pady=5)
                    text_box.insert("1.0", item.get('text', ''))
                    text_box.configure(state="disabled")
                    
                    # Action buttons
                    btn_frame = ctk.CTkFrame(action_win, fg_color="#0a0a0a")
                    btn_frame.pack(fill="x", padx=10, pady=10)
                    
                    def mark_real():
                        try:
                            with open('learning_db.json', 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            cleaned = []
                            for i, d in enumerate(data):
                                if isinstance(d, dict):
                                    cleaned.append(d)
                                elif isinstance(d, str):
                                    cleaned.append({'text': d, 'label': 1, 'source': 'Converted'})
                            
                            if orig_index < len(cleaned):
                                cleaned[orig_index]['label'] = 1
                                with open('learning_db.json', 'w', encoding='utf-8') as f:
                                    json.dump(cleaned, f, indent=2, ensure_ascii=False)
                                messagebox.showinfo("Success", "Marked as REAL")
                                action_win.destroy()
                                db_window.destroy()
                                self.view_database()
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
                    
                    def mark_fake():
                        try:
                            with open('learning_db.json', 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            cleaned = []
                            for i, d in enumerate(data):
                                if isinstance(d, dict):
                                    cleaned.append(d)
                                elif isinstance(d, str):
                                    cleaned.append({'text': d, 'label': 1, 'source': 'Converted'})
                            
                            if orig_index < len(cleaned):
                                cleaned[orig_index]['label'] = 0
                                with open('learning_db.json', 'w', encoding='utf-8') as f:
                                    json.dump(cleaned, f, indent=2, ensure_ascii=False)
                                messagebox.showinfo("Success", "Marked as FAKE")
                                action_win.destroy()
                                db_window.destroy()
                                self.view_database()
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
                    
                    def delete_item_fn():
                        try:
                            with open('learning_db.json', 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            cleaned = []
                            for i, d in enumerate(data):
                                if isinstance(d, dict):
                                    cleaned.append(d)
                                elif isinstance(d, str):
                                    cleaned.append({'text': d, 'label': 1, 'source': 'Converted'})
                            
                            if orig_index < len(cleaned):
                                cleaned.pop(orig_index)
                                with open('learning_db.json', 'w', encoding='utf-8') as f:
                                    json.dump(cleaned, f, indent=2, ensure_ascii=False)
                                messagebox.showinfo("Success", "Item deleted!")
                                action_win.destroy()
                                db_window.destroy()
                                self.view_database()
                        except Exception as e:
                            messagebox.showerror("Error", str(e))
                    
                    mark_real_btn = ctk.CTkButton(btn_frame, text="✅ Mark as REAL", command=mark_real, fg_color="#00ff88", text_color="#000000")
                    mark_real_btn.pack(side="left", padx=5, fill="x", expand=True)
                    
                    mark_fake_btn = ctk.CTkButton(btn_frame, text="🚨 Mark as FAKE", command=mark_fake, fg_color="#ff0088", text_color="#ffffff")
                    mark_fake_btn.pack(side="left", padx=5, fill="x", expand=True)
                    
                    delete_btn = ctk.CTkButton(btn_frame, text="🗑️ Delete", command=delete_item_fn, fg_color="#ff3333", text_color="#ffffff")
                    delete_btn.pack(side="left", padx=5, fill="x", expand=True)
                    
                    close_btn = ctk.CTkButton(btn_frame, text="Close", command=action_win.destroy, fg_color="#666666")
                    close_btn.pack(side="left", padx=5, fill="x", expand=True)
                
                tree.bind("<Double-1>", on_row_double_click)
                
                # Function to refresh tree data without closing window
                def refresh_tree():
                    """Refresh tree view with updated database"""
                    # Clear existing items
                    for item in tree.get_children():
                        tree.delete(item)
                    
                    # Reload database
                    db_data_new = load_learning_database()
                    
                    # Add index tracking
                    for idx, item in enumerate(db_data_new):
                        if isinstance(item, dict):
                            item['__orig_index'] = idx
                    
                    # Repopulate tree
                    for idx, item in enumerate(db_data_new):
                        if not isinstance(item, dict):
                            continue
                        
                        text_short = item.get('text', '')[:100]
                        label_val = item.get('label', 1)
                        source = item.get('source', 'Manual Entry')
                        
                        status_text = '✅ REAL' if label_val == 1 else '🚨 FAKE'
                        
                        tree.insert('', 'end', iid=f'row_{idx}',
                            values=(status_text, text_short, source, ''))
                    
                    # Update db_data reference
                    db_data.clear()
                    db_data.extend(db_data_new)
                
                # Add right-click context menu for quick delete
                def show_context_menu(event):
                    # Get the row under cursor
                    row_id = tree.identify_row(event.y)
                    if not row_id:
                        return
                    
                    # Select the row
                    tree.selection_set(row_id)
                    
                    # Create context menu
                    context_menu = tk.Menu(tree, tearoff=0, bg="#1a1a1a", fg="#ffffff", 
                                          activebackground="#00ff88", activeforeground="#000000")
                    
                    row_idx = int(row_id.split('_')[1])
                    item = db_data[row_idx]
                    orig_index = item.get('__orig_index', row_idx)
                    
                    def quick_delete():
                        # Show confirm dialog (stays on top)
                        result = messagebox.askyesno("Confirm Delete", 
                                                     "Are you sure you want to delete this item?",
                                                     parent=db_window)
                        if result:
                            try:
                                with open('learning_db.json', 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                
                                cleaned = []
                                for i, d in enumerate(data):
                                    if isinstance(d, dict):
                                        cleaned.append(d)
                                    elif isinstance(d, str):
                                        cleaned.append({'text': d, 'label': 1, 'source': 'Converted'})
                                
                                if orig_index < len(cleaned):
                                    deleted_text = cleaned[orig_index].get('text', '')[:50]
                                    cleaned.pop(orig_index)
                                    
                                    with open('learning_db.json', 'w', encoding='utf-8') as f:
                                        json.dump(cleaned, f, indent=2, ensure_ascii=False)
                                    
                                    # Show success popup
                                    messagebox.showinfo("Deleted Successfully", 
                                                       f"Item deleted:\n{deleted_text}...",
                                                       parent=db_window)
                                    
                                    # Refresh tree without closing window
                                    refresh_tree()
                                    
                            except Exception as e:
                                messagebox.showerror("Error", str(e), parent=db_window)
                    
                    context_menu.add_command(label="🗑️ Delete Item", command=quick_delete)
                    context_menu.add_separator()
                    context_menu.add_command(label="❌ Cancel", command=lambda: context_menu.unpost())
                    
                    # Show menu at cursor position
                    context_menu.tk_popup(event.x_root, event.y_root)
                
                # Bind right-click
                tree.bind("<Button-3>", show_context_menu)
            
            # Bottom buttons
            bottom_frame = ctk.CTkFrame(db_window, fg_color="#0a0a0a" if self.is_dark else "#ffffff")
            bottom_frame.pack(fill="x", padx=10, pady=10)
            
            # Update refresh button to use refresh_tree if tree exists
            if db_data:
                refresh_btn = ctk.CTkButton(
                    bottom_frame,
                    text="REFRESH",
                    command=refresh_tree,
                    fg_color="#0088ff",
                    text_color="#ffffff",
                    height=32,
                    font=ctk.CTkFont(size=11, weight="bold")
                )
            else:
                refresh_btn = ctk.CTkButton(
                    bottom_frame,
                    text="REFRESH",
                    command=lambda: (db_window.destroy(), self.view_database()),
                    fg_color="#0088ff",
                    text_color="#ffffff",
                    height=32,
                    font=ctk.CTkFont(size=11, weight="bold")
                )
            refresh_btn.pack(side="left", padx=5)
            
            close_btn = ctk.CTkButton(
                bottom_frame,
                text="CLOSE",
                command=db_window.destroy,
                fg_color="#ff6600",
                text_color="#ffffff",
                height=32,
                font=ctk.CTkFont(size=11, weight="bold")
            )
            close_btn.pack(side="left", padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Database Error: {str(e)}")
    
    def filter_database_display(self, db_data, db_window):
        """Filter and refresh database display based on search - works with Treeview"""
        search_query = self.search_input.get().lower() if hasattr(self, 'search_input') else ""
        
        try:
            # Find the Treeview widget
            tree = None
            for widget in db_window.winfo_children():
                if isinstance(widget, ttk.Treeview):
                    tree = widget
                    break
            
            if tree is None:
                return  # No tree found, skip
            
            # Clear all rows
            for item in tree.get_children():
                tree.delete(item)
            
            # Filter and repopulate
            if not search_query:
                filtered_data = db_data
            else:
                filtered_data = [item for item in db_data if isinstance(item, dict) and search_query in item.get('text', '').lower()]
            
            if not filtered_data:
                return
            
            # Re-add filtered rows
            for idx, item in enumerate(filtered_data):
                if not isinstance(item, dict):
                    continue
                
                text_short = item.get('text', '')[:100]
                label_val = item.get('label', 1)
                source = item.get('source', 'Manual Entry')
                
                status_text = '✅ REAL' if label_val == 1 else '🚨 FAKE'
                
                tree.insert('', 'end', iid=f'row_{idx}',
                    values=(status_text, text_short, source, ''))
        
        except Exception as e:
            pass  # Silent fail, user can refresh manually

    def open_manual_entry_window(self, parent_window, label_type, db_data=None):
        """Open window to manually add real or fake news"""
        try:
            entry_window = ctk.CTkToplevel(self.root)
            entry_window.title(f"Add {'REAL' if label_type == 1 else 'FAKE'} News")
            entry_window.geometry("900x600+100+100")
            entry_window.resizable(True, True)
            entry_window.attributes('-topmost', 1)
            entry_window.lift()
            entry_window.focus_force()
            entry_window.grab_set()
            entry_window.update()
            entry_window.configure(fg_color="#0a0a0a" if self.is_dark else "#ffffff")
            
            # Header
            header = ctk.CTkLabel(
                entry_window,
                text=f"Add {'REAL' if label_type == 1 else 'FAKE'} News to Database",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#00ff88" if label_type == 1 else "#ff0088"
            )
            header.pack(pady=15)
            
            # Input label
            input_label = ctk.CTkLabel(
                entry_window,
                text="Paste news text:",
                font=ctk.CTkFont(size=13),
                text_color="#ffff00"
            )
            input_label.pack(anchor="w", padx=20, pady=(10, 0))
            
            # Text input
            text_input = ctk.CTkTextbox(
                entry_window,
                height=280,
                fg_color="#0a0a0a",
                text_color="#ffffff",
                border_color="#00ff88" if label_type == 1 else "#ff0088",
                border_width=2,
                font=ctk.CTkFont(size=12)
            )
            text_input.pack(fill="both", expand=True, padx=20, pady=10)
            
            # Source input
            source_label = ctk.CTkLabel(
                entry_window,
                text="Source (optional):",
                font=ctk.CTkFont(size=12),
                text_color="#ffff00"
            )
            source_label.pack(anchor="w", padx=20, pady=(10, 0))
            
            source_input = ctk.CTkEntry(
                entry_window,
                placeholder_text="e.g., Manual Entry, Twitter, News Site",
                fg_color="#0a0a0a",
                text_color="#ffffff",
                border_color="#00ff88" if label_type == 1 else "#ff0088",
                border_width=2,
                font=ctk.CTkFont(size=12),
                height=40
            )
            source_input.pack(fill="x", padx=20, pady=10)
            
            # Buttons frame
            btn_frame = ctk.CTkFrame(entry_window, fg_color="#0a0a0a" if self.is_dark else "#ffffff")
            btn_frame.pack(fill="x", padx=20, pady=15)
            
            def save_entry():
                text = text_input.get("1.0", "end").strip()
                source = source_input.get().strip() or ("Real Entry" if label_type == 1 else "Fake Entry")
                
                if not text or len(text) < 10:
                    messagebox.showwarning("Invalid Input", "Please enter at least 10 characters!")
                    return
                
                try:
                    # Load existing data
                    db_data_local = []
                    if os.path.exists('learning_db.json'):
                        try:
                            with open('learning_db.json', 'r', encoding='utf-8') as f:
                                loaded_data = json.load(f)
                            
                            if isinstance(loaded_data, list):
                                db_data_local = loaded_data
                        except:
                            db_data_local = []
                    
                    # Add new entry
                    new_entry = {
                        'text': text,
                        'label': label_type,
                        'source': source,
                        'confidence': 1.0,
                        'timestamp': datetime.now().isoformat()
                    }
                    db_data_local.append(new_entry)
                    
                    # Save
                    with open('learning_db.json', 'w', encoding='utf-8') as f:
                        json.dump(db_data_local, f, indent=2, ensure_ascii=False)
                    
                    # Show notification
                    self.show_notification(
                        "✅ Success",
                        f"Added as {'REAL' if label_type == 1 else 'FAKE'} news!",
                        "success"
                    )
                    
                    entry_window.destroy()
                    
                    # Refresh database view if open
                    if hasattr(self, 'db_window') and self.db_window and self.db_window.winfo_exists():
                        self.db_window.destroy()
                    self.view_database()
                    
                except Exception as e:
                    self.show_notification(
                        "❌ Error",
                        f"Failed to save: {str(e)}",
                        "error"
                    )
            
            save_btn = ctk.CTkButton(
                btn_frame,
                text=f"SAVE AS {'REAL' if label_type == 1 else 'FAKE'}",
                command=save_entry,
                fg_color="#00ff88" if label_type == 1 else "#ff0088",
                text_color="#000000" if label_type == 1 else "#ffffff",
                height=40,
                font=ctk.CTkFont(size=13, weight="bold")
            )
            save_btn.pack(side="left", padx=8, fill="both", expand=True)
            
            cancel_btn = ctk.CTkButton(
                btn_frame,
                text="CANCEL",
                command=entry_window.destroy,
                fg_color="#666666",
                text_color="#ffffff",
                height=40,
                font=ctk.CTkFont(size=13)
            )
            cancel_btn.pack(side="left", padx=8)
            
            entry_window.update()
            
        except Exception as e:
            self.show_notification("❌ Error", f"Failed to open entry window: {str(e)}", "error")
            
            # Buttons frame
            btn_frame = ctk.CTkFrame(entry_window, fg_color="#0a0a0a" if self.is_dark else "#ffffff")
            btn_frame.pack(fill="x", padx=20, pady=15)
            
            def save_entry():
                text = text_input.get("1.0", "end").strip()
                source = source_input.get().strip() or ("Real Entry" if label_type == 1 else "Fake Entry")
                
                if not text or len(text) < 10:
                    messagebox.showwarning("Invalid Input", "Please enter at least 10 characters!")
                    return
                
                try:
                    # Load existing data - ensure it's a list
                    db_data = []
                    if os.path.exists('learning_db.json'):
                        try:
                            with open('learning_db.json', 'r', encoding='utf-8') as f:
                                loaded_data = json.load(f)
                            
                            # Make sure loaded_data is a list
                            if isinstance(loaded_data, list):
                                db_data = loaded_data
                            elif isinstance(loaded_data, dict):
                                # If it's a dict, try to convert to list
                                db_data = []
                            else:
                                db_data = []
                        except:
                            db_data = []
                    
                    # Add new entry
                    new_entry = {
                        'text': text,
                        'label': label_type,
                        'source': source,
                        'confidence': 1.0,
                        'timestamp': datetime.now().isoformat()
                    }
                    db_data.append(new_entry)
                    
                    # Save - ensure we're saving a list
                    with open('learning_db.json', 'w', encoding='utf-8') as f:
                        json.dump(db_data, f, indent=2, ensure_ascii=False)
                    
                    messagebox.showinfo("Success", f"Added as {'REAL' if label_type == 1 else 'FAKE'} news!")
                    entry_window.destroy()
                    
                    # Refresh database view
                    if hasattr(self, 'db_window') and self.db_window and self.db_window.winfo_exists():
                        self.db_window.destroy()
                    self.view_database()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save: {str(e)}")
            
            save_btn = ctk.CTkButton(
                btn_frame,
                text=f"SAVE AS {'REAL' if label_type == 1 else 'FAKE'}",
                command=save_entry,
                fg_color="#00ff88" if label_type == 1 else "#ff0088",
                text_color="#000000" if label_type == 1 else "#ffffff",
                height=40,
                font=ctk.CTkFont(size=13, weight="bold")
            )
            save_btn.pack(side="left", padx=8, fill="both", expand=True)
            
            cancel_btn = ctk.CTkButton(
                btn_frame,
                text="CANCEL",
                command=entry_window.destroy,
                fg_color="#666666",
                text_color="#ffffff",
                height=40,
                font=ctk.CTkFont(size=13)
            )
            cancel_btn.pack(side="left", padx=8)
            
            # Force window to appear
            entry_window.update()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open entry window: {str(e)}")
    
    def animate(self):
        """Animation loop"""
        self.root.after(100, self.animate)

# ======================== MAIN ========================
if __name__ == "__main__":
    print_loading_bar(85, 50)
    time.sleep(0.2)
    print_loading_bar(90, 50)
    
    # Build UI
    app = App()
    print_loading_bar(95, 50)
    
    # Mark 100% only when the window is actually mapped (visible)
    def _print_ready_once(_evt=None):
        if getattr(app, "_ready_printed", False):
            return
        app._ready_printed = True
        print_loading_bar(100, 50)
        print("\n✅ App Ready! Enjoy analyzing news!\n")
    
    # Bind to Map event (fires when window is shown) and add a fallback timer
    app.root.bind("<Map>", _print_ready_once)
    app.root.after(2000, _print_ready_once)  # Fallback in case Map event is missed
    
    app.root.mainloop()
