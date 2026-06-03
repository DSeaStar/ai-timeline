#!/usr/bin/env python3
"""Upload files to GitHub repo via API."""

import base64
import json
import os
import urllib.request
import urllib.error

TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = "DSeaStar"
REPO = "ai-timeline"
BRANCH = "main"

def upload_file(path, content, message):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path}"
    data = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": BRANCH
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"token {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json"
        },
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"✓ Created: {path}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body:
            print(f"⚠ Exists: {path}")
            return True
        print(f"✗ Failed: {path} - {e.code} {body[:200]}")
        return False

def main():
    import glob
    
    files = []
    for f in glob.glob("**/*", recursive=True):
        if os.path.isfile(f) and ".git" not in f:
            files.append(f)
    
    print(f"Uploading {len(files)} files...")
    for f in sorted(files):
        with open(f, "r", encoding="utf-8") as fh:
            content = fh.read()
        upload_file(f, content, f"feat: add {f}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
