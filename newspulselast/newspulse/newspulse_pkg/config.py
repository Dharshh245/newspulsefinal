import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

@dataclass
class AppConfig:
	app_title: str = os.getenv("APP_TITLE", "NewsPulse – NLP Analysis")
	mongodb_uri: str = os.getenv("MONGODB_URI", "")
	mongodb_db: str = os.getenv("MONGODB_DB", "newspulse")
	users_collection: str = os.getenv("MONGODB_USERS_COLLECTION", "users")
	docs_collection: str = os.getenv("MONGODB_DOCS_COLLECTION", "documents")
	sentiment_model: str = os.getenv(
		"SENTIMENT_MODEL",
		"cardiffnlp/twitter-roberta-base-sentiment-latest",
	)
	ner_hf_model: str = os.getenv("NER_HF_MODEL", "dslim/bert-base-NER")


def get_mongo_client_or_none() -> Optional["MongoClient"]:
	uri = AppConfig().mongodb_uri
	if not uri:
		return None
	try:
		from pymongo import MongoClient
		client = MongoClient(uri)
		# ping to validate connection
		client.admin.command("ping")
		return client
	except Exception:
		return None

