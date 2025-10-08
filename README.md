📰 Newspulse
An Interactive Streamlit App for Live News Exploration, Analysis, and Conversational Insights (Gemini-Powered)
________________________________________
📘 Overview
Newspulse is an AI-driven Streamlit platform that allows users to fetch, explore, and analyze live news in real time — now enhanced with an integrated Gemini-powered chatbot assistant.
You can not only read and analyze the latest headlines but also chat with the Gemini Bot to summarize, interpret, and discuss current events conversationally.
________________________________________
🚀 Features
🔹 Live News Fetching
•	Fetches current headlines across popular categories:
o	Entertainment, Business, Sports, Technology
•	Uses GNews API for up-to-date news feeds.
🔹 Keyword Search
•	Type any keyword to fetch the 10 most recent matching articles.
•	Displays title, source, and URL with clickable links.
🔹 Article Cards
•	Each article shows:
o	Thumbnail image
o	Title and short summary
o	Source name and external URL
🔹 One-Click NLP Analysis
•	Analyze any article instantly:
o	Sentiment Analysis (positive / negative / neutral)
o	Tokenization and Bigram extraction
o	Named Entity Recognition (NER) via spaCy
🔹 Overall Insights
•	Visualize patterns and trends across multiple articles:
o	Sentiment distribution plots
o	Frequent words and entities
o	Aggregated statistics
________________________________________
🤖 NewsPulse Bot (Gemini AI Assistant)
The NewsPulse Bot is an intelligent chat assistant powered by Google’s Gemini API.
It helps users interact naturally with the news data — asking questions, generating summaries, or explaining context directly inside the Streamlit app.
💡 Capabilities
•	Summarize news headlines or articles
•	Explain topics, organizations, or public figures mentioned in articles
•	Answer queries like “What’s trending in technology today?”
•	Compare sentiment or tone across fetched stories
•	Maintains chat context during the session for smooth interactions
🧠 Powered by
•	Google Generative AI SDK (google-generativeai)
•	Requires a valid Gemini API key (GEMINI_API_KEY)
Example Prompts
🗣️ “Summarize today’s finance headlines.”
🗣️ “Explain why AI startups are in the news today.”
🗣️ “What’s the sentiment around Indian stock market updates?”
________________________________________
🧠 Tech Stack
Layer	Tools / Libraries
Frontend/UI	Streamlit
APIs & Integration	requests, GNews API (GNEWS_API_KEY)
Chatbot Engine	Gemini API (google-generativeai)
NLP Processing	spaCy, NLTK, transformers, torch
Data & Visualization	pandas, matplotlib, seaborn, plotly
Utilities	tqdm, orjson, feedparser
Auth & Storage (scaffolded)	bcrypt, pymongo[srv], python-dotenv
________________________________________
🗂️ Project Structure
newspulse2/
│
├── newspulse/
│   ├── app.py                     # Streamlit entry point
│   ├── newsapi_fetch.py           # CLI script for NewsAPI keyword search
│   ├── requirements.txt
│   │
│   └── newspulse_pkg/
│       ├── __init__.py
│       ├── auth.py                # Authentication helpers
│       ├── bot.py                 # Gemini-based chatbot assistant
│       ├── config.py              # Environment/config helpers
│       ├── ingestion.py           # Data ingestion utilities
│       ├── ner.py                 # Entity extraction (spaCy)
│       ├── news_api.py            # GNews integration (category + keyword)
│       ├── news_ui.py             # Streamlit UI components
│       ├── preprocessing.py       # Text cleaning, tokenization, n-grams
│       ├── sentiment.py           # Sentiment prediction
│       ├── utils.py               # Misc helpers
│       └── viz.py                 # Plotting utilities
________________________________________
⚙️ Setup Instructions
# 1. Clone repository
git clone https://github.com/<your-username>/newspulse.git
cd newspulse2/newspulse

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add environment variables in .env
GNEWS_API_KEY=your_gnews_api_key
GEMINI_API_KEY=your_gemini_api_key

# 5. Run the Streamlit app
streamlit run app.py
________________________________________
🧩 Future Enhancements
•	Contextual multi-turn chat memory for the Gemini Bot
•	Article summarization across multiple sources
•	Multilingual support for non-English news
•	Voice-based interaction support
•	Custom Gemini prompt templates for different analysis modes

