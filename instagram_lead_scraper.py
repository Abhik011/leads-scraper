import os
import re
from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
import argparse

# Load .env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
CSE_ID = os.getenv("CSE_ID")

# Corrected Regular expressions
EMAIL_REGEX = re.compile(r"[\w\.-]+@gmail\.com", re.I)
PHONE_REGEX = re.compile(r"\+?\d[\d\s\-]{9,15}")

def extract_contacts(snippet):
    email = EMAIL_REGEX.search(snippet)
    phone = PHONE_REGEX.search(snippet)
    return {
        "Email": email.group(0) if email else None,
        "Phone": phone.group(0).replace(" ", "") if phone else None
    }

def google_search(query, max_results):
    service = build("customsearch", "v1", developerKey=API_KEY)
    start = 1
    results = []
    while len(results) < max_results and start <= 90:
        res = service.cse().list(q=query, cx=CSE_ID, num=10, start=start).execute()
        items = res.get("items", [])
        for item in items:
            contact = extract_contacts(item.get("snippet", ""))
            if contact["Email"]:
                results.append({
                    "Title": item.get("title"),
                    "Link": item.get("link"),
                    "Email": contact["Email"],
                    "Phone": contact["Phone"],
                    "Fetched At": datetime.utcnow().isoformat()
                })
        start += 10
    return results

def save_to_csv(results, filename):
    df = pd.DataFrame(results)
    os.makedirs("leads", exist_ok=True)
    path = f"leads/{filename}.csv"
    if os.path.exists(path):
        existing = pd.read_csv(path)
        df = pd.concat([existing, df]).drop_duplicates(subset="Email")
    df.to_csv(path, index=False)
    print(f"✅ Saved {len(df)} unique leads to {path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profession", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--max", type=int, default=30)
    args = parser.parse_args()

    query = f'site:instagram.com "{args.profession}" "{args.location}" "@gmail.com"'
    results = google_search(query, args.max)
    if not results:
        print("⚠️ No results found.")
    else:
        filename = f"{args.profession.replace(' ', '_')}_{args.location.replace(' ', '_')}"
        save_to_csv(results, filename)

if __name__ == "__main__":
    main()
