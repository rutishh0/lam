import React, { useState, useEffect } from 'react';
import {
  Play,
  Pause,
  Square,
  Settings,
  Zap,
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle,
  RefreshCw,
  Activity,
  Bot,
  TrendingUp,
  Eye,
  Filter,
  Download
} from 'lucide-react';

const AutomationPanel = () => {
  const [automations, setAutomations] = useState([]);
  const [systemStatus, setSystemStatus] = useState('active');
  const [isLoading, setIsLoading] = useState(true);
  const [selectedAutomation, setSelectedAutomation] = useState(null);

  // Mock data - replace with real API calls
  useEffect(() => {
    const fetchAutomations = async () => {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAutomations([
        {
          id: 1,
          name: 'University Application Processing',
          description: 'Automated form filling and document submission for UK universities',
          status: 'running',
          progress: 85,
          lastRun: '2 minutes ago',
          nextRun: '1 hour',
          successRate: 94.5,
          tasksCompleted: 142,
          estimatedCompletion: '15 minutes',
          priority: 'high'
        },
        {
          id: 2,
          name: 'Document Analysis & Verification',
          description: 'AI-powered document processing and compliance checking',
          status: 'running',
          progress: 60,
          lastRun: '5 minutes ago',
          nextRun: '30 minutes',
          successRate: 97.2,
          tasksCompleted: 89,
          estimatedCompletion: '25 minutes',
          priority: 'medium'
        },
        {
          id: 3,
          name: 'Client Communication Management',
          description: 'Automated email responses and status updates',
          status: 'paused',
          progress: 0,
          lastRun: '1 hour ago',
          nextRun: 'Manual start',
          successRate: 89.1,
          tasksCompleted: 234,
          estimatedCompletion: 'N/A',
          priority: 'low'
        },
        {
          id: 4,
          name: 'Data Backup & Sync',
          description: 'Automated backup of client data and application files',
          status: 'scheduled',
          progress: 0,
          lastRun: '6 hours ago',
          nextRun: '2 hours',
          successRate: 99.8,
          tasksCompleted: 567,
          estimatedCompletion: 'N/A',
          priority: 'high'
        }
      ]);
      setIsLoading(false);
    };

    fetchAutomations();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'running':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'paused':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'scheduled':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'error':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running':
        return <Activity className="w-4 h-4" />;
      case 'paused':
        return <Pause className="w-4 h-4" />;
      case 'scheduled':
        return <Clock className="w-4 h-4" />;
      case 'error':
        return <XCircle className="w-4 h-4" />;
      default:
        return <Square className="w-4 h-4" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'text-red-600 bg-red-50';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'low':
        return 'text-green-600 bg-green-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const handleAction = (automationId, action) => {
    setAutomations(prev => 
      prev.map(automation => 
        automation.id === automationId 
          ? { 
              ...automation, 
              status: action === 'start' ? 'running' : action === 'pause' ? 'paused' : action 
            }
          : automation
      )
    );
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Automation Control</h1>
          <p className="text-gray-600 mt-1">
            Monitor and manage your AI automation workflows
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 px-3 py-2 bg-green-50 rounded-lg">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-green-700">System Online</span>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
            <Settings className="w-4 h-4" />
            <span>Settings</span>
          </button>
        </div>
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Bot className="w-6 h-6 text-blue-600" />
            </div>
            <span className="text-green-600 text-sm font-medium">+12% today</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">4</h3>
          <p className="text-sm text-gray-600">Active Automations</p>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <span className="text-green-600 text-sm font-medium">+8.5%</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">1,032</h3>
          <p className="text-sm text-gray-600">Tasks Completed</p>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
            <span className="text-green-600 text-sm font-medium">+2.1%</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">95.2%</h3>
          <p className="text-sm text-gray-600">Success Rate</p>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-orange-600" />
            </div>
            <span className="text-red-600 text-sm font-medium">-15min</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">4.2h</h3>
          <p className="text-sm text-gray-600">Avg Processing Time</p>
        </div>
      </div>

      {/* Automation List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100">
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Automation Workflows</h2>
            <div className="flex items-center space-x-3">
              <button className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                <Filter className="w-4 h-4" />
                <span>Filter</span>
              </button>
              <button className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
            </div>
          </div>
        </div>

        <div className="divide-y divide-gray-100">
          {automations.map((automation) => (
            <div key={automation.id} className="p-6 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-4 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{automation.name}</h3>
                    <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(automation.status)}`}>
                      {getStatusIcon(automation.status)}
                      <span className="capitalize">{automation.status}</span>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(automation.priority)}`}>
                      {automation.priority} priority
                    </span>
                  </div>
                  <p className="text-gray-600 mb-3">{automation.description}</p>
                  
                  {/* Progress Bar */}
                  {automation.status === 'running' && (
                    <div className="mb-3">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Progress</span>
                        <span className="font-medium">{automation.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${automation.progress}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 mt-1">
                        Estimated completion: {automation.estimatedCompletion}
                      </p>
                    </div>
                  )}

                  {/* Stats */}
                  <div className="flex items-center space-x-6 text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span>{automation.tasksCompleted} completed</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <TrendingUp className="w-4 h-4 text-blue-500" />
                      <span>{automation.successRate}% success rate</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4 text-orange-500" />
                      <span>Last run: {automation.lastRun}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <RefreshCw className="w-4 h-4 text-purple-500" />
                      <span>Next: {automation.nextRun}</span>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center space-x-2 ml-6">
                  <button 
                    onClick={() => setSelectedAutomation(automation)}
                    className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                    title="View details"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  
                  {automation.status === 'running' ? (
                    <button 
                      onClick={() => handleAction(automation.id, 'pause')}
                      className="flex items-center space-x-1 px-3 py-2 bg-yellow-100 text-yellow-700 rounded-lg hover:bg-yellow-200 transition-colors"
                    >
                      <Pause className="w-4 h-4" />
                      <span>Pause</span>
                    </button>
                  ) : (
                    <button 
                      onClick={() => handleAction(automation.id, 'start')}
                      className="flex items-center space-x-1 px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors"
                    >
                      <Play className="w-4 h-4" />
                      <span>Start</span>
                    </button>
                  )}
                  
                  <button 
                    onClick={() => handleAction(automation.id, 'stop')}
                    className="flex items-center space-x-1 px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
                  >
                    <Square className="w-4 h-4" />
                    <span>Stop</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AutomationPanel; 