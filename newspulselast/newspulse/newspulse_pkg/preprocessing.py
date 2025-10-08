from __future__ import annotations

import re
from collections import Counter
from typing import Dict, Iterable, List, Tuple

import nltk
import spacy


_NLTK_RESOURCES = [
	("stopwords", "corpora/stopwords"),
	("punkt", "tokenizers/punkt"),
]


def _ensure_nltk():
	for resource, path in _NLTK_RESOURCES:
		try:
			nltk.data.find(path)
		except LookupError:
			nltk.download(resource, quiet=True)
_ensure_nltk()


def load_spacy_model() -> spacy.language.Language:
	try:
		return spacy.load("en_core_web_sm", disable=["parser", "textcat"])
	except OSError:
		from spacy.cli import download
		download("en_core_web_sm")
		return spacy.load("en_core_web_sm", disable=["parser", "textcat"])


def clean_and_lemmatize(text: str, nlp: spacy.language.Language) -> Tuple[str, List[str]]:
	text = text.strip()
	if not text:
		return "", []
	doc = nlp(text)
	lemmas: List[str] = []
	for token in doc:
		if token.is_stop or token.is_punct or not token.is_alpha:
			continue
		lemma = token.lemma_.lower()
		if not lemma:
			continue
		lemmas.append(lemma)
	clean_text = " ".join(lemmas)
	return clean_text, lemmas


def preprocess_texts(texts: Iterable[str]) -> List[Dict]:
	nlp = load_spacy_model()
	results: List[Dict] = []
	for t in texts:
		clean_text, tokens = clean_and_lemmatize(t if isinstance(t, str) else str(t), nlp)
		results.append({"raw": t, "clean": clean_text, "tokens": tokens})
	return results


def compute_top_frequencies(tokens_list: Iterable[List[str]], top_k: int = 25) -> List[Tuple[str, int]]:
	counter: Counter = Counter()
	for tokens in tokens_list:
		counter.update(tokens)
	return counter.most_common(top_k)


def compute_top_bigrams(tokens_list: Iterable[List[str]], top_k: int = 20) -> List[Tuple[str, int]]:
	"""Compute the most common bigrams across all token lists.
	Returns list of ("word1 word2", count)."""
	counter: Counter = Counter()
	for tokens in tokens_list:
		for i in range(len(tokens) - 1):
			w1, w2 = tokens[i], tokens[i + 1]
			if not w1 or not w2:
				continue
			counter.update([f"{w1} {w2}"])
	return counter.most_common(top_k)
