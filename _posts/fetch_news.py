import feedparser
import os
from datetime import datetime
import hashlib

KEYWORDS = ["World Cup 2026", "World Cup", "WC2026", "FIFA World Cup", "Bóng đá thế giới 2026", "World Cup 2026"]
RSS_FEEDS = [
    "https://vnexpress.net/rss/the-thao.rss",
    "https://tuoitre.vn/rss/the-thao.rss",
    "https://thanhnien.vn/rss/the-thao.rss",
    "https://news.google.com/rss/search?q=World+Cup+2026+lang:vi&hl=vi&gl=VN&ceid=VN:vi",  # Google News VN
]

def get_existing_posts():
    posts = set()
    for f in os.listdir("_posts"):
        if f.endswith(".md"):
            posts.add(f)
    return posts

def create_md_post(item):
    title = item.title
    link = item.link
    pub_date = item.published if hasattr(item, 'published') else datetime.now().isoformat()
    summary = item.summary if hasattr(item, 'summary') else ""
    
    if not any(kw.lower() in (title + summary).lower() for kw in KEYWORDS):
        return None
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = hashlib.md5(title.encode()).hexdigest()[:10]
    filename = f"_posts/{date_str}-wc-{slug}.md"
    
    content = f"""---
title: {title}
date: {pub_date}
categories: worldcup
---

{summary}

**Nguồn:** [{link}]({link})
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def main():
    existing = get_existing_posts()
    new_count = 0
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            md = create_md_post(entry)
            if md and os.path.basename(md) not in existing:
                new_count += 1
                print(f"New post: {md}")
    print(f"Added {new_count} new posts")

if __name__ == "__main__":
    main()
