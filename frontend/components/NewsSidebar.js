"use client";

import React, { useState, useEffect } from 'react';

const NewsSidebar = ({ type, title, subtitle }) => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      try {
        // Construct the URL using your environment variable and the API prefix
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const endpoint = type === 'corporate' ? '/api/v1/corporate' : '/api/v1/news';
        
        const response = await fetch(`${baseUrl}${endpoint}`);
        
        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }
        
        const data = await response.json();
        setNews(data.results || []);
      } catch (error) {
        console.error("Failed to fetch news:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, [type]);

  if (loading) return <div className="p-4 text-gray-500">Loading {title}...</div>;

  return (
    <div className="bg-white rounded-lg shadow h-full overflow-hidden flex flex-col">
      <div className="p-4 border-b">
        <h2 className="font-bold text-lg">{title}</h2>
        <p className="text-xs text-gray-400">{subtitle}</p>
      </div>
      <div className="overflow-y-auto flex-1 p-4 space-y-4">
        {news.map((item, index) => (
          <div key={index} className="border-b pb-2">
            <a 
              href={item.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="text-sm font-medium hover:text-blue-600 block"
            >
              {item.title}
            </a>
            <p className="text-xs text-gray-500 mt-1">{item.source?.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewsSidebar;