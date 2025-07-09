import React, { useState, useEffect } from 'react';
import {
  Users,
  FileText,
  Zap,
  Clock,
  CheckCircle,
  AlertTriangle,
  Activity,
  TrendingUp,
  Bot,
  Calendar,
  Star,
  ArrowRight,
  Play,
  Pause,
  RefreshCw
} from 'lucide-react';
import MetricCard from './MetricCard';

const ModernDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [automationStatus, setAutomationStatus] = useState('active');

  // Mock data - replace with real API calls
  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setDashboardData({
        totalApplications: 142,
        activeClients: 38,
        successRate: 94.5,
        pendingTasks: 12,
        weeklyGrowth: 15.8,
        monthlyRevenue: 28500,
        averageProcessingTime: 4.2,
        automationHealth: 98.5
      });
      setIsLoading(false);
    };

    fetchDashboardData();
  }, []);

  const recentApplications = [
    {
      id: 1,
      client: 'Sarah Chen',
      university: 'Oxford University',
      status: 'submitted',
      submittedAt: '2 hours ago'
    },
    {
      id: 2,
      client: 'James Wilson',
      university: 'Cambridge University',
      status: 'processing',
      submittedAt: '4 hours ago'
    },
    {
      id: 3,
      client: 'Priya Patel',
      university: 'Imperial College',
      status: 'accepted',
      submittedAt: '1 day ago'
    },
    {
      id: 4,
      client: 'Mohammed Al-Ahmad',
      university: 'UCL',
      status: 'submitted',
      submittedAt: '1 day ago'
    }
  ];

  const aiTasks = [
    {
      id: 1,
      task: 'Processing personal statement for Oxford application',
      progress: 85,
      client: 'Sarah Chen',
      estimatedCompletion: '15 min'
    },
    {
      id: 2,
      task: 'Document verification and analysis',
      progress: 60,
      client: 'James Wilson',
      estimatedCompletion: '30 min'
    },
    {
      id: 3,
      task: 'Application form auto-filling',
      progress: 95,
      client: 'Lisa Zhang',
      estimatedCompletion: '5 min'
    }
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'submitted':
        return 'bg-blue-100 text-blue-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      case 'accepted':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Welcome back! Here's what's happening with your automation system.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button 
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all ${
              automationStatus === 'active' 
                ? 'bg-green-100 text-green-700 hover:bg-green-200' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
            onClick={() => setAutomationStatus(automationStatus === 'active' ? 'paused' : 'active')}
          >
            {automationStatus === 'active' ? (
              <>
                <Pause className="w-4 h-4" />
                <span>Pause AI</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Start AI</span>
              </>
            )}
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Applications"
          value={dashboardData?.totalApplications || 0}
          icon={FileText}
          trend="up"
          trendValue="+12%"
          description="This month"
          color="blue"
          isLoading={isLoading}
        />
        <MetricCard
          title="Active Clients"
          value={dashboardData?.activeClients || 0}
          icon={Users}
          trend="up"
          trendValue="+8"
          description="New this week"
          color="green"
          isLoading={isLoading}
        />
        <MetricCard
          title="Success Rate"
          value={`${dashboardData?.successRate || 0}%`}
          icon={Star}
          trend="up"
          trendValue="+2.3%"
          description="Last 30 days"
          color="purple"
          isLoading={isLoading}
        />
        <MetricCard
          title="AI Tasks Pending"
          value={dashboardData?.pendingTasks || 0}
          icon={Zap}
          trend="down"
          trendValue="-5"
          description="Processing queue"
          color="orange"
          isLoading={isLoading}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Applications */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Recent Applications</h2>
            <button className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center space-x-1">
              <span>View all</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
          
          <div className="space-y-4">
            {recentApplications.map((app) => (
              <div key={app.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {app.client.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{app.client}</p>
                    <p className="text-sm text-gray-600">{app.university}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(app.status)}`}>
                    {app.status}
                  </span>
                  <p className="text-xs text-gray-500 mt-1">{app.submittedAt}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Task Monitor */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">AI Tasks</h2>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-green-600 font-medium">Active</span>
            </div>
          </div>
          
          <div className="space-y-4">
            {aiTasks.map((task) => (
              <div key={task.id} className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900 mb-1">{task.task}</p>
                    <p className="text-xs text-gray-600">Client: {task.client}</p>
                  </div>
                  <span className="text-xs text-gray-500">{task.estimatedCompletion}</span>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-gray-600">Progress</span>
                    <span className="font-medium">{task.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${task.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <button className="w-full mt-4 py-2 text-sm text-blue-600 hover:text-blue-700 font-medium border border-blue-200 rounded-lg hover:bg-blue-50 transition-colors">
            View All Tasks
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all group">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200 transition-colors">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-left">
              <p className="font-medium text-gray-900">Add Client</p>
              <p className="text-sm text-gray-600">Create new client profile</p>
            </div>
          </button>
          
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:border-purple-300 hover:bg-purple-50 transition-all group">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center group-hover:bg-purple-200 transition-colors">
              <Bot className="w-5 h-5 text-purple-600" />
            </div>
            <div className="text-left">
              <p className="font-medium text-gray-900">New Automation</p>
              <p className="text-sm text-gray-600">Set up AI task</p>
            </div>
          </button>
          
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:border-green-300 hover:bg-green-50 transition-all group">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center group-hover:bg-green-200 transition-colors">
              <FileText className="w-5 h-5 text-green-600" />
            </div>
            <div className="text-left">
              <p className="font-medium text-gray-900">Upload Documents</p>
              <p className="text-sm text-gray-600">Add client files</p>
            </div>
          </button>
          
          <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:border-orange-300 hover:bg-orange-50 transition-all group">
            <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center group-hover:bg-orange-200 transition-colors">
              <Activity className="w-5 h-5 text-orange-600" />
            </div>
            <div className="text-left">
              <p className="font-medium text-gray-900">View Analytics</p>
              <p className="text-sm text-gray-600">Performance insights</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModernDashboard; 