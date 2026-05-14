"use client"; // <--- ADD THIS
import React, { useState } from 'react';

export default function ScoutEngine() {
  const [formData, setFormData] = useState({ role: '', location: '', skills: '' });
  const [status, setStatus] = useState('idle'); // idle, processing, success
  const [results, setResults] = useState(null);

  const startScout = async (e) => {
    e.preventDefault();
    setStatus('processing');

    // 1. Send the Criteria to your FastAPI /scout endpoint
    const response = await fetch('http://localhost:8000/api/v1/scout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        role: formData.role,
        location: formData.location,
        required_skills: formData.skills.split(',').map(s => s.trim())
      }),
    });

    const { task_id } = await response.json();

    // 2. The Polling Logic (The "Is it ready yet?" loop)
    const pollInterval = setInterval(async () => {
      const taskRes = await fetch(`http://localhost:8000/api/v1/tasks/${task_id}`);
      const taskData = await taskRes.json();

      if (taskData.status === 'SUCCESS') {
        setResults(taskData.result);
        setStatus('success');
        clearInterval(pollInterval); // Stop the loop
      } else if (taskData.status === 'FAILURE') {
        alert("Agent encountered an error.");
        setStatus('idle');
        clearInterval(pollInterval);
      }
    }, 2000); // Check every 2 seconds
  };

  return (
    <div className="space-y-6">
      <form onSubmit={startScout} className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input 
            className="p-2 border rounded border-gray-300 outline-none focus:border-blue-500"
            placeholder="Target Role"
            onChange={(e) => setFormData({...formData, role: e.target.value})}
            required
          />
          <input 
            className="p-2 border rounded border-gray-300 outline-none focus:border-blue-500"
            placeholder="City"
            onChange={(e) => setFormData({...formData, location: e.target.value})}
            required
          />
          <input 
            className="md:col-span-2 p-2 border rounded border-gray-300 outline-none focus:border-blue-500"
            placeholder="Skills (comma separated)"
            onChange={(e) => setFormData({...formData, skills: e.target.value})}
            required
          />
        </div>
        <button 
          disabled={status === 'processing'}
          className="mt-4 w-full bg-blue-600 text-white py-2 rounded-full font-semibold hover:bg-blue-700 disabled:bg-gray-400"
        >
          {status === 'processing' ? '🕵️ Agent Hunting...' : 'Launch Talent Scout'}
        </button>
      </form>

      {status === 'success' && (
        <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
          <h3 className="text-lg font-bold mb-4 text-green-700">✓ Mission Complete</h3>
          <div className="bg-gray-50 p-4 rounded text-sm font-mono text-gray-700 whitespace-pre-wrap">
            {JSON.stringify(results, null, 2)}
          </div>
        </div>
      )}
    </div>
  );
}