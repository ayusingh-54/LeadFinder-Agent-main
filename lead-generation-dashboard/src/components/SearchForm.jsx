import React, { useState } from "react";
import { FiSearch, FiLink, FiZap } from "react-icons/fi";

function SearchForm({ onSearch, loading }) {
  const [query, setQuery] = useState("");
  const [numLinks, setNumLinks] = useState(3);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query, numLinks);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label
          className="block text-slate-300 text-sm font-semibold mb-3"
          htmlFor="query"
        >
          What leads are you looking for?
        </label>
        <div className="relative">
          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., AI machine learning services, SaaS marketing tools..."
            className="w-full pl-12 pr-4 py-4 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-slate-800 transition-all duration-300"
            required
          />
          <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-500 w-5 h-5" />
        </div>
      </div>

      <div>
        <label
          className="block text-slate-300 text-sm font-semibold mb-3"
          htmlFor="numLinks"
        >
          Number of sources to analyze
        </label>
        <div className="relative">
          <input
            id="numLinks"
            type="number"
            value={numLinks}
            onChange={(e) => setNumLinks(e.target.value)}
            min="1"
            max="10"
            className="w-full pl-12 pr-4 py-4 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-slate-800 transition-all duration-300"
            required
          />
          <FiLink className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-500 w-5 h-5" />
        </div>
        <p className="mt-2 text-xs text-slate-500">
          Recommended: 3-5 sources for optimal results
        </p>
      </div>

      <button
        type="submit"
        disabled={loading}
        className={`w-full flex items-center justify-center gap-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40
          ${loading ? "opacity-70 cursor-not-allowed" : "hover:scale-[1.02]"}`}
      >
        {loading ? (
          <>
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            <span>Generating Leads...</span>
          </>
        ) : (
          <>
            <FiZap className="w-5 h-5" />
            <span>Generate Leads</span>
          </>
        )}
      </button>
    </form>
  );
}

export default SearchForm;
