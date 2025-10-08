from __future__ import annotations

from typing import Dict, List

import spacy
from transformers import AutoModelForTokenClassification, AutoTokenizer, TokenClassificationPipeline

from .config import AppConfig


def get_spacy_ner() -> spacy.language.Language:
	try:
		return spacy.load("en_core_web_sm")
	except OSError:
		from spacy.cli import download
		download("en_core_web_sm")
		return spacy.load("en_core_web_sm")


_HF_NER: TokenClassificationPipeline | None = None


def get_hf_ner() -> TokenClassificationPipeline:
	global _HF_NER
	if _HF_NER is not None:
		return _HF_NER
	model_name = AppConfig().ner_hf_model
	tokenizer = AutoTokenizer.from_pretrained(model_name)
	model = AutoModelForTokenClassification.from_pretrained(model_name)
	_HF_NER = TokenClassificationPipeline(model=model, tokenizer=tokenizer, aggregation_strategy="simple")
	return _HF_NER


def extract_entities_spacy(texts: List[str]) -> List[List[Dict]]:
	nlp = get_spacy_ner()
	results: List[List[Dict]] = []
	for t in texts:
		doc = nlp(t)
		ents: List[Dict] = []
		for ent in doc.ents:
			if ent.label_ in {"PERSON", "ORG", "GPE", "LOC"}:
				ents.append({"text": ent.text, "label": ent.label_, "start": ent.start_char, "end": ent.end_char})
		results.append(ents)
	return results


def extract_entities_hf(texts: List[str]) -> List[List[Dict]]:
	pipeline = get_hf_ner()
	results: List[List[Dict]] = []
	for t in texts:
		preds = pipeline(t, truncation=True, padding=True, max_length=512)
		filtered = [
			{"text": p.get("word"), "label": p.get("entity_group"), "score": float(p.get("score", 0.0)), "start": p.get("start"), "end": p.get("end")}
			for p in preds
			if p.get("entity_group") in {"PER", "ORG", "LOC"}
		]
		results.append(filtered)
	return results

