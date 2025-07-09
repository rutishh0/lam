import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Play,
  Pause,
  Square,
  Monitor,
  Eye,
  Settings,
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  Zap,
  RefreshCw,
  Camera,
  Download,
  Maximize,
  Minimize,
  RotateCcw,
  MousePointer,
  Keyboard,
  Globe,
  Users,
  University,
  FileText,
  TrendingUp,
  Server
} from 'lucide-react';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;
const WS_URL = BACKEND_URL.replace('http', 'ws');

const AutomationControlPanel = () => {
  const [sessions, setSessions] = useState([]);
  const [activeSession, setActiveSession] = useState(null);
  const [browserView, setBrowserView] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState([]);
  const [showBrowserControls, setShowBrowserControls] = useState(false);
  const [automationStats, setAutomationStats] = useState({
    totalSessions: 0,
    activeSessions: 0,
    completedSessions: 0,
    errorSessions: 0
  });

  const wsRef = useRef(null);
  const browserCanvasRef = useRef(null);
  const logContainerRef = useRef(null);

  useEffect(() => {
    fetchSessions();
    const interval = setInterval(fetchSessions, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (activeSession) {
      connectWebSocket(activeSession.session_id);
    }
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [activeSession]);

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const fetchSessions = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.get(`${API}/admin/automation/sessions`, { headers });
      const sessionsData = response.data || [];
      
      setSessions(sessionsData);
      
      // Calculate stats
      const stats = {
        totalSessions: sessionsData.length,
        activeSessions: sessionsData.filter(s => s.status === 'running').length,
        completedSessions: sessionsData.filter(s => s.status === 'completed').length,
        errorSessions: sessionsData.filter(s => s.status === 'error').length
      };
      setAutomationStats(stats);
      
      setLoading(false);
    } catch (error) {
      console.error('Error fetching sessions:', error);
      toast.error('Failed to load automation sessions');
      setLoading(false);
    }
  };

  const connectWebSocket = (sessionId) => {
    if (wsRef.current) {
      wsRef.current.close();
    }

    const wsUrl = `${WS_URL}/ws/automation/${sessionId}`;
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      setIsConnected(true);
      addLog('info', 'WebSocket connected');
      
      // Request initial status
      sendWebSocketMessage({
        type: 'get_status',
        timestamp: new Date().toISOString()
      });
    };

    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      handleWebSocketMessage(message);
    };

    wsRef.current.onclose = () => {
      setIsConnected(false);
      addLog('warning', 'WebSocket disconnected');
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      addLog('error', 'WebSocket connection error');
    };
  };

  const sendWebSocketMessage = (message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  const handleWebSocketMessage = (message) => {
    switch (message.type) {
      case 'status_update':
        updateSessionStatus(message);
        addLog('info', `Status: ${message.current_step} (${message.progress}%)`);
        break;
        
      case 'screenshot':
        setBrowserView(message.data);
        break;
        
      case 'page_event':
        addLog('debug', `Page ${message.event}: ${JSON.stringify(message.data)}`);
        break;
        
      case 'automation_response':
        addLog('success', `${message.action} completed: ${message.success ? 'Success' : 'Failed'}`);
        break;
        
      case 'browser_action_response':
        addLog('info', `Browser action ${message.action}: ${message.success ? 'Success' : 'Failed'}`);
        break;
        
      default:
        console.log('Unknown WebSocket message:', message);
    }
  };

  const updateSessionStatus = (statusData) => {
    setSessions(prev => prev.map(session => 
      session.session_id === statusData.session_id 
        ? { ...session, ...statusData }
        : session
    ));

    if (activeSession && activeSession.session_id === statusData.session_id) {
      setActiveSession(prev => ({ ...prev, ...statusData }));
    }
  };

  const addLog = (level, message) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev.slice(-99), { // Keep last 100 logs
      id: Date.now(),
      timestamp,
      level,
      message
    }]);
  };

  const createNewSession = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.post(`${API}/admin/automation/sessions/create`, {
        client_id: 'demo-client',
        university_name: 'University of Oxford'
      }, { headers });

      if (response.data.success) {
        toast.success('New automation session created');
        fetchSessions();
      }
    } catch (error) {
      console.error('Error creating session:', error);
      toast.error('Failed to create automation session');
    }
  };

  const startAutomation = async (sessionId) => {
    try {
      const token = localStorage.getItem('auth_token');
      const headers = { Authorization: `Bearer ${token}` };

      const demoClientData = {
        full_name: "John Doe",
        email: "john.doe@example.com",
        phone: "+44 7700 900123",
        date_of_birth: "1995-05-15",
        nationality: "British",
        address: "123 Oxford Street, London, W1D 1DF, UK",
        personal_statement: "I am passionate about computer science and artificial intelligence...",
        academic_history: [
          { institution: "Royal Grammar School", qualification: "A-Levels", grade: "A*AA", year: 2022 }
        ],
        course_preferences: [
          { course_name: "Computer Science", course_code: "CS101", entry_year: 2024 }
        ]
      };

      sendWebSocketMessage({
        type: 'start_automation',
        client_data: demoClientData
      });

      toast.success('Automation started');
    } catch (error) {
      console.error('Error starting automation:', error);
      toast.error('Failed to start automation');
    }
  };

  const pauseAutomation = (sessionId) => {
    sendWebSocketMessage({ type: 'pause_automation' });
    toast.info('Automation paused');
  };

  const resumeAutomation = (sessionId) => {
    sendWebSocketMessage({ type: 'resume_automation' });
    toast.info('Automation resumed');
  };

  const stopAutomation = (sessionId) => {
    sendWebSocketMessage({ type: 'stop_automation' });
    toast.warning('Automation stopped');
  };

  const captureScreenshot = () => {
    sendWebSocketMessage({ 
      type: 'request_screenshot',
      timestamp: new Date().toISOString()
    });
  };

  const handleBrowserClick = (event) => {
    if (!showBrowserControls) return;
    
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    sendWebSocketMessage({
      type: 'browser_action',
      action: {
        type: 'click',
        x: Math.round(x),
        y: Math.round(y)
      }
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return 'text-green-600 bg-green-100';
      case 'paused': return 'text-yellow-600 bg-yellow-100';
      case 'completed': return 'text-blue-600 bg-blue-100';
      case 'error': return 'text-red-600 bg-red-100';
      case 'stopped': return 'text-gray-600 bg-gray-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running': return <Activity className="w-4 h-4" />;
      case 'paused': return <Pause className="w-4 h-4" />;
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'error': return <AlertCircle className="w-4 h-4" />;
      case 'stopped': return <Square className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const StatCard = ({ title, value, icon: Icon, color = 'blue' }) => (
    <div className="bg-white rounded-lg shadow-md p-4 border-l-4 border-blue-500">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <Icon className={`w-8 h-8 text-${color}-500`} />
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-500" />
        <span className="ml-2 text-lg text-gray-600">Loading automation control panel...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AI Automation Control</h2>
          <p className="text-gray-600">Monitor and control university application automation</p>
        </div>
        <button
          onClick={createNewSession}
          className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          <Play className="w-4 h-4" />
          <span>New Session</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard
          title="Total Sessions"
          value={automationStats.totalSessions}
          icon={Server}
          color="blue"
        />
        <StatCard
          title="Active Sessions"
          value={automationStats.activeSessions}
          icon={Activity}
          color="green"
        />
        <StatCard
          title="Completed"
          value={automationStats.completedSessions}
          icon={CheckCircle}
          color="purple"
        />
        <StatCard
          title="Errors"
          value={automationStats.errorSessions}
          icon={AlertCircle}
          color="red"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sessions List */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Automation Sessions</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {sessions.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Server className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                  <p>No automation sessions yet</p>
                  <button
                    onClick={createNewSession}
                    className="mt-4 text-blue-600 hover:text-blue-700"
                  >
                    Create your first session
                  </button>
                </div>
              ) : (
                sessions.map((session) => (
                  <div
                    key={session.session_id}
                    className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                      activeSession?.session_id === session.session_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setActiveSession(session)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <University className="w-4 h-4 text-gray-600" />
                        <span className="font-medium text-gray-900">
                          {session.university_name}
                        </span>
                      </div>
                      <span className={`inline-flex items-center space-x-1 px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(session.status)}`}>
                        {getStatusIcon(session.status)}
                        <span>{session.status}</span>
                      </span>
                    </div>
                    <div className="text-sm text-gray-600">
                      <p>Client: {session.client_id}</p>
                      <p>Created: {new Date(session.created_at).toLocaleString()}</p>
                      {session.current_step && (
                        <p>Step: {session.current_step} ({session.progress || 0}%)</p>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Session Control */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Session Control</h3>
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-sm text-gray-600">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
          </div>
          <div className="p-6">
            {activeSession ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => startAutomation(activeSession.session_id)}
                    disabled={activeSession.status === 'running'}
                    className="flex items-center justify-center space-x-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Play className="w-4 h-4" />
                    <span>Start</span>
                  </button>
                  <button
                    onClick={() => pauseAutomation(activeSession.session_id)}
                    disabled={activeSession.status !== 'running'}
                    className="flex items-center justify-center space-x-2 px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Pause className="w-4 h-4" />
                    <span>Pause</span>
                  </button>
                  <button
                    onClick={() => resumeAutomation(activeSession.session_id)}
                    disabled={activeSession.status !== 'paused'}
                    className="flex items-center justify-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Play className="w-4 h-4" />
                    <span>Resume</span>
                  </button>
                  <button
                    onClick={() => stopAutomation(activeSession.session_id)}
                    disabled={!['running', 'paused'].includes(activeSession.status)}
                    className="flex items-center justify-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Square className="w-4 h-4" />
                    <span>Stop</span>
                  </button>
                </div>

                <div className="border-t pt-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Progress</span>
                    <span className="text-sm text-gray-600">{activeSession.progress || 0}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${activeSession.progress || 0}%` }}
                    ></div>
                  </div>
                  {activeSession.current_step && (
                    <p className="text-sm text-gray-600 mt-2">{activeSession.current_step}</p>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Monitor className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                <p>Select a session to control</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Browser View and Logs */}
      {activeSession && (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Browser View */}
          <div className="xl:col-span-2 bg-white rounded-lg shadow-md">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">Live Browser View</h3>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setShowBrowserControls(!showBrowserControls)}
                    className={`p-2 rounded-lg ${showBrowserControls ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-600'}`}
                    title="Toggle browser controls"
                  >
                    <MousePointer className="w-4 h-4" />
                  </button>
                  <button
                    onClick={captureScreenshot}
                    className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200"
                    title="Capture screenshot"
                  >
                    <Camera className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
            <div className="p-6">
              <div className="border border-gray-300 rounded-lg overflow-hidden bg-gray-50">
                {browserView ? (
                  <img
                    ref={browserCanvasRef}
                    src={`data:image/png;base64,${browserView}`}
                    alt="Browser view"
                    className="w-full h-auto cursor-pointer"
                    onClick={handleBrowserClick}
                    style={{ maxHeight: '600px', objectFit: 'contain' }}
                  />
                ) : (
                  <div className="flex items-center justify-center h-64 text-gray-500">
                    <div className="text-center">
                      <Eye className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                      <p>No browser view available</p>
                      <p className="text-sm">Start automation to see live browser</p>
                    </div>
                  </div>
                )}
              </div>
              {showBrowserControls && (
                <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-800 mb-2">
                    <MousePointer className="w-4 h-4 inline mr-1" />
                    Browser controls enabled - Click on the browser view to interact
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Activity Logs */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Activity Logs</h3>
            </div>
            <div className="p-6">
              <div
                ref={logContainerRef}
                className="h-96 overflow-y-auto bg-gray-900 rounded-lg p-4 font-mono text-sm"
              >
                {logs.length === 0 ? (
                  <div className="text-gray-500 text-center py-8">
                    No logs yet
                  </div>
                ) : (
                  logs.map((log) => (
                    <div key={log.id} className="mb-1">
                      <span className="text-gray-400">[{log.timestamp}]</span>
                      <span className={`ml-2 ${
                        log.level === 'error' ? 'text-red-400' :
                        log.level === 'warning' ? 'text-yellow-400' :
                        log.level === 'success' ? 'text-green-400' :
                        log.level === 'info' ? 'text-blue-400' :
                        'text-gray-300'
                      }`}>
                        {log.message}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AutomationControlPanel;
