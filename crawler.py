from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

BASE_URL = "https://sites.google.com/view/ngangs-lab/"

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
    for tag in soup.find_all(["iframe", "embed", "video"]):
        src = tag.get("src") or tag.get("data-src")
        if src and any(domain in src for domain in ["youtube.com", "vimeo.com", "drive.google.com"]):
            videos.append((url, src))
    print(f"Scanning {url} — found {len(videos)} videos")
    return videos

video_list = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    all_links = get_page_links(page, BASE_URL)
    for link in all_links:
        video_list.extend(extract_videos(page, link))
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
    a { font-size: 0.9em; color: #555; text-align: center; margin-top: 5px; }
</style>
</head>
<body>
<h1>Video Index</h1>
<div class="video-container">
"""

for page, video in video_list:
    html += f"""
    <div class="video-box">
        <iframe src="{video}" allowfullscreen></iframe>
        <a href="{page}" target="_blank">{page}</a>
    </div>
    """

html += """
</div>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

# Build HTML
html = """
<html>
  <head>
    <title>Video Index</title>
    <style>
      body { font-family: Arial; padding: 20px; }
      h1 { text-align: center; }
      .video-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }
      .video-box { width: 300px; }
      iframe { width: 100%; height: 170px; border: none; }
      .source { font-size: 0.9em; color: #555; text-align: center; margin-top: 5px; }
    </style>
  </head>
  <body>
    <h1>Video Index</h1>
    <div class="video-container">
"""

for page, video in video_list:
    html += f"""
      <div class="video-box">
        <iframe src="{video}" allowfullscreen></iframe>
        <div class="source">From: <a href="{page}" target="_blank">{page}</a></div>
      </div>
    """

html += """
    </div>
  </body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)
