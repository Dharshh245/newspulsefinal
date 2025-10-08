from __future__ import annotations

from typing import Optional, List, Dict, Any

import bcrypt

from .config import AppConfig, get_mongo_client_or_none


def _get_collections():
	client = get_mongo_client_or_none()
	if not client:
		return None, None
	cfg = AppConfig()
	db = client[cfg.mongodb_db]
	return db[cfg.users_collection], db[cfg.docs_collection]


def hash_password(password: str) -> bytes:
	salt = bcrypt.gensalt(rounds=12)
	return bcrypt.hashpw(password.encode("utf-8"), salt)


def verify_password(password: str, hashed_value: Any) -> bool:
	# Handle BSON Binary or other types coming from Mongo
	try:
		if isinstance(hashed_value, (bytes, bytearray)):
			hashed_bytes = bytes(hashed_value)
		else:
			hashed_bytes = bytes(hashed_value)
	except Exception:
		return False
	return bcrypt.checkpw(password.encode("utf-8"), hashed_bytes)


def register_user(username: str, password: str) -> bool:
	users_col, _ = _get_collections()
	if users_col is None:
		return False
	if users_col.find_one({"username": username}):
		return False
	users_col.insert_one({"username": username, "password": hash_password(password)})
	return True


def authenticate_user(username: str, password: str) -> bool:
	users_col, _ = _get_collections()
	if users_col is None:
		return False
	user = users_col.find_one({"username": username})
	if not user:
		return False
	return verify_password(password, user.get("password"))


def is_auth_configured() -> bool:
	return get_mongo_client_or_none() is not None


def save_documents(documents: List[Dict]) -> int:
	"""Insert analyzed documents into MongoDB when available.

	Each document should include at least: username (optional), text, clean, sentiment, entities.
	Returns number of inserted documents. If MongoDB disabled, returns 0.
	"""
	_, docs_col = _get_collections()
	if docs_col is None or not documents:
		return 0
	res = docs_col.insert_many(documents)
	return len(res.inserted_ids)

