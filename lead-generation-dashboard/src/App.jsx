import React, { useState } from "react";
import axios from "axios";
import LeadTable from "./components/LeadTable";
import SearchForm from "./components/SearchForm";
import "./index.css";
import {
  FiSearch,
  FiUsers,
  FiZap,
  FiTarget,
  FiTrendingUp,
  FiShield,
} from "react-icons/fi";

// API URL - uses environment variable in production, localhost in development
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [leads, setLeads] = useState([]);
  const [urls, setUrls] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query, numLinks) => {
    setLoading(true);
    setError(null);
    setHasSearched(true);
    try {
      const response = await axios.post(`${API_URL}/generate-leads`, {
        query,
        num_links: Number(numLinks),
      });

      setLeads(response.data.user_data || []);
      setUrls(response.data.urls || []);

      // Show message if no leads found
      if (!response.data.user_data?.length && !response.data.urls?.length) {
        setError("No leads found for this query. Try a different search term.");
      }
    } catch (error) {
      console.error("Error fetching leads:", error);
      if (error.response?.status === 404) {
        setError("No leads found for this query. Try a different search term.");
      } else if (error.response?.status === 500) {
        setError("Server error. Please check your API keys and try again.");
      } else {
        setError(
          "Failed to connect to server. Make sure the backend is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Animated background gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-950 -z-10"></div>
      <div className="fixed inset-0 opacity-30 -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500 rounded-full filter blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500 rounded-full filter blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-cyan-500 rounded-full filter blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="container mx-auto max-w-7xl px-6 py-12">
        {/* Header */}
        <header className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-500/10 border border-indigo-500/20 rounded-full text-indigo-400 text-sm font-medium mb-6">
            <FiZap className="w-4 h-4" />
            Powered by OpenAI GPT-4
          </div>
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-white via-indigo-200 to-purple-200 bg-clip-text text-transparent">
              LeadFinder
            </span>
            <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              {" "}
              AI
            </span>
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10">
            Discover high-quality leads through AI-powered social analysis.
            Transform your prospecting with intelligent automation.
          </p>

          {/* Feature badges */}
          <div className="flex flex-wrap justify-center gap-4">
            <FeatureCard icon={<FiTarget />} text="Precision Targeting" />
            <FeatureCard icon={<FiTrendingUp />} text="Smart Analytics" />
            <FeatureCard icon={<FiShield />} text="Quality Verified" />
            <FeatureCard icon={<FiUsers />} text="Rich Profiles" />
          </div>
        </header>

        {/* Search Section */}
        <div className="flex justify-center mb-16">
          <div className="w-full max-w-2xl">
            <div className="relative">
              <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-1000"></div>
              <div className="relative bg-slate-900/90 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-8">
                <SearchForm onSearch={handleSearch} loading={loading} />
              </div>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
              <span className="text-xl">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {/* Results Section */}
        {leads.length > 0 || urls.length > 0 ? (
          <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl overflow-hidden shadow-2xl">
            <LeadTable leads={leads} sourceUrls={urls} />
          </div>
        ) : (
          <div className="text-center py-20">
            <div className="max-w-md mx-auto">
              <div className="relative w-32 h-32 mx-auto mb-8">
                <div className="absolute inset-0 bg-indigo-500/20 rounded-full animate-ping"></div>
                <div className="absolute inset-2 bg-indigo-500/10 rounded-full animate-pulse"></div>
                <div className="relative flex items-center justify-center w-32 h-32">
                  <div className="bg-slate-800 p-6 rounded-full border border-slate-700 shadow-xl">
                    <FiSearch className="w-12 h-12 text-indigo-400" />
                  </div>
                </div>
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">
                {loading
                  ? "Analyzing Sources..."
                  : hasSearched
                  ? "No Results Found"
                  : "Ready to Discover"}
              </h3>
              <p className="text-slate-400 mb-6">
                {loading
                  ? "AI is scanning social platforms and extracting valuable lead data..."
                  : hasSearched
                  ? "Try a different search query or increase the number of sources"
                  : "Enter your target audience or service to find potential leads"}
              </p>
              {loading && (
                <div className="flex justify-center gap-2">
                  {[...Array(4)].map((_, i) => (
                    <div
                      key={i}
                      className="w-2.5 h-2.5 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full animate-bounce"
                      style={{ animationDelay: `${i * 0.15}s` }}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-20 py-8">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
          <p className="text-slate-500 text-sm">
            &copy; 2025 LeadFinder AI. Built with OpenAI & React.
          </p>
          <div className="flex items-center gap-6 mt-4 md:mt-0">
            <span className="text-slate-600 text-sm">Privacy Policy</span>
            <span className="text-slate-600 text-sm">Terms of Service</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, text }) {
  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 border border-slate-700/50 rounded-full hover:border-indigo-500/50 hover:bg-slate-800/80 transition-all duration-300">
      <div className="text-indigo-400">{icon}</div>
      <span className="text-sm font-medium text-slate-300">{text}</span>
    </div>
  );
}

export default App;
