import React, { useEffect, useRef, useState } from 'react';
import config from '../config';

export default function AgentChat({ token }) {
  const [threadId, setThreadId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [runId, setRunId] = useState(null);
  const [events, setEvents] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    // Create a thread on mount
    const createThread = async () => {
      const res = await fetch(`${config.apiUrl}/api/agent/threads`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({})
      });
      const data = await res.json();
      setThreadId(data.thread_id);
    };
    createThread();
  }, [token]);

  const sendMessage = async () => {
    if (!threadId || !input.trim()) return;
    await fetch(`${config.apiUrl}/api/agent/threads/${threadId}/messages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ role: 'user', content: input })
    });
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
  };

  const startRun = async (targetUrl) => {
    if (!threadId) return;
    const res = await fetch(`${config.apiUrl}/api/agent/runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ thread_id: threadId, target_url: targetUrl })
    });
    const data = await res.json();
    setRunId(data.run_id);

    // Open WS and start
    const wsUrl = (config.wsUrl || config.apiUrl.replace('http', 'ws')) + `/api/agent/ws/agent/${data.run_id}`.replace('/api/agent', '');
    const ws = new WebSocket(`${config.wsUrl}/api/agent/ws/agent/${data.run_id}`.replace('/api/agent', ''));
    wsRef.current = ws;
    ws.onmessage = (evt) => {
      try { setEvents(prev => [...prev, JSON.parse(evt.data)]); } catch {}
    };

    await fetch(`${config.apiUrl}/api/agent/runs/${data.run_id}/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ target_url: targetUrl, mode: 'general' })
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-4">Agent Chat</h3>
      <div className="space-y-3 mb-4 max-h-64 overflow-auto">
        {messages.map((m, idx) => (
          <div key={idx} className="p-3 rounded-lg" style={{backgroundColor: m.role === 'user' ? '#eef2ff' : '#f1f5f9'}}>
            <div className="text-xs text-gray-500 mb-1">{m.role}</div>
            <div className="text-gray-800 whitespace-pre-wrap">{m.content}</div>
          </div>
        ))}
      </div>
      <div className="flex space-x-2 mb-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
          placeholder="Describe what to do..."
        />
        <button onClick={sendMessage} className="px-4 py-2 bg-blue-600 text-white rounded-lg">Send</button>
      </div>
      <div className="flex space-x-2 mb-4">
        <input id="targetUrl" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" placeholder="https://target.example.com" />
        <button onClick={() => startRun(document.getElementById('targetUrl').value)} className="px-4 py-2 bg-purple-600 text-white rounded-lg">Start Run</button>
      </div>
      <div className="border rounded-lg p-3 max-h-64 overflow-auto text-sm bg-gray-50">
        {events.map((e, i) => (
          <div key={i} className="mb-2">
            <div className="text-gray-600">{e.type}</div>
            {e.type === 'tool_progress' && e.screenshot && (
              <img alt="screenshot" src={`data:image/png;base64,${e.screenshot}`} className="mt-2 border rounded" />
            )}
            {e.error && <div className="text-red-600">{e.error}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}



