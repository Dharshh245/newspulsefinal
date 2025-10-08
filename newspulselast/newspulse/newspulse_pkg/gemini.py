# from __future__ import annotations

# import os
# from typing import List, Dict

# import google.generativeai as genai


# class GeminiNotConfigured(Exception):
# 	pass


# def _get_client() -> genai.GenerativeModel:
# 	api_key = os.getenv("GEMINI_API_KEY", "").strip()
# 	if not api_key:
# 		raise GeminiNotConfigured("GEMINI_API_KEY is not configured")
# 	genai.configure(api_key=api_key)
# 	# Using a general-purpose, widely available model name
# 	return genai.GenerativeModel("gemini-1.5-flash")


# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
# 	"""Call Gemini to answer questions or summarize based on provided articles.

# 	Args:
# 		user_query: The user's question or instruction.
# 		articles: A list of article dicts with keys like 'title', 'description', 'content', 'url', 'source'.

# 	Returns:
# 		Model text response.
# 	"""
# 	model = _get_client()
# 	# Construct a short context from the articles. Keep it bounded to avoid exceeding token limits.
# 	context_lines: List[str] = []
# 	for a in articles[:20]:
# 		title = (a.get("title") or "").strip()
# 		desc = (a.get("description") or "").strip()
# 		source = (a.get("source") or "").strip()
# 		if title or desc:
# 			ctx = f"- {title} :: {desc}"
# 			if source:
# 				ctx += f" (source: {source})"
# 			context_lines.append(ctx[:500])

# 	prompt = (
# 		"You are a concise assistant. Answer the question using ONLY the provided article notes when possible. "
# 		"If unsure, say you are not sure. Keep answers short and clear.\n\n"
# 		"Article notes:\n" + ("\n".join(context_lines) or "(no notes)") + "\n\n"
# 		f"User question: {user_query}\n"
# 	)

# 	resp = model.generate_content(prompt)
# 	text = getattr(resp, "text", None)
# 	if not text and hasattr(resp, "candidates") and resp.candidates:
# 		# Fallback extraction for SDK variants
# 		try:
# 			text = resp.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
# 		except Exception:
# 			text = ""
# 	return (text or "")[:4000]


# from __future__ import annotations

# import os
# from typing import List, Dict

# import google.generativeai as genai


# class GeminiNotConfigured(Exception):
#     pass


# def _get_client() -> genai.GenerativeModel:
#     api_key = os.getenv("GEMINI_API_KEY", "").strip()
#     if not api_key:
#         raise GeminiNotConfigured("GEMINI_API_KEY is not configured")
#     genai.configure(api_key=api_key)
#     # Use a valid, supported model
#     return genai.GenerativeModel("gemini-1.5")


# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
#     """Call Gemini to answer questions or summarize based on provided articles."""
#     model = _get_client()
#     # Construct a short context from the articles. Keep it bounded to avoid exceeding token limits.
#     context_lines: List[str] = []
#     for a in articles[:20]:
#         title = (a.get("title") or "").strip()
#         desc = (a.get("description") or "").strip()
#         source = (a.get("source") or "").strip()
#         if title or desc:
#             ctx = f"- {title} :: {desc}"
#             if source:
#                 ctx += f" (source: {source})"
#             context_lines.append(ctx[:500])

#     prompt = (
#         "You are a concise assistant. Answer the question using ONLY the provided article notes when possible. "
#         "If unsure, say you are not sure. Keep answers short and clear.\n\n"
#         "Article notes:\n" + ("\n".join(context_lines) or "(no notes)") + "\n\n"
#         f"User question: {user_query}\n"
#     )

#     resp = model.generate_content(prompt)
#     text = getattr(resp, "text", None)
#     if not text and hasattr(resp, "candidates") and resp.candidates:
#         # Fallback extraction for SDK variants
#         try:
#             text = resp.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
#         except Exception:
#             text = ""
#     return (text or "")[:4000]



# from __future__ import annotations
# import os
# from typing import List, Dict
# import google.generativeai as genai


# class GeminiNotConfigured(Exception):
#     pass


# def _get_client() -> genai.GenerativeModel:
#     api_key = os.getenv("GEMINI_API_KEY", "").strip()
#     if not api_key:
#         raise GeminiNotConfigured("GEMINI_API_KEY is not configured")
#     genai.configure(api_key=api_key)
#     # Use a valid, supported model
#     return genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"


# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
#     """Call Gemini to answer questions or summarize based on provided articles."""
#     model = _get_client()

#     context_lines: List[str] = []
#     for a in articles[:20]:
#         title = (a.get("title") or "").strip()
#         desc = (a.get("description") or "").strip()
#         source = (a.get("source") or "").strip()
#         if title or desc:
#             ctx = f"- {title} :: {desc}"
#             if source:
#                 ctx += f" (source: {source})"
#             context_lines.append(ctx[:500])

#     prompt = (
#         "You are a concise assistant. Answer the question using ONLY the provided article notes when possible. "
#         "If unsure, say you are not sure. Keep answers short and clear.\n\n"
#         "Article notes:\n" + ("\n".join(context_lines) or "(no notes)") + "\n\n"
#         f"User question: {user_query}\n"
#     )

#     resp = model.generate_content(prompt)
#     text = getattr(resp, "text", None)
#     if not text and hasattr(resp, "candidates") and resp.candidates:
#         try:
#             text = resp.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
#         except Exception:
#             text = ""
#     return (text or "")[:4000]


# from __future__ import annotations
# import os
# from typing import List, Dict
# import google.generativeai as genai
# import streamlit as st


# class GeminiNotConfigured(Exception):
#     pass


# def _get_client(preferred_model="gemini-1.5-flash") -> genai.GenerativeModel:
#     """Get a Gemini model safely with fallback."""
#     api_key = os.getenv("GEMINI_API_KEY", "").strip()
#     if not api_key:
#         raise GeminiNotConfigured("GEMINI_API_KEY is not configured")
    
#     genai.configure(api_key=api_key)

#     # List available models
#     try:
#         models = genai.list_models().get("models", [])
#         available = [m["name"] for m in models]
#     except Exception as e:
#         st.error(f"Error fetching models: {e}")
#         available = []

#     # Use preferred model if available
#     if preferred_model in available:
#         return genai.GenerativeModel(preferred_model)

#     # Fallback: pick the first Gemini model available
#     fallback = next((m for m in available if "gemini" in m.lower()), None)
#     if fallback:
#         st.warning(f"Preferred model '{preferred_model}' not found. Using '{fallback}' instead.")
#         return genai.GenerativeModel(fallback)

#     st.error("No Gemini models available. Please check your API key or network.")
#     return None


# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
#     """Call Gemini to answer questions or summarize based on provided articles."""
#     model = _get_client()
#     if not model:
#         return "Chatbot unavailable. No model found."

#     context_lines: List[str] = []
#     for a in articles[:20]:
#         title = (a.get("title") or "").strip()
#         desc = (a.get("description") or "").strip()
#         source = (a.get("source") or "").strip()
#         if title or desc:
#             ctx = f"- {title} :: {desc}"
#             if source:
#                 ctx += f" (source: {source})"
#             context_lines.append(ctx[:500])

#     prompt = (
#         "You are a concise assistant. Answer the question using ONLY the provided article notes when possible. "
#         "If unsure, say you are not sure. Keep answers short and clear.\n\n"
#         "Article notes:\n" + ("\n".join(context_lines) or "(no notes)") + "\n\n"
#         f"User question: {user_query}\n"
#     )

#     try:
#         resp = model.generate_content(prompt)
#     except Exception as e:
#         return f"Error generating summary: {e}"

#     text = getattr(resp, "text", None)
#     if not text and hasattr(resp, "candidates") and resp.candidates:
#         try:
#             text = resp.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
#         except Exception:
#             text = ""
#     return (text or "")[:4000]


# from __future__ import annotations
# import os
# from typing import List, Dict
# import google.generativeai as genai

# # Configure your Gemini API key
# api_key = os.getenv("GEMINI_API_KEY", "").strip()
# if not api_key:
#     raise ValueError("GEMINI_API_KEY is not set in your environment.")
# genai.configure(api_key=api_key)

# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
#     """
#     Safely summarize or answer questions based on any list of articles.
#     Works for all articles, avoids model 404s.
#     """
#     try:
#         model = genai.GenerativeModel("gemini-1.5")  # safe fallback model
#     except Exception as e:
#         return f"Chatbot unavailable. Error initializing model: {e}"

#     # Build context from articles
#     context_lines: List[str] = []
#     for a in articles[:20]:
#         title = (a.get("title") or "").strip()
#         desc = (a.get("description") or "").strip()
#         source = (a.get("source") or "").strip()
#         if title or desc:
#             ctx = f"- {title} :: {desc}"
#             if source:
#                 ctx += f" (source: {source})"
#             context_lines.append(ctx[:500])

#     prompt = (
#         "You are a concise assistant. Answer the question using ONLY the provided article notes when possible. "
#         "If unsure, say you are not sure. Keep answers short and clear.\n\n"
#         "Article notes:\n" + ("\n".join(context_lines) or "(no notes)") + "\n\n"
#         f"User question: {user_query}\n"
#     )

#     try:
#         resp = model.generate_content(prompt)
#         text = getattr(resp, "text", None)
#         if not text and hasattr(resp, "candidates") and resp.candidates:
#             text = resp.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
#         return (text or "")[:4000]
#     except Exception as e:
#         return f"Error generating summary: {e}"


# from __future__ import annotations
# import os
# from typing import List, Dict
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load .env
# load_dotenv()

# # Configure Gemini API key
# api_key = os.getenv("GEMINI_API_KEY", "").strip()
# if not api_key:
#     raise ValueError("GEMINI_API_KEY is not set in your environment.")
# genai.configure(api_key=api_key)

# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
#     """
#     Safely summarize or answer questions based on any list of articles.
#     Works for all articles, avoids model 404s.
#     """
#     try:
#         # Use a stable Gemini model directly
#         model = genai.GenerativeModel("gemini-1.5")
#     except Exception as e:
#         return f"Chatbot unavailable. Error initializing model: {e}"

#     # Build context from articles
#     context_lines: List[str] = []
#     for a in articles[:20]:
#         title = (a.get("title") or "").strip()
#         desc = (a.get("description") or "").strip()
#         source = (a.get("source") or "").strip()
#         if title or desc:
#             ctx = f"- {title} :: {desc}"
#             if source:
#                 ctx += f" (source: {source})"
#             context_lines.append(ctx[:500])

#     prompt = (
#         "You are a concise assistant. Answer the question using ONLY the provided article notes when possible. "
#         "If unsure, say you are not sure. Keep answers short and clear.\n\n"
#         "Article notes:\n" + ("\n".join(context_lines) or "(no notes)") + "\n\n"
#         f"User question: {user_query}\n"
#     )

#     try:
#         resp = model.generate_content(prompt)
#         text = getattr(resp, "text", None)
#         if not text and hasattr(resp, "candidates") and resp.candidates:
#             text = resp.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
#         return (text or "")[:4000]
#     except Exception as e:
#         return f"Error generating summary: {e}"


# from __future__ import annotations
# import os
# from typing import List, Dict
# from dotenv import load_dotenv
# import google.generativeai as genai


# class GeminiNotConfigured(Exception):
#     """Raised when GEMINI_API_KEY is not configured properly."""
#     pass


# # ------------------------------------------------------------
# # 🔹 Initialize Gemini API
# # ------------------------------------------------------------
# def _configure_gemini() -> str:
#     """Load API key from .env or environment and return selected model name."""
#     load_dotenv()

#     api_key = os.getenv("GEMINI_API_KEY", "").strip()
#     if not api_key:
#         raise GeminiNotConfigured("❌ GEMINI_API_KEY is missing. Please add it to your .env file.")

#     genai.configure(api_key=api_key)

#     # Use a safe and supported model from your available list
#     # (as per your test output)
#     return "models/gemini-2.5-flash"


# # ------------------------------------------------------------
# # 🔹 Main summarization function
# # ------------------------------------------------------------
# def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
#     """
#     Summarize or answer questions based on a list of articles.
#     Automatically handles errors, and supports all current Gemini models.
#     """
#     try:
#         model_name = _configure_gemini()
#         model = genai.GenerativeModel(model_name)
#     except Exception as e:
#         return f"⚠️ Chatbot unavailable: {e}"

#     # Build context from articles
#     context_lines: List[str] = []
#     for a in articles[:20]:
#         title = (a.get("title") or "").strip()
#         desc = (a.get("description") or "").strip()
#         source = (a.get("source") or "").strip()

#         if title or desc:
#             ctx = f"- {title} :: {desc}"
#             if source:
#                 ctx += f" (source: {source})"
#             context_lines.append(ctx[:500])

#     # Prepare the prompt
#     prompt = (
#         "You are a concise assistant. Answer the question using ONLY the provided article notes. "
#         "If unsure, say you are not sure. Keep the answer short and clear.\n\n"
#         "Article notes:\n"
#         + ("\n".join(context_lines) if context_lines else "(no notes available)") +
#         f"\n\nUser question: {user_query}"
#     )

#     # Generate a response
#     try:
#         response = model.generate_content(prompt)
#         # The latest SDK returns an object with .text or candidates
#         if hasattr(response, "text") and response.text:
#             return response.text.strip()

#         if hasattr(response, "candidates") and response.candidates:
#             return response.candidates[0].content.parts[0].text.strip()

#         return "⚠️ No response text found."
#     except Exception as e:
#         return f"⚠️ Error generating response: {e}"


# # ------------------------------------------------------------
# # 🔹 Optional: test the module directly
# # ------------------------------------------------------------
# if __name__ == "__main__":
#     test_articles = [
#         {
#             "title": "Taylor Swift says close friend Ed Sheeran discovered her engagement on Instagram",
#             "description": "‘You have to email him,’ Swift said of Sheeran during an appearance on The Tonight Show.",
#             "source": "BreakingNews.ie"
#         },
#         {
#             "title": "Becomes Akshay Kumar's 5th Film To Cross This Important Milestone Post-COVID",
#             "description": "Jolly LLB 3 becomes Akshay Kumar’s fifth post-COVID film to hit a major global milestone.",
#             "source": "Koimoi"
#         }
#     ]
#     print("🧠 Testing Gemini summarizer...\n")
#     print(summarize_with_context("Summarize the news briefly.", test_articles))


from __future__ import annotations
import os
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai


class GeminiNotConfigured(Exception):
    """Raised when GEMINI_API_KEY is not configured properly."""
    pass


# ------------------------------------------------------------
# 🔹 Initialize Gemini API
# ------------------------------------------------------------
def _configure_gemini() -> str:
    """Load API key from .env or environment and return selected model name."""
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiNotConfigured("❌ GEMINI_API_KEY is missing. Please add it to your .env file.")

    genai.configure(api_key=api_key)

    # ✅ Use your verified available model
    return "models/gemini-2.5-flash"


# ------------------------------------------------------------
# 🔹 Main AI Function
# ------------------------------------------------------------
def summarize_with_context(user_query: str, articles: List[Dict]) -> str:
    """
    AI assistant that summarizes or answers questions using article context + general knowledge.
    It automatically handles full forms, facts, and open-ended questions.
    """
    try:
        model_name = _configure_gemini()
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        return f"⚠️ Chatbot unavailable: {e}"

    # 🔸 Collect context from articles
    context_lines: List[str] = []
    for a in articles[:20]:
        title = (a.get("title") or "").strip()
        desc = (a.get("description") or "").strip()
        source = (a.get("source") or "").strip()
        if title or desc:
            ctx = f"- {title} :: {desc}"
            if source:
                ctx += f" (source: {source})"
            context_lines.append(ctx[:500])

    # 🔸 Custom AI personality + system prompt
    SYSTEM_ROLE = """
    You are Nova, an intelligent and friendly AI journalist inside the NewsPulse app.
    You understand current affairs, explain terms and full forms (like BCCI, GDP, OTT),
    and use your general world knowledge when news context isn't enough.
    Always sound natural, confident, and concise.
    """

    # 🔸 Combine everything into one prompt
    prompt = (
        f"{SYSTEM_ROLE}\n\n"
        "Use the following article context (if available) to answer the question. "
        "If context doesn't help, use your general knowledge.\n\n"
        "Article notes:\n"
        + ("\n".join(context_lines) if context_lines else "(no news notes available)") +
        f"\n\nUser question: {user_query}\n\n"
        "Your answer should be short, clear, and factually correct."
    )

    # 🔸 Generate answer
    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text.strip()
        if hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()

        return "⚠️ No response text found."

    except Exception as e:
        return f"⚠️ Error generating response: {e}"


# ------------------------------------------------------------
# 🔹 Optional: Run test directly
# ------------------------------------------------------------
if __name__ == "__main__":
    test_articles = [
        {
            "title": "India’s GDP expected to grow by 7% in 2025, says IMF report",
            "description": "The International Monetary Fund predicts a strong economic rebound for India.",
            "source": "Reuters"
        },
        {
            "title": "BCCI announces T20 World Cup squad",
            "description": "India includes Rohit Sharma, Virat Kohli, and Jasprit Bumrah in the squad.",
            "source": "NDTV Sports"
        }
    ]

    print("🧠 Testing Gemini AI Assistant...\n")
    print(summarize_with_context("What is the full form of BCCI?", test_articles))
    print("\n------------------------------------\n")
    print(summarize_with_context("Summarize the above news briefly.", test_articles))
