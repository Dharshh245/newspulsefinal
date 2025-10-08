from __future__ import annotations

from typing import Dict, List, Optional

from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline

from .config import AppConfig


_PIPELINE: TextClassificationPipeline | None = None
_MODEL_NAME: str | None = None


def get_sentiment_pipeline(model_name: Optional[str] = None) -> TextClassificationPipeline:
	global _PIPELINE, _MODEL_NAME
	requested = model_name or AppConfig().sentiment_model
	if _PIPELINE is not None and _MODEL_NAME == requested:
		return _PIPELINE
	tokenizer = AutoTokenizer.from_pretrained(requested)
	model = AutoModelForSequenceClassification.from_pretrained(requested)
	_PIPELINE = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False)
	_MODEL_NAME = requested
	return _PIPELINE


def predict_sentiment(texts: List[str], model_name: Optional[str] = None) -> List[Dict]:
	pipeline = get_sentiment_pipeline(model_name)
	outputs = pipeline(texts, truncation=True, padding=True, max_length=512)
	# normalize labels
	results: List[Dict] = []
	for out in outputs:
		raw_label = str(out["label"]).lower()
		label = raw_label
		if raw_label in {"positive", "pos"}:
			label = "positive"
		elif raw_label in {"negative", "neg"}:
			label = "negative"
		elif raw_label in {"neutral", "neu"}:
			label = "neutral"
		elif raw_label.startswith("label_"):
			# Map indices for common models
			try:
				idx = int(raw_label.split("_")[-1])
			except Exception:
				idx = -1
			active_model = (model_name or AppConfig().sentiment_model).lower()
			if "cardiffnlp/twitter-roberta-base-sentiment" in active_model:
				mapping = {0: "negative", 1: "neutral", 2: "positive"}
			else:
				mapping = {0: "negative", 1: "positive"}
			label = mapping.get(idx, "neutral")
		score = float(out["score"]) if isinstance(out, dict) else float(out.score)
		results.append({"label": label, "score": score})
	return results

