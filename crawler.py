import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sites.google.com/lisarogers.org/songs-a-lot/home"

from urllib.parse import urljoin

def get_page_links(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        if full_url.startswith(base_url):
            links.append(full_url)
            print(f"Scanning {url} — found {len(videos)} videos")
    return list(set(links))

def extract_videos(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    videos = []
    for tag in soup.find_all(["iframe", "embed", "video"]):
        src = tag.get("src") or tag.get("data-src")
        if src and any(domain in src for domain in ["youtube.com", "vimeo.com", "drive.google.com"]):
            videos.append((url, src))
    return videos

all_links = get_page_links(BASE_URL)
video_list = []
for link in all_links:
    video_list.extend(extract_videos(link))

print("Pages found:", all_links)
print("Videos found:", video_list)

if not video_list:
    html += "<p>No videos found. Check your Google Site or crawler settings.</p>"

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
