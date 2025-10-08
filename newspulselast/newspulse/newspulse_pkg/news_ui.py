from __future__ import annotations

from typing import Dict, List

import streamlit as st

from .news_api import fetch_news_category, NewsApiError, search_gnews
from .sentiment import predict_sentiment
from .preprocessing import preprocess_texts, compute_top_frequencies, compute_top_bigrams
from .ner import extract_entities_spacy
from .viz import plotly_sentiment_distribution, plotly_word_frequencies, entities_count_table, plotly_bigrams, plotly_entity_labels

# Safe optional import for Gemini helper
try:
	from .gemini import summarize_with_context, GeminiNotConfigured  # type: ignore
except Exception:
	# Fallbacks so exception handlers and guards work even if dependency is missing
	summarize_with_context = None  # type: ignore[assignment]
	class GeminiNotConfigured(Exception):  # type: ignore[no-redef]
		pass


def _ensure_state():
	if "news_articles" not in st.session_state:
		st.session_state["news_articles"] = {
			"entertainment": [],
			"finance": [],
			"sports": [],
			"technology": [],
		}
	if "news_search_results" not in st.session_state:
		st.session_state["news_search_results"] = []
	if "news_search_query" not in st.session_state:
		st.session_state["news_search_query"] = ""
	if "news_article_sentiments" not in st.session_state:
		st.session_state["news_article_sentiments"] = {}
	if "news_overall_sentiments" not in st.session_state:
		st.session_state["news_overall_sentiments"] = []
	if "open_article_analysis" not in st.session_state:
		st.session_state["open_article_analysis"] = None
	if "article_chatbot_answers" not in st.session_state:
		st.session_state["article_chatbot_answers"] = {}


def _section_header(title: str, subtitle: str | None = None):
	st.markdown(
		f"""
		<div style="
			padding: 0.6rem 1rem;
			background: linear-gradient(90deg, #5B8DEF, #9b5de5);
			border-radius: 12px;
			color: white;
			margin-bottom:0.8rem;
			box-shadow: 0 4px 14px rgba(0,0,0,.25);
		">
			<h3 style="margin:0; color:white;">{title}</h3>
			{f"<div style='font-size:0.9rem; opacity:0.9;'>{subtitle}</div>" if subtitle else ""}
		</div>
		""",
		unsafe_allow_html=True,
	)


def _render_overall_summary():
	_section_header("📊 Overall Analysis", "Run analysis to see the current batch trends.")
	sentiments = st.session_state.get("news_overall_sentiments", [])
	overall_freq = st.session_state.get("news_overall_freq", [])
	overall_entities = st.session_state.get("news_overall_entities", [])
	col1, col2 = st.columns(2)
	with col1:
		if sentiments:
			fig = plotly_sentiment_distribution(sentiments)
			if fig:
				st.plotly_chart(fig, use_container_width=True, key="overall_sentiment_chart")
		else:
			st.info("No overall sentiments yet.")
	with col2:
		if overall_freq:
			figf = plotly_word_frequencies(overall_freq)
			if figf:
				st.plotly_chart(figf, use_container_width=True, key="overall_freq_chart")
		else:
			st.info("No word frequency yet.")
	# Advanced: bigrams and entity label distribution
	adv1, adv2 = st.columns(2)
	with adv1:
		if overall_freq:
			arts = st.session_state.get("news_articles", {})
			texts = [a.get("content") or a.get("description") or a.get("title") for v in arts.values() for a in v]
			texts = [t for t in texts if t]
			pp = preprocess_texts(texts)
			bigrams = compute_top_bigrams([r["tokens"] for r in pp], top_k=20)
			figb = plotly_bigrams(bigrams)
			if figb:
				st.plotly_chart(figb, use_container_width=True, key="overall_bigrams_chart")
	with adv2:
		if overall_entities:
			fige = plotly_entity_labels(overall_entities)
			if fige:
				st.plotly_chart(fige, use_container_width=True, key="overall_entity_labels_chart")
	if overall_entities:
		st.markdown("### 🏷 Entities (Top)")
		tbl = entities_count_table(overall_entities)
		st.dataframe(tbl.head(50), use_container_width=True)


def _update_overall_sentiment():
	all_articles: List[Dict] = []
	arts = st.session_state.get("news_articles", {})
	for cat, lst in arts.items():
		all_articles.extend(lst)
	contents = [a.get("content") or a.get("description") or a.get("title") for a in all_articles]
	contents = [c for c in contents if c]
	if not contents:
		st.session_state["news_overall_sentiments"] = []
		st.session_state["news_overall_freq"] = []
		st.session_state["news_overall_entities"] = []
		return
	pp = preprocess_texts(contents)
	tokens_list = [r["tokens"] for r in pp]
	st.session_state["news_overall_freq"] = compute_top_frequencies(tokens_list, top_k=25)
	ents = extract_entities_spacy([r["raw"] for r in pp])
	st.session_state["news_overall_entities"] = ents
	st.session_state["news_overall_sentiments"] = predict_sentiment([r["clean"] or r["raw"] for r in pp])


def _render_article_card(article: Dict, category: str, index: int):
	with st.container():
		st.markdown("<div class='card'>", unsafe_allow_html=True)
		cols = st.columns([1, 3])
		image_url = (article.get("image") or "").strip()
		title = article.get("title") or ""
		description = article.get("description") or ""
		url_ = (article.get("url") or "").strip()
		source = article.get("source") or ""
		article_id = (article.get("id") or f"{category}-{index}")
		with cols[0]:
			if image_url:
				st.image(image_url, use_container_width=True)
			else:
				st.caption("📷 No image")
		with cols[1]:
			st.markdown(f"**{title}**")
			if description:
				st.write(description)
			meta = " | ".join([part for part in [source, url_] if part])
			if meta:
				st.caption(meta)
			if st.button("🔎 Analyze", key=f"sent_{category}_{index}"):
				text = (article.get("content") or description or title)
				if text:
					res = predict_sentiment([text])[0]
					pp = preprocess_texts([text])
					tokens = pp[0]["tokens"] if pp else []
					freq = compute_top_frequencies([tokens], top_k=15)
					bigrams = compute_top_bigrams([tokens], top_k=10)
					ents = extract_entities_spacy([text])[0]
					st.session_state["news_article_sentiments"][article_id] = res
					st.session_state["open_article_analysis"] = {
						"title": title,
						"sent": res,
						"freq": freq,
						"bigrams": bigrams,
						"ents": ents,
					}
			if st.session_state.get("open_article_analysis") and st.session_state["open_article_analysis"].get("title") == title:
				data = st.session_state["open_article_analysis"]
				with st.expander("📑 Article Analysis", expanded=True):
					c1, c2 = st.columns(2)
					with c1:
						label = str(data["sent"].get("label", "")).capitalize()
						score = float(data["sent"].get("score", 0.0))
						st.markdown(f"**Sentiment:** {label} ({score:.2f})")
						ents = data.get("ents") or []
						if ents:
							st.markdown("#### 🏷 Entities")
							st.write(", ".join(sorted({e.get("text") for e in ents})))
						else:
							st.caption("No entities detected.")
					with c2:
						fig = plotly_word_frequencies(data.get("freq") or [])
						if fig:
							st.plotly_chart(fig, use_container_width=True, key=f"art_{category}_{index}_freq")
						figb = plotly_bigrams(data.get("bigrams") or [])
					if figb:
							st.plotly_chart(figb, use_container_width=True, key=f"art_{category}_{index}_bigrams")
					st.button("❌ Close", key=f"close_{category}_{index}", on_click=lambda: st.session_state.update({"open_article_analysis": None}))
			# Per-article chatbot input
			st.divider()
			chat_key = f"chat_{category}_{index}"
			user_msg = st.text_input("Ask about this article", key=f"{chat_key}_input", placeholder="e.g., Summarize this article")
			if st.button("Ask Bot", key=f"{chat_key}_ask") and user_msg:
				if summarize_with_context is None:
					st.error("Gemini chatbot is unavailable. Please set GEMINI_API_KEY.")
				else:
					try:
						answer = summarize_with_context(user_msg, [article])
						st.session_state["article_chatbot_answers"][article_id] = answer or ""
					except GeminiNotConfigured as e:
						st.error(str(e))
					except Exception as e:
						st.error(f"Chatbot error: {e}")
			ans = st.session_state.get("article_chatbot_answers", {}).get(article_id)
			if ans:
				st.info(ans)
		st.markdown("</div>", unsafe_allow_html=True)


def render_live_news_space():
	_ensure_state()

	st.markdown("""
	<div class='card' style='padding: 1rem 1.25rem; background: linear-gradient(135deg,#5B8DEF,#9b5de5); color:white;'>
		<div style='display:flex;align-items:center;justify-content:space-between;gap:1rem;'>
			<div>
				<h3 style='margin:0;'>📰 Live News</h3>
				<div class='subtle'>Fetch and analyze fresh headlines across selected categories.</div>
			</div>
		</div>
	</div>
	""", unsafe_allow_html=True)

	fetch_col, analyze_col = st.columns([1, 1])
	with fetch_col:
		if st.button("⚡ Fetch Articles", key="btn_fetch", use_container_width=True):
			try:
				categories = list(st.session_state["news_articles"].keys())
				fetched: Dict[str, List[Dict]] = {}
				for cat in categories:
					fetched[cat] = fetch_news_category(cat, 20)
				st.session_state["news_articles"] = fetched
				st.session_state["news_article_sentiments"] = {}
				st.session_state["news_overall_sentiments"] = []
				st.session_state["news_overall_freq"] = []
				st.session_state["news_overall_entities"] = []
				st.session_state["open_article_analysis"] = None
				st.session_state["news_search_results"] = []
				st.success("✅ Fetched latest articles for all categories.")
			except NewsApiError as e:
				st.error(str(e))
			except Exception as e:
				st.error(f"Failed to fetch articles: {e}")
	with analyze_col:
		if st.button("📊 Run Overall Analysis", key="btn_overall", use_container_width=True):
			_update_overall_sentiment()

	_render_overall_summary()

	# Search bar
	st.markdown("<div class='card-header'><h3 style='margin:0'>🔎 Search News</h3><span class='subtle'>Search headlines by keyword</span></div>", unsafe_allow_html=True)
	with st.container():
		st.markdown("<div class='card'>", unsafe_allow_html=True)
		q_col, btn_col = st.columns([4, 1])
		with q_col:
			query = st.text_input("Enter search keywords", key="news_search_query", value=st.session_state.get("news_search_query", ""))
		with btn_col:
			if st.button("Search", key="btn_search", use_container_width=True):
				if query and query.strip():
					try:
						results = search_gnews(query.strip(), 20)
						st.session_state["news_search_results"] = results
						st.session_state["open_article_analysis"] = None
						st.success(f"🔍 Found {len(results)} results for '{query.strip()}'.")
					except NewsApiError as e:
						st.error(str(e))
					except Exception as e:
						st.error(f"Search failed: {e}")
		st.markdown("</div>", unsafe_allow_html=True)

	# Render search results if any
	search_results = st.session_state.get("news_search_results", [])
	if search_results:
		_section_header("🔎 Search Results")
		for idx, a in enumerate(search_results):
			_render_article_card(a, "search", idx)

	tab_names = [
		"🎬 Entertainment", "💰 Finance", "🏟️ Sports", "💻 Technology",
	]
	cats = ["entertainment", "finance", "sports", "technology"]
	tabs = st.tabs(tab_names)
	for i, cat in enumerate(cats):
		with tabs[i]:
			arts = st.session_state["news_articles"].get(cat, [])
			if not arts:
				st.info("No articles. Click Fetch Articles.")
			else:
				for idx, a in enumerate(arts):
					_render_article_card(a, cat, idx)

	# Chatbot section at bottom
	_section_header("💬 Chat with the feed", "Ask questions or request summaries based on the articles above.")
	with st.container():
		st.markdown("<div class='card'>", unsafe_allow_html=True)
		user_msg = st.text_input("Ask the chatbot", key="chatbot_input", placeholder="e.g., Summarize the top headlines")
		if st.button("Ask", key="chatbot_ask") and user_msg:
			if summarize_with_context is None:
				st.error("Gemini chatbot is unavailable. Please set GEMINI_API_KEY.")
			else:
				try:
					all_articles = []
					arts = st.session_state.get("news_articles", {})
					for lst in arts.values():
						all_articles.extend(lst)
					answer = summarize_with_context(user_msg, all_articles)
					if answer:
						st.success(answer)
					else:
						st.info("No response from model.")
				except GeminiNotConfigured as e:
					st.error(str(e))
				except Exception as e:
					st.error(f"Chatbot error: {e}")
		st.markdown("</div>", unsafe_allow_html=True)