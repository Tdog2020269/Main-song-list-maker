from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://sites.google.com/lisarogers.org/songs-a-lot/home"

def get_page_links(page, base_url):
    page.goto(base_url)
    soup = BeautifulSoup(page.content(), "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            links.append(href)
    return list(set(links))

def extract_videos(page, url):
    page.goto(url)
    soup = BeautifulSoup(page.content(), "html.parser")
    videos = []
    for tag in soup.find_all(["iframe", "embed", "video", "a"]):
        src = tag.get("src") or tag.get("href") or tag.get("data-src")
        if src and any(domain in src for domain in [
            "youtube.com",
            "youtubeeducation.com",
            "vimeo.com",
            "drive.google.com"
        ]):
            videos.append((url, src))
    print(f"Scanning {url} — found {len(videos)} videos")
    return videos

video_list = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    all_links = get_page_links(page, BASE_URL)
    print("Total pages scanned:", len(all_links))
    for link in all_links:
        video_list.extend(extract_videos(page, link))
    print("Total videos found:", len(video_list))
    browser.close()

# Build HTML
html = """
<html>
<head>
<title>Video Index</title>
<style>
    body { font-family: Arial; padding: 20px; }
    .video-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
    .video-box { width: 480px; }
    iframe { width: 100%; height: 270px; border: none; }
    a { font-size: 0.9em; color: #555; text-align: center; margin-top: 5px; display: block; }
</style>
</head>
<body>
<h1>Video Index</h1>
<div class="video-container">
"""

for page_url, video in video_list:
    html += f"""
    <div class="video-box">
        <iframe src="{video}" allowfullscreen></iframe>
        <a href="{page_url}" target="_blank">{page_url}</a>
    </div>
    """

html += """
</div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
    
print("index.html written with", html.count("<iframe"), "videos")
