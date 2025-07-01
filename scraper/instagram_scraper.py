import os, re, pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()                       # pulls API_KEY + CSE_ID
API_KEY = os.getenv("API_KEY")
CSE_ID  = os.getenv("CSE_ID")

EMAIL_RE  = re.compile(r"[\w\.-]+@gmail\.com", re.I)
PHONE_RE  = re.compile(r"\+?\d[\d\s\-]{9,15}")

def _extract(snippet: str):
    email = EMAIL_RE.search(snippet)
    phone = PHONE_RE.search(snippet)
    return {
        "Email":  email.group(0).lower() if email else None,
        "Phone":  phone.group(0).replace(" ", "") if phone else None,
    }

def google_search(query: str, limit: int = 30):
    service = build("customsearch", "v1", developerKey=API_KEY)
    start, hits = 1, []
    while len(hits) < limit and start <= 90:
        result = service.cse().list(q=query, cx=CSE_ID, num=10, start=start).execute()
        for item in result.get("items", []):
            contact = _extract(item.get("snippet", ""))
            if contact["Email"]:
                hits.append({
                    "Title": item.get("title"),
                    "Link":  item.get("link"),
                    **contact,
                    "Fetched": datetime.utcnow().isoformat()
                })
        start += 10
    return pd.DataFrame(hits)

def save_excel(df: pd.DataFrame, filename: str) -> str:
    os.makedirs("leads", exist_ok=True)
    path = f"leads/{filename}.xlsx"
    df.to_excel(path, index=False)
    return path
