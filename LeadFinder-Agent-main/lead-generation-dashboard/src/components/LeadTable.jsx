import React, { useState } from "react";
import { CSVLink } from "react-csv";
import {
  FiArrowUp,
  FiArrowDown,
  FiExternalLink,
  FiDownload,
  FiUser,
  FiClock,
  FiChevronDown,
} from "react-icons/fi";
import { ImStatsBars } from "react-icons/im";

function LeadTable({ leads, sourceUrls }) {
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "ascending",
  });

  const sortedLeads = React.useMemo(() => {
    const sortableLeads = [...leads];
    if (sortConfig.key !== null) {
      sortableLeads.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableLeads;
  }, [leads, sortConfig]);

  const requestSort = (key) => {
    let direction = "ascending";
    if (sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  const StatsCard = ({ title, value, icon, gradient }) => (
    <div
      className={`relative overflow-hidden p-6 rounded-2xl bg-gradient-to-br ${gradient}`}
    >
      <div className="relative z-10">
        <div className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
          {icon}
          {title}
        </div>
        <p className="text-3xl font-bold text-white">{value}</p>
      </div>
      <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-white/10 rounded-full blur-xl"></div>
    </div>
  );

  return (
    <div className="bg-transparent">
      {/* Header */}
      <div className="flex flex-wrap justify-between items-center p-6 border-b border-slate-700/50">
        <h2 className="text-2xl font-bold flex items-center text-white mb-4 md:mb-0">
          <ImStatsBars className="mr-3 text-indigo-400" />
          Lead Analysis Report
        </h2>
        <CSVLink
          data={leads}
          filename="lead_report.csv"
          className="flex items-center gap-2 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 border border-emerald-500/30 font-semibold py-2.5 px-5 rounded-xl transition-all duration-300"
        >
          <FiDownload className="w-4 h-4" />
          Export CSV
        </CSVLink>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 bg-slate-800/30">
        <StatsCard
          title="Total Leads"
          value={leads.length}
          icon={<FiUser className="w-4 h-4" />}
          gradient="from-indigo-600 to-indigo-700"
        />
        <StatsCard
          title="Avg. Upvotes"
          value={
            Math.round(
              leads.reduce((acc, lead) => acc + lead.Upvotes, 0) / leads.length
            ) || 0
          }
          icon={<FiArrowUp className="w-4 h-4" />}
          gradient="from-purple-600 to-purple-700"
        />
        <StatsCard
          title="Sources Analyzed"
          value={sourceUrls.length}
          icon={<FiExternalLink className="w-4 h-4" />}
          gradient="from-cyan-600 to-cyan-700"
        />
      </div>

      {/* Leads Grid */}
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {sortedLeads.map((lead, index) => {
            const firstLink = (lead.Links || "").split(", ")[0] || "#";
            const displayDate = lead.Timestamp
              ? new Date(lead.Timestamp).toLocaleDateString()
              : "";
            const confidenceScore = lead["Confidence Score"] || 0;
            const confidenceColor =
              lead.Confidence === "high"
                ? "text-emerald-400 bg-emerald-500/20 border-emerald-500/30"
                : lead.Confidence === "medium"
                ? "text-yellow-400 bg-yellow-500/20 border-yellow-500/30"
                : "text-red-400 bg-red-500/20 border-red-500/30";

            return (
              <a
                key={index}
                href={firstLink}
                target="_blank"
                rel="noopener noreferrer"
                className="group block border border-slate-700/50 rounded-2xl p-5 bg-slate-800/30 hover:bg-slate-800/60 hover:border-indigo-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-indigo-500/10"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold text-sm">
                      {lead.Username?.charAt(0)?.toUpperCase() || "U"}
                    </div>
                    <h3 className="text-lg font-semibold text-white truncate max-w-[150px]">
                      {lead.Username}
                    </h3>
                  </div>
                  <div className="flex items-center gap-2">
                    {lead.Source && (
                      <span className="px-3 py-1 text-xs font-medium rounded-full bg-slate-700/60 text-slate-200 border border-slate-600/60">
                        {lead.Source}
                      </span>
                    )}
                    <span className="px-3 py-1 text-xs font-medium rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      {lead["Post Type"]}
                    </span>
                  </div>
                </div>

                {/* Title if available */}
                {lead.Title && (
                  <h4 className="text-white text-sm font-medium mb-2 line-clamp-1">
                    {lead.Title}
                  </h4>
                )}

                <p className="text-slate-300 text-sm mb-3 line-clamp-3 leading-relaxed">
                  {lead.Snippet || lead.Bio}
                </p>

                <div className="flex justify-between items-center text-sm mb-4 pt-4 border-t border-slate-700/50">
                  <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
                    <FiArrowUp className="w-4 h-4" />
                    {lead.Upvotes} upvotes
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-500">
                    <FiClock className="w-3.5 h-3.5" />
                    {displayDate || ""}
                  </div>
                </div>

                {/* Confidence Score Bar */}
                <div className="mb-3">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span
                      className={`px-2 py-0.5 rounded border ${confidenceColor}`}
                    >
                      {lead.Confidence?.toUpperCase() || "UNKNOWN"}
                    </span>
                    <span className="text-slate-400">
                      {confidenceScore}/100
                    </span>
                  </div>
                  <div className="w-full bg-slate-700/50 rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full ${
                        lead.Confidence === "high"
                          ? "bg-emerald-500"
                          : lead.Confidence === "medium"
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${Math.min(confidenceScore, 100)}%` }}
                    ></div>
                  </div>
                </div>

                <div className="flex items-center justify-center gap-2 text-indigo-400 group-hover:text-indigo-300 font-medium py-2 rounded-xl bg-indigo-500/10 group-hover:bg-indigo-500/20 transition-all">
                  <FiExternalLink className="w-4 h-4" />
                  View Profile
                </div>
              </a>
            );
          })}
        </div>
      </div>

      {/* Source URLs Section */}
      <div className="p-6 border-t border-slate-700/50">
        <details className="group">
          <summary className="flex items-center cursor-pointer list-none text-slate-300 hover:text-white transition-colors">
            <FiChevronDown className="w-5 h-5 mr-2 transition-transform group-open:rotate-180" />
            <span className="text-lg font-semibold">
              Analyzed Sources ({sourceUrls.length})
            </span>
          </summary>
          <div className="mt-4 space-y-2 pl-7">
            {sourceUrls.map((url, index) => (
              <a
                key={index}
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 p-3 rounded-xl bg-slate-800/30 hover:bg-slate-800/60 border border-slate-700/50 hover:border-indigo-500/50 transition-all duration-300 text-indigo-400 hover:text-indigo-300 truncate"
              >
                <FiExternalLink className="w-4 h-4 flex-shrink-0" />
                <span className="truncate">{url}</span>
              </a>
            ))}
          </div>
        </details>
      </div>
    </div>
  );
}

export default LeadTable;
