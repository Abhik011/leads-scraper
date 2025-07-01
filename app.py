import streamlit as st
from scraper.instagram_scraper import google_search, save_excel

st.title("📈 Instagram Lead Scraper")

prof   = st.text_input("Profession / Keyword", "interior designer")
loc    = st.text_input("Location", "India")
limit  = st.slider("Max Google results", 10, 100, 30)

if st.button("Run Scraper"):
    with st.spinner("Fetching leads…"):
        query = f'site:instagram.com "{prof}" "{loc}" "@gmail.com"'
        df    = google_search(query, limit)
    if df.empty:
        st.warning("No leads found.")
    else:
        st.success(f"Found {len(df)} leads 🎉")
        st.dataframe(df, use_container_width=True)

        excel = save_excel(df, f"{prof.replace(' ','_')}_{loc}")
        with open(excel, "rb") as f:
            st.download_button("⬇️ Download Excel", f,
                               file_name="instagram_leads.xlsx")
