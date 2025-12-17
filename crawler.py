import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sites.google.com/lisarogers.org/songs-a-lot/song-sorting-stuff/albums"

def get_page_links(base_url):
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(base_url):
            links.append(href)
    return list(set(links))

def extract_videos(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    videos = []
    for iframe in soup.find_all("iframe"):
        src = iframe.get("src", "")
        if "youtube.com" in src or "vimeo.com" in src or "drive.google.com" in src:
            videos.append((url, src))
    return videos

all_links = get_page_links(BASE_URL)
video_list = []
for link in all_links:
    video_list.extend(extract_videos(link))

# Build HTML
html = "<html><head><title>Video Index</title></head><body><h1>Video Index</h1><ul>"
for page, video in video_list:
    html += f"<li><a href='{video}' target='_blank'>{video}</a> (from {page})</li>"
html += "</ul></body></html>"

with open("index.html", "w") as f:
    f.write(html)
