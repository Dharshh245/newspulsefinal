# NEWPULSE
Newspulse Documantation 
Content (What the app does)
Interactive Streamlit app to fetch, explore, and analyze live news.
Category-based headlines (entertainment, finance, business, technology) from GNews.
Keyword search bar to fetch top 10 latest articles dynamically.
Per-article quick analysis (sentiment, tokens, bigrams, named entities).
Overall analysis across fetched articles (sentiment distribution, word frequencies, entities).
Features
Live news fetching: Pulls current headlines by category.
Keyword search: Type a term to get the 10 most recent articles; shows title, source, and URL.
Article cards: Image, title, description, and source/URL metadata.
One-click analysis: Per-article sentiment + tokens, bigrams, entities.
Overall insights: Distribution plots and tables for the fetched batch.
Session state: Keeps fetched data and analysis selections.
Graceful errors: Clear messages for missing API keys, rate limits, no results, or network issues.

Tech Used
Frontend: Streamlit.
HTTP/Integration: requests, GNews API (via GNEWS_API_KEY). Standalone script for NewsAPI.org is included (newsapi_fetch.py).
NLP: spaCy, NLTK, transformers, torch.
Data/Plots: pandas, matplotlib, seaborn, plotly.
Utils: tqdm, orjson, feedparser.
Auth/Storage (scaffolded): bcrypt, pymongo[srv], python-dotenv.

Project Structure (VS Code)
newspulse2/
  newspulse/
    newspulse/
      app.py                    # Streamlit entry point
      newsapi_fetch.py          # Standalone CLI script for NewsAPI.org keyword search
      requirements.txt
      newspulse_pkg/
        __init__.py
        auth.py                 # Auth helpers
        config.py               # Config/env helpers
        ingestion.py            # Data ingestion utilities
        ner.py                  # Entity extraction (spaCy)
        news_api.py             # GNews integration (category + keyword search)
        news_ui.py              # Streamlit UI components (live news UI, keyword search UI)
        preprocessing.py        # Text cleaning, tokenization, n-grams
        sentiment.py            # Sentiment prediction
        utils.py                # Misc helpers
        viz.py                  # Plotting utilities (plotly/matplotlib)
