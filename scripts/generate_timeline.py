#!/usr/bin/env python3
"""Generate timeline Markdown files from YAML data."""

import yaml
import glob
from pathlib import Path
from datetime import datetime

CATEGORY_EMOJI = {
    "llm": "📝",
    "image": "🎨",
    "video": "🎬",
    "speech": "🎵",
    "research": "🔬",
    "policy": "⚖️",
    "business": "💼",
}

CATEGORY_NAME = {
    "llm": "大语言模型",
    "image": "文生图",
    "video": "文生视频",
    "speech": "语音/音频",
    "research": "研究突破",
    "policy": "政策监管",
    "business": "商业动态",
}

def generate_timeline(year, events):
    """Generate Markdown for a year."""
    lines = [f"# {year} 年 AI 时间线\n", f"共 {len(events)} 个事件\n"]
    
    # Sort by date
    events = sorted(events, key=lambda x: x.get("date", ""))
    
    for event in events:
        date = event.get("date", "")
        title = event.get("title", "")
        category = event.get("category", "")
        description = event.get("description", "")
        links = event.get("links", [])
        tags = event.get("tags", [])
        
        emoji = CATEGORY_EMOJI.get(category, "📌")
        cat_name = CATEGORY_NAME.get(category, category)
        
        lines.append(f"## {emoji} {date} — {title}\n")
        lines.append(f"**分类：** {cat_name}  |  **标签：** {', '.join(tags)}\n")
        lines.append(f"{description}\n")
        
        if links:
            lines.append("**相关链接：**")
            for link in links:
                lines.append(f"- [{link['text']}]({link['url']})")
            lines.append("")
        
        lines.append("---\n")
    
    return "\n".join(lines)

def main():
    data_dir = Path("data")
    timeline_dir = Path("timeline")
    timeline_dir.mkdir(exist_ok=True)
    
    # Read all YAML files
    for yaml_file in sorted(data_dir.glob("*.yml")):
        year = yaml_file.stem
        with open(yaml_file, "r", encoding="utf-8") as f:
            events = yaml.safe_load(f) or []
        
        markdown = generate_timeline(year, events)
        output_file = timeline_dir / f"{year}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        print(f"Generated: {output_file} ({len(events)} events)")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
