import React, { useState } from "react";

function NewsSummary() {
  const [articleText, setArticleText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async () => {
    setError("");
    setSummary("");
    if (!articleText.trim()) {
      setError("Please paste a news article to summarize.");
      return;
    }

    setLoading(true);
    try {
      const resp = await fetch("/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ articleText }),
      });
      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
      }
      const data = await resp.json();
      setSummary(data.summary || "");
    } catch (e) {
      setError("Failed to fetch summary. Make sure the API is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h2 className="text-2xl font-semibold mb-4">Ollama News Summary</h2>

      <textarea
        className="w-full border rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[160px]"
        placeholder="Paste news article text here..."
        value={articleText}
        onChange={(e) => setArticleText(e.target.value)}
      />

      <div className="mt-3 flex items-center gap-3">
        <button
          onClick={handleSummarize}
          disabled={loading}
          className="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Summarizing..." : "Summarize"}
        </button>
        {error && <span className="text-red-600 text-sm">{error}</span>}
      </div>

      {summary && (
        <div className="mt-6 bg-white dark:bg-gray-900 border rounded-lg shadow-sm p-4">
          <h3 className="font-medium mb-2">Summary</h3>
          <p className="text-gray-800 dark:text-gray-100 whitespace-pre-wrap">{summary}</p>
        </div>
      )}
    </div>
  );
}

export default NewsSummary;


