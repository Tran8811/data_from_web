import requests
from bs4 import BeautifulSoup

# Sitemap chính
MAIN_SITEMAP = "https://www.skysports.com/sitemap.xml"

resp = requests.get(MAIN_SITEMAP)
soup = BeautifulSoup(resp.text, "xml")

f1_sitemaps = []
for loc in soup.find_all("loc"):
    url = loc.text
    if "f1" in url.lower():
        f1_sitemaps.append(url)

print("Các sitemap F1 tìm thấy:")
for u in f1_sitemaps:
    print(u)
