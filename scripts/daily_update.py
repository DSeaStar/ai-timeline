#!/usr/bin/env python3
"""Daily AI news fetcher and timeline updater."""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Config
REPO_DIR = Path(__file__).parent.parent
DATA_DIR = REPO_DIR / "data"
TIMELINE_DIR = REPO_DIR / "timeline"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USER = "DSeaStar"
REPO_NAME = "ai-timeline"

# AI news RSS sources
RSS_SOURCES = [
    "https://www.reddit.com/r/artificial/hot.json?limit=10",
    "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI&hitsPerPage=10",
]

def fetch_reddit_ai_news():
    """Fetch hot posts from r/artificial."""
    import urllib.request
    import urllib.error
    
    url = "https://www.reddit.com/r/artificial/hot.json?limit=10"
    req = urllib.request.Request(url, headers={"User-Agent": "AI-Timeline-Bot/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        
        news = []
        for post in data.get("data", {}).get("children", []):
            p = post["data"]
            news.append({
                "title": p["title"],
                "url": f"https://reddit.com{p['permalink']}",
                "score": p["score"],
                "date": datetime.fromtimestamp(p["created_utc"], tz=timezone.utc).strftime("%Y-%m-%d"),
            })
        return news
    except Exception as e:
        print(f"Reddit fetch failed: {e}")
        return []

def fetch_hackernews_ai():
    """Fetch AI-related stories from Hacker News."""
    import urllib.request
    
    url = "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI%20OR%20LLM%20OR%20GPT%20OR%20model&hitsPerPage=10"
    req = urllib.request.Request(url, headers={"User-Agent": "AI-Timeline-Bot/1.0"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        
        news = []
        for hit in data.get("hits", []):
            news.append({
                "title": hit["title"],
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
                "score": hit.get("points", 0),
                "date": datetime.fromtimestamp(hit["created_at_i"], tz=timezone.utc).strftime("%Y-%m-%d"),
            })
        return news
    except Exception as e:
        print(f"Hacker News fetch failed: {e}")
        return []

def categorize_event(title):
    """Auto-categorize based on title keywords."""
    title_lower = title.lower()
    
    if any(k in title_lower for k in ["video", "sora", "runway", "pika", "kling", "veo"]):
        return "video"
    elif any(k in title_lower for k in ["image", "dall-e", "midjourney", "stable diffusion", "imagen"]):
        return "image"
    elif any(k in title_lower for k in ["speech", "audio", "whisper", "tts", "voice", "music", "suno"]):
        return "speech"
    elif any(k in title_lower for k in ["paper", "research", "arxiv", "study", "benchmark"]):
        return "research"
    elif any(k in title_lower for k in ["policy", "regulation", "law", "gov", "eu ai act"]):
        return "policy"
    elif any(k in title_lower for k in ["funding", "invest", "acquisition", "billion", "ipo"]):
        return "business"
    else:
        return "llm"

def load_existing_events(year):
    """Load existing events for a year."""
    file_path = DATA_DIR / f"{year}.yml"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    return []

def save_events(year, events):
    """Save events to YAML file."""
    file_path = DATA_DIR / f"{year}.yml"
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(events, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

def generate_markdown():
    """Regenerate all timeline markdown files."""
    sys.path.insert(0, str(REPO_DIR / "scripts"))
    from generate_timeline import main as gen_main
    gen_main()

def commit_and_push():
    """Commit and push to GitHub."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Configure git if needed
    subprocess.run(["git", "config", "user.email", "bot@ai-timeline.local"], cwd=REPO_DIR, capture_output=True)
    subprocess.run(["git", "config", "user.name", "AI Timeline Bot"], cwd=REPO_DIR, capture_output=True)
    
    # Add, commit, push
    subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, check=True)
    result = subprocess.run(["git", "commit", "-m", f"daily: AI news update {today}"], cwd=REPO_DIR, capture_output=True, text=True)
    
    if result.returncode != 0 and "nothing to commit" not in result.stdout.lower() and "nothing to commit" not in result.stderr.lower():
        print(f"Commit failed: {result.stderr}")
        return False
    
    # Push with token if available
    if GITHUB_TOKEN:
        remote_url = f"https://{GITHUB_USER}:{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=REPO_DIR, capture_output=True)
    
    result = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Push failed: {result.stderr}")
        return False
    
    print("✓ Pushed to GitHub")
    return True

def main():
    """Main daily update routine."""
    print(f"=== AI Timeline Daily Update: {datetime.now().isoformat()} ===")
    
    # Fetch news from multiple sources
    all_news = []
    all_news.extend(fetch_reddit_ai_news())
    all_news.extend(fetch_hackernews_ai())
    
    # Sort by score (popularity) and filter today only
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_news = [n for n in all_news if n["date"] == today_str]
    today_news.sort(key=lambda x: x["score"], reverse=True)
    
    if not today_news:
        print("No AI news found for today.")
        return
    
    print(f"Found {len(today_news)} AI news items for today")
    
    # Convert to timeline events
    year = datetime.now().year
    existing_events = load_existing_events(year)
    existing_titles = {e["title"] for e in existing_events}
    
    new_events = []
    for news in today_news[:5]:  # Top 5 most popular
        if news["title"] in existing_titles:
            continue
        
        event = {
            "date": news["date"],
            "title": news["title"],
            "category": categorize_event(news["title"]),
            "description": f"Source: {news['url']}",
            "links": [{"text": "Source", "url": news["url"]}],
            "tags": ["auto-fetched"],
        }
        new_events.append(event)
        print(f"  + {news['title'][:60]}... [{event['category']}]")
    
    if not new_events:
        print("No new events to add.")
        return
    
    # Save and regenerate
    existing_events.extend(new_events)
    save_events(year, existing_events)
    print(f"\nSaved {len(new_events)} new events to data/{year}.yml")
    
    generate_markdown()
    print("Regenerated timeline markdown files")
    
    # Commit and push
    commit_and_push()
    
    print("\nDone!")

if __name__ == "__main__":
    main()
