import requests
import json
import csv
import time
import argparse
import re
from tqdm import tqdm

def clean_text(text):
    # Loại bỏ ký tự không hiển thị và thay thế ký tự lạ
    text = text.encode("utf-8", "ignore").decode("utf-8")
    text = re.sub(r"[\r\n\t]+", " ", text)  # bỏ dòng và tab
    text = re.sub(r"\s+", " ", text).strip()
    return text

def scrape_guardian_api(max_articles=100, delay=1.0, api_key="--apikey 144e2ad7-f300-498d-9f7e-4ae0b95938f8"):
    url = "https://content.guardianapis.com/search"
    params = {
        "section": "football",
        "page-size": 50,
        "show-fields": "headline,bodyText",
        "api-key": api_key
    }

    articles = []
    page = 1
    pbar = tqdm(total=max_articles, desc="Articles")

    while len(articles) < max_articles:
        params["page"] = page
        response = requests.get(url, params=params)
        data = response.json()

        results = data.get("response", {}).get("results", [])
        if not results:
            print("❌ No more results found.")
            break

        for item in results:
            headline = clean_text(item["fields"]["headline"])
            link = item["webUrl"]
            content = clean_text(item["fields"]["bodyText"])

            articles.append({
                "title": headline,
                "url": link,
                "content": content
            })

            pbar.update(1)
            if len(articles) >= max_articles:
                break

            time.sleep(delay)

        page += 1

    pbar.close()

    # Save JSONL (UTF-8 chuẩn)
    with open("articles.jsonl", "w", encoding="utf-8") as f:
        for art in articles:
            f.write(json.dumps(art, ensure_ascii=False) + "\n")

    # Save CSV (UTF-8 BOM để Excel mở không lỗi font)
    with open("articles.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "content"])
        writer.writeheader()
        writer.writerows(articles)

    print(f"✅ Saved {len(articles)} articles -> articles.jsonl, articles.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=100)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--apikey", type=str, required=True)
    args = parser.parse_args()

    scrape_guardian_api(args.max, args.delay, args.apikey)
