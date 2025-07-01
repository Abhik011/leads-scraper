### Quickstart (local)

```bash
git clone https://github.com/you/instagram-lead-scraper-web.git
cd instagram-lead-scraper-web
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your keys
streamlit run app.py
