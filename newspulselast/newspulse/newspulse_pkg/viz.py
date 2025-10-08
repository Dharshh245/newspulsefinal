from __future__ import annotations

from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px


def plot_word_frequencies(freq_pairs: List[tuple[str, int]]):
	if not freq_pairs:
		return None
	words, counts = zip(*freq_pairs)
	plt.figure(figsize=(10, 5))
	sns.barplot(x=list(words), y=list(counts), color="#4C78A8")
	plt.xticks(rotation=45, ha="right")
	plt.xlabel("Word")
	plt.ylabel("Frequency")
	plt.title("Top Word Frequencies")
	plt.tight_layout()
	return plt.gcf()


def sentiment_distribution_chart(sentiments: List[Dict]):
	if not sentiments:
		return None
	df = pd.DataFrame(sentiments)
	plt.figure(figsize=(6, 4))
	sns.countplot(x="label", data=df, hue="label", legend=False, palette="Set2")
	plt.title("Sentiment Distribution")
	plt.xlabel("Label")
	plt.ylabel("Count")
	plt.tight_layout()
	return plt.gcf()


def entities_count_table(entities_lists: List[List[Dict]]) -> pd.DataFrame:
	rows: List[Dict] = []
	for ents in entities_lists:
		for e in ents:
			rows.append({"entity": e.get("text"), "label": e.get("label")})
	df = pd.DataFrame(rows)
	if df.empty:
		return pd.DataFrame(columns=["label", "entity", "count"])  # empty
	counts = df.groupby(["label", "entity"]).size().reset_index(name="count").sort_values("count", ascending=False)
	return counts


def plotly_word_frequencies(freq_pairs: List[tuple[str, int]]):
	if not freq_pairs:
		return None
	words, counts = zip(*freq_pairs)
	df = pd.DataFrame({"word": list(words), "count": list(counts)})
	fig = px.bar(
		df, x="word", y="count", title="Top Word Frequencies",
		labels={"word": "Word", "count": "Frequency"}, template="plotly_white",
	)
	fig.update_layout(xaxis_tickangle=-45)
	return fig


def plotly_sentiment_distribution(sentiments: List[Dict]):
	if not sentiments:
		return None
	df = pd.DataFrame(sentiments)
	counts = df.groupby("label").size().reset_index(name="count")
	fig = px.pie(counts, values="count", names="label", title="Sentiment Distribution",
			hole=0.35, template="plotly_white")
	fig.update_traces(textposition="inside", textinfo="percent+label")
	return fig


def plotly_bigrams(bigrams: List[tuple[str, int]]):
	if not bigrams:
		return None
	phrases, counts = zip(*bigrams)
	df = pd.DataFrame({"bigram": list(phrases), "count": list(counts)})
	fig = px.bar(df, x="bigram", y="count", title="Top Bigrams", labels={"bigram": "Bigram", "count": "Frequency"}, template="plotly_white")
	fig.update_layout(xaxis_tickangle=-45)
	return fig


def plotly_entity_labels(entities_lists: List[List[Dict]]):
	rows: List[Dict] = []
	for ents in entities_lists:
		for e in ents:
			rows.append({"label": e.get("label")})
	df = pd.DataFrame(rows)
	if df.empty:
		return None
	counts = df.groupby("label").size().reset_index(name="count")
	fig = px.bar(counts, x="label", y="count", title="Entity Labels", template="plotly_white")
	return fig
