from __future__ import annotations

from typing import List, Tuple  
import pandas as pd
from datasets import load_dataset
import feedparser


SUPPORTED_FILE_TYPES = {".txt", ".csv"}


def read_text_file(file_path: str) -> List[str]:
	with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
		return [line.strip() for line in f if line.strip()]


def read_csv_file(file_path: str, text_column: str | None = None) -> List[str]:
	df = pd.read_csv(file_path)
	if text_column and text_column in df.columns:
		series = df[text_column].astype(str)
	else:
		for col in df.columns:
			if df[col].dtype == object:
				series = df[col].astype(str)
				break
		else:
			raise ValueError("No suitable text column found in CSV")
	return [t for t in series.tolist() if isinstance(t, str) and t.strip()]


def load_ag_news(split: str = "train", limit: int | None = 1000) -> List[str]:
	ds = load_dataset("ag_news", split=split)
	texts: List[str] = []
	for row in ds:
		text = (row.get("text") or row.get("description") or "").strip()
		if text:
			texts.append(text)
		if limit and len(texts) >= limit:
			break
	return texts


def fetch_rss_texts(feed_urls: List[str], limit_per_feed: int = 20) -> List[str]:
	"""Fetch latest entries from RSS/Atom feeds and return combined texts.

	Combines title + summary/content where available.
	"""
	collected: List[str] = []
	for url in feed_urls:
		try:
			feed = feedparser.parse(url)
			for entry in feed.entries[: max(0, limit_per_feed)]:
				title = (getattr(entry, "title", "") or "").strip()
				summary = (getattr(entry, "summary", "") or getattr(entry, "description", "") or "").strip()
				content = f"{title}. {summary}".strip(". ")
				if content:
					collected.append(content)
		except Exception:
			continue
	return collected

