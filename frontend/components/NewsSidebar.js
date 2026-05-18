"use client";

import React, { useEffect, useState } from 'react';
import { TrendingUp, RefreshCw, ExternalLink, Clock } from 'lucide-react';

export default function NewsSidebar() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // The address 127.0.0.1 is used because the browser (the client)
  // needs to talk to the port exposed by Docker on your host machine.
  const fetchLatestNews = async () => {
    setLoading(true);
    setError(null);
    try {
 // This uses the environment variable if found, otherwise it falls back to your live Railway backend directly
        const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'https://newsjobsresearch-production.up.railway.app';

        const res = await fetch(`${BACKEND_URL}/api/v1/news`);
      
      if (!res.ok) {
        throw new Error(`Failed to fetch: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      
      // We map specifically to data.results as seen in your cURL output
      setNews(data.results || []);
    } catch (err) {
      console.error("News fetch failed:", err);
      setError("Unable to connect to the news feed.");
    } finally {
      setLoading(false);
    }
  };

  // Auto-fetch on mount
  useEffect(() => {
    fetchLatestNews();
  }, []);

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col h-full max-h-[85vh]">
      {/* Header */}
      <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50/50">
        <h2 className="font-bold text-gray-900 flex items-center gap-2">
          <TrendingUp size={20} className="text-blue-600" />
          Market Insights
        </h2>
        
        <button 
          onClick={fetchLatestNews}
          disabled={loading}
          className={`p-2 rounded-lg transition-all hover:bg-gray-200 ${loading ? 'opacity-50' : 'opacity-100'}`}
          title="Refresh Insights"
        >
          <RefreshCw size={18} className={`text-gray-600 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-5">
        {error && (
          <div className="p-3 bg-red-50 text-red-600 text-xs rounded-lg border border-red-100">
            {error}
          </div>
        )}

        {!loading && news.length > 0 ? (
          news.map((item, i) => (
            <div key={i} className="group relative border-b border-gray-100 last:border-0 pb-4 last:pb-0">
              <a 
                href={item.url} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="block space-y-2"
              >
                <div className="flex justify-between items-start gap-2">
                  <h3 className="text-[13px] font-semibold text-gray-800 leading-tight group-hover:text-blue-600 transition-colors line-clamp-3">
                    {item.title}
                  </h3>
                  <ExternalLink size={12} className="text-gray-300 group-hover:text-blue-400 shrink-0 mt-1" />
                </div>
                
                <div className="flex items-center gap-3">
                  <span className="text-[10px] font-black uppercase text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">
                    {item.source?.name || "Market News"}
                  </span>
                  <div className="flex items-center gap-1 text-[10px] text-gray-400">
                    <Clock size={10} />
                    {item.publishedAt ? new Date(item.publishedAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : 'Recent'}
                  </div>
                </div>
              </a>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            {loading ? (
              <>
                <div className="w-8 h-8 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin mb-4"></div>
                <p className="text-xs text-gray-500 font-medium">Scanning Market Data...</p>
              </>
            ) : (
              <p className="text-xs text-gray-400 italic">No insights found. Click the refresh button above.</p>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-3 bg-gray-50/80 border-t border-gray-100">
        <button 
          onClick={fetchLatestNews}
          className="w-full text-center text-[11px] font-bold text-gray-500 hover:text-blue-600 uppercase tracking-widest transition-colors"
        >
          Check for Updates
        </button>
      </div>
    </div>
  );
}