from __future__ import annotations

from typing import List

import streamlit as st
try:
	from streamlit.runtime.scriptrunner import get_script_run_ctx
except Exception:
	get_script_run_ctx = None  # type: ignore[assignment]

from newspulse_pkg.auth import authenticate_user, register_user, is_auth_configured
from newspulse_pkg.config import AppConfig
from newspulse_pkg.news_ui import render_live_news_space


def _ensure_streamlit_run():
	try:
		if get_script_run_ctx is None or get_script_run_ctx() is None:
			import sys
			print("This script is a Streamlit app. Run: streamlit run app.py")
			sys.exit(0)
	except Exception:
		pass


def _inject_global_styles():
	st.markdown(
		"""
		<style>
		:root {
			--primary:#5B8DEF;
			--gradient: linear-gradient(135deg,#5B8DEF,#9b5de5);
			--bg:#0f172a;
			--surface:#111827;
			--surface-2:#0b1220;
			--text:#E5E7EB;
			--muted:#9CA3AF;
			--border:rgba(255,255,255,0.08);
			--shadow:0 6px 20px rgba(0,0,0,.4);
		}
		[data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
		.block-container { padding-top: 2rem; padding-bottom: 2rem; }
		h1,h2,h3,h4 { color: var(--text); letter-spacing:-.01em; }
		.subtle { color: var(--muted); font-size: .9rem; }

		/* Card */
		.card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.1rem 1.3rem; box-shadow: var(--shadow); transition: transform .15s ease; }
		.card:hover { transform: translateY(-3px); }
		.card-header { display:flex; align-items:center; justify-content:space-between; gap:1rem; }

		/* Buttons */
		.stButton>button { border-radius: 10px; padding: .55rem 1rem; font-weight:600; transition: all .2s ease; }
		.stButton>button[kind="primary"], .stButton>button:hover { background: var(--gradient) !important; border:none !important; color: #fff !important; box-shadow: 0 6px 16px rgba(91,141,239,.35); }
		.stButton>button { background:#1f2937; border: 1px solid var(--border); color: var(--text); }
		.stButton>button:hover { background:#243244; }

		/* Inputs */
		input, textarea, select { background: #0b1220 !important; color: var(--text) !important; border-radius:10px !important; border: 1px solid var(--border) !important; }

		/* Tabs */
		.stTabs [data-baseweb="tab-list"] { gap: .5rem; }
		.stTabs [data-baseweb="tab"] { background:#0b1220; color: var(--text); border-radius: 12px 12px 0 0; padding:.4rem .9rem; border:1px solid var(--border); transition: all .2s ease; }
		.stTabs [data-baseweb="tab"]:hover { background:#1e293b; }
		.stTabs [data-baseweb="tab"][aria-selected="true"] { background: var(--gradient); color:white !important; border:none; }
		</style>
		""",
		unsafe_allow_html=True,
	)


_ensure_streamlit_run()

cfg = AppConfig()
st.set_page_config(page_title=cfg.app_title, page_icon="📰", layout="wide")

st.markdown(
	f"""
	<div style="padding:1.2rem 1.4rem; background:linear-gradient(135deg,#5B8DEF,#9b5de5); border-radius:14px; box-shadow:0 6px 20px rgba(0,0,0,.35); margin-bottom:1.2rem;">
		<h1 style="margin:0; color:white;">{cfg.app_title}</h1>
	</div>
	""",
	unsafe_allow_html=True,
)

_inject_global_styles()


def auth_flow() -> bool:
	if "auth_ok" not in st.session_state:
		st.session_state["auth_ok"] = False
	if st.session_state.get("auth_ok"):
		return True
	st.markdown("<div class='card'>", unsafe_allow_html=True)
	st.markdown("<div class='card-header'><h3 style='margin:0'>🔐 Login</h3><span class='subtle'>Sign in to continue</span></div><div class='divider'></div>", unsafe_allow_html=True)
	login_tab, register_tab = st.tabs(["Login", "Register"])
	with login_tab:
		lu = st.text_input("Username", key="login_username")
		lp = st.text_input("Password", type="password", key="login_password")
		if not is_auth_configured():
			st.info("⚠️ MongoDB is not configured. Set `MONGODB_URI` in `.env` to enable login.")
		if st.button("Login", key="btn_login", type="primary") and lu and lp:
			ok = authenticate_user(lu, lp)
			if ok:
				st.session_state["auth_ok"] = True
				st.session_state["username"] = lu
				st.success("✅ Logged in successfully")
				st.rerun()
			else:
				st.warning("❌ Login failed or auth disabled.")
	with register_tab:
		ru = st.text_input("Username", key="reg_username")
		rp = st.text_input("Password", type="password", key="reg_password")
		if not is_auth_configured():
			st.info("⚠️ MongoDB is not configured. Set `MONGODB_URI` in `.env` to enable registration.")
		if st.button("Create account", key="btn_register"):
			if ru and rp:
				ok = register_user(ru, rp)
				if ok:
					st.success("🎉 Registered. Please login.")
				else:
					st.warning("⚠️ User exists or auth disabled.")
	st.markdown("</div>", unsafe_allow_html=True)
	return st.session_state.get("auth_ok", False)


if not auth_flow():
	st.stop()

colA, colB = st.columns([4, 1])
with colA:
	st.caption(f"👤 User: {st.session_state.get('username', 'guest')}")
with colB:
	if st.button("🚪 Logout", use_container_width=True):
		st.session_state["auth_ok"] = False
		st.session_state.pop("username", None)
		st.rerun()

render_live_news_space()


