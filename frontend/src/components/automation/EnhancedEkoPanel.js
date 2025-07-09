import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Bot,
  Brain,
  FileText,
  Monitor,
  Play,
  Pause,
  Square,
  Zap,
  Clock,
  CheckCircle,
  AlertCircle,
  Settings,
  ChevronRight,
  Activity,
  Sparkles,
  Globe,
  Upload,
  Eye,
  RefreshCw,
  Users,
  Layers,
  GitBranch,
  Cpu,
  Database,
  Lightning,
  Network,
  Target,
  BarChart3,
  Timer,
  ArrowRight,
  Plus,
  Trash2,
  Info
} from 'lucide-react';
import toast from 'react-hot-toast';

const EnhancedEkoPanel = () => {
  const [isInitialized, setIsInitialized] = useState(false);
  const [capabilities, setCapabilities] = useState(null);
  const [sessionStatus, setSessionStatus] = useState(null);
  const [activeWorkflows, setActiveWorkflows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [parallelApplications, setParallelApplications] = useState([]);
  const [monitoringPortals, setMonitoringPortals] = useState([]);

  useEffect(() => {
    checkEnhancedEkoStatus();
    fetchEnhancedCapabilities();
    fetchSessionStatus();
  }, []);

  const checkEnhancedEkoStatus = async () => {
    try {
      const response = await fetch('/api/eko-enhanced/health-enhanced');
      const data = await response.json();
      setIsInitialized(data.status === 'healthy');
    } catch (error) {
      console.error('Error checking Enhanced Eko status:', error);
      setIsInitialized(false);
    }
  };

  const initializeEnhancedEko = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/eko-enhanced/initialize-enhanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        setIsInitialized(true);
        toast.success('Enhanced Eko automation framework initialized successfully!');
        await fetchEnhancedCapabilities();
        await fetchSessionStatus();
      } else {
        throw new Error('Failed to initialize Enhanced Eko');
      }
    } catch (error) {
      toast.error('Failed to initialize Enhanced Eko automation');
      console.error('Enhanced Eko initialization error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEnhancedCapabilities = async () => {
    try {
      const response = await fetch('/api/eko-enhanced/capabilities/advanced', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setCapabilities(data);
      }
    } catch (error) {
      console.error('Error fetching enhanced capabilities:', error);
    }
  };

  const fetchSessionStatus = async () => {
    try {
      const response = await fetch('/api/eko-enhanced/sessions/status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setSessionStatus(data);
      }
    } catch (error) {
      console.error('Error fetching session status:', error);
    }
  };

  const createBrowserSession = async (sessionType = 'isolated', options = {}) => {
    try {
      const response = await fetch('/api/eko-enhanced/browser-session/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          session_type: sessionType,
          headless: true,
          ...options
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success(`Browser session created: ${result.session_id}`);
        await fetchSessionStatus();
        return result.session_id;
      } else {
        throw new Error('Failed to create browser session');
      }
    } catch (error) {
      toast.error('Failed to create browser session');
      console.error('Session creation error:', error);
    }
  };

  const processParallelApplications = async () => {
    if (parallelApplications.length === 0) {
      toast.error('Please add at least one university application');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/eko-enhanced/applications/parallel', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          applications: parallelApplications,
          max_concurrent: 3,
          use_separate_browsers: true
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success(`Parallel processing started for ${parallelApplications.length} applications!`);
        await fetchSessionStatus();
        return result;
      } else {
        throw new Error('Failed to start parallel processing');
      }
    } catch (error) {
      toast.error('Failed to start parallel application processing');
      console.error('Parallel processing error:', error);
    } finally {
      setLoading(false);
    }
  };

  const startPortalMonitoring = async () => {
    if (monitoringPortals.length === 0) {
      toast.error('Please add at least one portal to monitor');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/eko-enhanced/portals/monitor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          portals: monitoringPortals,
          monitoring_interval: 300 // 5 minutes
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success(`Portal monitoring started for ${monitoringPortals.length} portals!`);
        await fetchSessionStatus();
        return result;
      } else {
        throw new Error('Failed to start portal monitoring');
      }
    } catch (error) {
      toast.error('Failed to start portal monitoring');
      console.error('Portal monitoring error:', error);
    } finally {
      setLoading(false);
    }
  };

  const createIntelligentWorkflow = async (workflowDescription, coordinationStrategy = 'adaptive') => {
    setLoading(true);
    try {
      const response = await fetch('/api/eko-enhanced/workflow/intelligent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          workflow_description: workflowDescription,
          coordination_strategy: coordinationStrategy
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success('Intelligent workflow created successfully!');
        await fetchSessionStatus();
        return result;
      } else {
        throw new Error('Failed to create intelligent workflow');
      }
    } catch (error) {
      toast.error('Failed to create intelligent workflow');
      console.error('Intelligent workflow error:', error);
    } finally {
      setLoading(false);
    }
  };

  const cleanupBrowserSessions = async (sessionIds = null) => {
    try {
      const response = await fetch('/api/eko-enhanced/sessions/cleanup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          session_ids: sessionIds
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success(`Cleaned up ${result.cleaned_sessions.length} browser sessions`);
        await fetchSessionStatus();
        return result;
      } else {
        throw new Error('Failed to cleanup sessions');
      }
    } catch (error) {
      toast.error('Failed to cleanup browser sessions');
      console.error('Session cleanup error:', error);
    }
  };

  const addParallelApplication = () => {
    const university = prompt('University name:');
    const url = prompt('Application URL:');
    if (university && url) {
      setParallelApplications([...parallelApplications, {
        university_name: university,
        application_url: url,
        client_profile: {
          firstName: 'John',
          lastName: 'Doe',
          email: 'john@example.com'
        },
        documents: ['transcript.pdf', 'personal_statement.pdf']
      }]);
    }
  };

  const addMonitoringPortal = () => {
    const university = prompt('University name:');
    const url = prompt('Portal URL:');
    if (university && url) {
      setMonitoringPortals([...monitoringPortals, {
        university: university,
        portal_url: url,
        credentials: { username: 'user', password: 'pass' }
      }]);
    }
  };

  const SessionTypeCard = ({ type, description, useCases, isActive, onSelect }) => (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
        isActive 
          ? 'border-teal-500 bg-teal-50' 
          : 'border-gray-200 bg-white hover:border-teal-300'
      }`}
      onClick={onSelect}
    >
      <div className="flex items-center mb-2">
        <Layers className="w-5 h-5 text-teal-600 mr-2" />
        <h3 className="font-semibold text-gray-900 capitalize">{type}</h3>
      </div>
      <p className="text-sm text-gray-600 mb-3">{description}</p>
      <div className="space-y-1">
        {useCases.slice(0, 2).map((useCase, index) => (
          <span key={index} className="inline-block bg-gray-100 text-xs px-2 py-1 rounded mr-2">
            {useCase}
          </span>
        ))}
      </div>
    </motion.div>
  );

  const MetricCard = ({ title, value, icon: Icon, color, change }) => (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-lg flex items-center justify-center bg-gradient-to-br from-${color}-500 to-${color}-600`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {change && (
          <span className={`text-sm font-medium ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
            {change > 0 ? '+' : ''}{change}%
          </span>
        )}
      </div>
      <h3 className="text-2xl font-bold text-gray-900 mb-1">{value}</h3>
      <p className="text-sm text-gray-600">{title}</p>
    </div>
  );

  const WorkflowCard = ({ title, description, example, action, icon: Icon }) => (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-200"
    >
      <div className="flex items-center mb-4">
        <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg flex items-center justify-center mr-3">
          <Icon className="w-5 h-5 text-white" />
        </div>
        <h3 className="font-semibold text-gray-900">{title}</h3>
      </div>
      <p className="text-sm text-gray-600 mb-4">{description}</p>
      {example && (
        <div className="bg-gray-50 rounded-lg p-3 mb-4">
          <p className="text-xs text-gray-500 mb-1">Example:</p>
          <p className="text-sm text-gray-700">{example.workflow_description}</p>
        </div>
      )}
      <button
        onClick={action}
        className="w-full bg-gradient-to-r from-teal-600 to-cyan-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:shadow-lg transition-all duration-200"
      >
        Start Workflow
      </button>
    </motion.div>
  );

  if (!isInitialized) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-teal-50 to-cyan-50 p-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-16"
          >
            <div className="w-24 h-24 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-full flex items-center justify-center mx-auto mb-8">
              <Lightning className="w-12 h-12 text-white" />
            </div>
            
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Enhanced Eko Automation Framework
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Advanced multi-browser automation with parallel processing, intelligent coordination, 
              and enterprise-grade session management for university applications.
            </p>
            
            <div className="grid md:grid-cols-4 gap-6 mb-12">
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Users className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Multi-Browser Sessions</h3>
                <p className="text-sm text-gray-600">
                  Run multiple browser instances simultaneously
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Zap className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Parallel Processing</h3>
                <p className="text-sm text-gray-600">
                  Process multiple applications at the same time
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Brain className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Intelligent Coordination</h3>
                <p className="text-sm text-gray-600">
                  AI optimizes browser usage automatically
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Network className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Session Management</h3>
                <p className="text-sm text-gray-600">
                  Advanced session isolation and persistence
                </p>
              </div>
            </div>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={initializeEnhancedEko}
              disabled={loading}
              className="bg-gradient-to-r from-teal-600 to-cyan-600 text-white px-8 py-4 rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center">
                  <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                  Initializing Enhanced Eko...
                </div>
              ) : (
                <div className="flex items-center">
                  <Lightning className="w-5 h-5 mr-2" />
                  Initialize Enhanced Framework
                </div>
              )}
            </motion.button>
          </motion.div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg flex items-center justify-center mr-3">
                <Lightning className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Enhanced Eko Automation</h1>
                <p className="text-sm text-gray-600">Multi-browser AI automation platform</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-green-600 bg-green-50 px-3 py-1 rounded-full">
                <CheckCircle className="w-4 h-4 mr-1" />
                Enhanced Framework Active
              </div>
              {sessionStatus && (
                <div className="flex items-center text-sm text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                  <Database className="w-4 h-4 mr-1" />
                  {sessionStatus.total_sessions} Active Sessions
                </div>
              )}
              <button 
                onClick={() => cleanupBrowserSessions()}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-lg"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            </div>
          </div>
          
          {/* Navigation Tabs */}
          <div className="flex space-x-8 mt-6">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'parallel', label: 'Parallel Processing', icon: Users },
              { id: 'monitoring', label: 'Portal Monitoring', icon: Monitor },
              { id: 'sessions', label: 'Browser Sessions', icon: Layers },
              { id: 'workflows', label: 'Intelligent Workflows', icon: Brain }
            ].map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setSelectedTab(tab.id)}
                  className={`flex items-center px-1 py-2 border-b-2 font-medium text-sm transition-colors ${
                    selectedTab === tab.id
                      ? 'border-teal-500 text-teal-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          {selectedTab === 'dashboard' && (
            <motion.div
              key="dashboard"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Enhanced Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                  title="Active Sessions"
                  value={sessionStatus?.total_sessions || 0}
                  icon={Database}
                  color="teal"
                  change={15}
                />
                <MetricCard
                  title="Parallel Workflows"
                  value={activeWorkflows.length}
                  icon={Users}
                  color="blue"
                  change={8}
                />
                <MetricCard
                  title="Success Rate"
                  value="98.5%"
                  icon={Target}
                  color="green"
                  change={2.1}
                />
                <MetricCard
                  title="Performance Boost"
                  value="4.2x"
                  icon={Zap}
                  color="purple"
                  change={12}
                />
              </div>

              {/* Enhanced Workflow Templates */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Enhanced Automation Workflows</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <WorkflowCard
                    title="Parallel Applications"
                    description="Apply to multiple universities simultaneously using separate browser instances"
                    example={{
                      workflow_description: "Apply to Oxford, Cambridge, Imperial, UCL, and King's College simultaneously"
                    }}
                    icon={Users}
                    action={() => setSelectedTab('parallel')}
                  />
                  <WorkflowCard
                    title="Portal Monitoring"
                    description="Monitor multiple university portals continuously with dedicated sessions"
                    example={{
                      workflow_description: "Monitor all application portals every 30 minutes"
                    }}
                    icon={Monitor}
                    action={() => setSelectedTab('monitoring')}
                  />
                  <WorkflowCard
                    title="Intelligent Coordination"
                    description="Let AI automatically determine the optimal browser coordination strategy"
                    example={{
                      workflow_description: "Complete all university applications with optimal efficiency"
                    }}
                    icon={Brain}
                    action={() => createIntelligentWorkflow("Complete all my university applications efficiently", "adaptive")}
                  />
                </div>
              </div>
            </motion.div>
          )}

          {selectedTab === 'parallel' && (
            <motion.div
              key="parallel"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">Parallel Application Processing</h2>
                    <p className="text-sm text-gray-600">Process multiple university applications simultaneously</p>
                  </div>
                  <button
                    onClick={addParallelApplication}
                    className="flex items-center bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Application
                  </button>
                </div>

                {parallelApplications.length > 0 ? (
                  <div className="space-y-4 mb-6">
                    {parallelApplications.map((app, index) => (
                      <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div>
                          <h3 className="font-medium text-gray-900">{app.university_name}</h3>
                          <p className="text-sm text-gray-600">{app.application_url}</p>
                        </div>
                        <button
                          onClick={() => setParallelApplications(parallelApplications.filter((_, i) => i !== index))}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Users className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>No applications added yet</p>
                  </div>
                )}

                <button
                  onClick={processParallelApplications}
                  disabled={loading || parallelApplications.length === 0}
                  className="w-full bg-gradient-to-r from-teal-600 to-cyan-600 text-white py-3 px-6 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all duration-200"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                      Processing Applications...
                    </div>
                  ) : (
                    <div className="flex items-center justify-center">
                      <Play className="w-5 h-5 mr-2" />
                      Start Parallel Processing ({parallelApplications.length} applications)
                    </div>
                  )}
                </button>
              </div>
            </motion.div>
          )}

          {selectedTab === 'sessions' && sessionStatus && (
            <motion.div
              key="sessions"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-gray-900">Browser Session Management</h2>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => createBrowserSession('isolated')}
                      className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors"
                    >
                      Create Session
                    </button>
                    <button
                      onClick={() => cleanupBrowserSessions()}
                      className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                    >
                      Cleanup All
                    </button>
                  </div>
                </div>

                {capabilities && (
                  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                    {capabilities.multi_browser_support.session_types.map((sessionType, index) => (
                      <SessionTypeCard
                        key={index}
                        type={sessionType.type}
                        description={sessionType.description}
                        useCases={sessionType.use_cases}
                        isActive={false}
                        onSelect={() => createBrowserSession(sessionType.type)}
                      />
                    ))}
                  </div>
                )}

                {sessionStatus.active_sessions.length > 0 ? (
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Active Sessions</h3>
                    {sessionStatus.active_sessions.map((sessionId, index) => {
                      const details = sessionStatus.session_details[sessionId];
                      return (
                        <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <h4 className="font-medium text-gray-900">{sessionId}</h4>
                            <p className="text-sm text-gray-600">
                              Type: {details?.session_type} | Headless: {details?.headless ? 'Yes' : 'No'}
                            </p>
                          </div>
                          <button
                            onClick={() => cleanupBrowserSessions([sessionId])}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    <Database className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p>No active browser sessions</p>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default EnhancedEkoPanel;
