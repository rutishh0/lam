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
  RefreshCw
} from 'lucide-react';
import toast from 'react-hot-toast';

const EkoAutomationPanel = () => {
  const [isInitialized, setIsInitialized] = useState(false);
  const [capabilities, setCapabilities] = useState(null);
  const [workflowHistory, setWorkflowHistory] = useState([]);
  const [activeWorkflows, setActiveWorkflows] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTab, setSelectedTab] = useState('dashboard');

  useEffect(() => {
    checkEkoStatus();
    fetchCapabilities();
    fetchWorkflowHistory();
  }, []);

  const checkEkoStatus = async () => {
    try {
      const response = await fetch('/api/eko/health');
      const data = await response.json();
      setIsInitialized(data.status === 'healthy');
    } catch (error) {
      console.error('Error checking Eko status:', error);
      setIsInitialized(false);
    }
  };

  const initializeEko = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/eko/initialize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        setIsInitialized(true);
        toast.success('Eko automation framework initialized successfully!');
        await fetchCapabilities();
      } else {
        throw new Error('Failed to initialize Eko');
      }
    } catch (error) {
      toast.error('Failed to initialize Eko automation');
      console.error('Eko initialization error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCapabilities = async () => {
    try {
      const response = await fetch('/api/eko/capabilities', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setCapabilities(data);
      }
    } catch (error) {
      console.error('Error fetching capabilities:', error);
    }
  };

  const fetchWorkflowHistory = async () => {
    try {
      const response = await fetch('/api/eko/workflows/history', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setWorkflowHistory(data);
      }
    } catch (error) {
      console.error('Error fetching workflow history:', error);
    }
  };

  const createCustomWorkflow = async (taskDescription, additionalData = {}) => {
    setLoading(true);
    try {
      const response = await fetch('/api/eko/workflow/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          task_description: taskDescription,
          ...additionalData
        })
      });

      if (response.ok) {
        const result = await response.json();
        toast.success('Workflow created successfully!');
        await fetchWorkflowHistory();
        return result;
      } else {
        throw new Error('Failed to create workflow');
      }
    } catch (error) {
      toast.error('Failed to create workflow');
      console.error('Workflow creation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const QuickActionCard = ({ icon: Icon, title, description, action, color = "teal" }) => (
    <motion.div
      whileHover={{ scale: 1.02, y: -2 }}
      className={`bg-white rounded-xl p-6 shadow-sm border border-gray-100 cursor-pointer
        hover:shadow-lg transition-all duration-200`}
      onClick={action}
    >
      <div className={`w-12 h-12 bg-gradient-to-br from-${color}-500 to-${color}-600 
        rounded-xl flex items-center justify-center mb-4`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <h3 className="font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600 mb-3">{description}</p>
      <div className="flex items-center text-teal-600 text-sm font-medium">
        <span>Get Started</span>
        <ChevronRight className="w-4 h-4 ml-1" />
      </div>
    </motion.div>
  );

  const WorkflowStatusBadge = ({ status }) => {
    const statusConfig = {
      completed: { color: 'green', icon: CheckCircle, text: 'Completed' },
      running: { color: 'blue', icon: Activity, text: 'Running' },
      failed: { color: 'red', icon: AlertCircle, text: 'Failed' },
      pending: { color: 'yellow', icon: Clock, text: 'Pending' }
    };

    const config = statusConfig[status] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
        bg-${config.color}-100 text-${config.color}-800`}>
        <Icon className="w-3 h-3 mr-1" />
        {config.text}
      </span>
    );
  };

  const AgentCard = ({ agent }) => (
    <div className="bg-white rounded-lg p-4 border border-gray-100">
      <div className="flex items-center mb-3">
        <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-cyan-600 rounded-lg 
          flex items-center justify-center mr-3">
          <Bot className="w-4 h-4 text-white" />
        </div>
        <div>
          <h4 className="font-medium text-gray-900">{agent.name}</h4>
          <p className="text-xs text-gray-500">{agent.description}</p>
        </div>
      </div>
      <ul className="space-y-1">
        {agent.capabilities.slice(0, 3).map((capability, index) => (
          <li key={index} className="text-xs text-gray-600 flex items-center">
            <CheckCircle className="w-3 h-3 text-teal-500 mr-2 flex-shrink-0" />
            {capability}
          </li>
        ))}
      </ul>
    </div>
  );

  if (!isInitialized) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-teal-50 to-cyan-50 p-6">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-16"
          >
            <div className="w-24 h-24 bg-gradient-to-br from-teal-500 to-cyan-600 
              rounded-full flex items-center justify-center mx-auto mb-8">
              <Sparkles className="w-12 h-12 text-white" />
            </div>
            
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Eko Automation Framework
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Transform your university application process with AI-powered automation. 
              Create complex workflows using simple natural language.
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Brain className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Natural Language</h3>
                <p className="text-sm text-gray-600">
                  Describe what you want automated in plain English
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Globe className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Multi-Platform</h3>
                <p className="text-sm text-gray-600">
                  Works across browsers, desktops, and web applications
                </p>
              </div>
              
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <Zap className="w-8 h-8 text-teal-600 mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Production Ready</h3>
                <p className="text-sm text-gray-600">
                  Enterprise-grade automation with reliability built-in
                </p>
              </div>
            </div>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={initializeEko}
              disabled={loading}
              className="bg-gradient-to-r from-teal-600 to-cyan-600 text-white px-8 py-4 
                rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200
                disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center">
                  <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                  Initializing Eko...
                </div>
              ) : (
                <div className="flex items-center">
                  <Play className="w-5 h-5 mr-2" />
                  Initialize Eko Framework
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
              <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-cyan-600 
                rounded-lg flex items-center justify-center mr-3">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Eko Automation</h1>
                <p className="text-sm text-gray-600">AI-powered workflow automation</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-green-600 bg-green-50 
                px-3 py-1 rounded-full">
                <CheckCircle className="w-4 h-4 mr-1" />
                Framework Active
              </div>
              <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg">
                <Settings className="w-5 h-5" />
              </button>
            </div>
          </div>
          
          {/* Navigation Tabs */}
          <div className="flex space-x-8 mt-6">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'workflows', label: 'Workflows', icon: Bot },
              { id: 'agents', label: 'Agents', icon: Brain },
              { id: 'history', label: 'History', icon: Clock }
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
              {/* Quick Actions */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <QuickActionCard
                    icon={Globe}
                    title="University Application"
                    description="Automate complete university application process"
                    action={() => createCustomWorkflow("Apply to Oxford University Computer Science program")}
                  />
                  <QuickActionCard
                    icon={Monitor}
                    title="Status Monitoring"
                    description="Monitor multiple application statuses"
                    action={() => createCustomWorkflow("Check status of all my university applications")}
                  />
                  <QuickActionCard
                    icon={FileText}
                    title="Document Prep"
                    description="Prepare and format application documents"
                    action={() => createCustomWorkflow("Prepare all required documents for university applications")}
                  />
                  <QuickActionCard
                    icon={Brain}
                    title="Custom Workflow"
                    description="Create workflow with natural language"
                    action={() => {
                      const task = prompt("Describe what you want to automate:");
                      if (task) createCustomWorkflow(task);
                    }}
                  />
                </div>
              </div>

              {/* Active Workflows */}
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Active Workflows</h2>
                <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                  {activeWorkflows.length > 0 ? (
                    <div className="divide-y divide-gray-200">
                      {activeWorkflows.map((workflow, index) => (
                        <div key={index} className="p-4 flex items-center justify-between">
                          <div className="flex items-center">
                            <Activity className="w-5 h-5 text-teal-600 mr-3" />
                            <div>
                              <h3 className="font-medium text-gray-900">{workflow.description}</h3>
                              <p className="text-sm text-gray-500">Started {workflow.started}</p>
                            </div>
                          </div>
                          <div className="flex items-center space-x-3">
                            <div className="w-32 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-teal-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${workflow.progress}%` }}
                              />
                            </div>
                            <span className="text-sm text-gray-600">{workflow.progress}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-8 text-center text-gray-500">
                      <Bot className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      <p>No active workflows</p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}

          {selectedTab === 'agents' && capabilities && (
            <motion.div
              key="agents"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Available Agents</h2>
                <div className="grid md:grid-cols-2 gap-4">
                  {capabilities.agents.map((agent, index) => (
                    <AgentCard key={index} agent={agent} />
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {selectedTab === 'history' && (
            <motion.div
              key="history"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Workflow History</h2>
                <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
                  {workflowHistory.length > 0 ? (
                    <div className="divide-y divide-gray-200">
                      {workflowHistory.map((workflow, index) => (
                        <div key={index} className="p-4">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-medium text-gray-900">{workflow.description}</h3>
                            <WorkflowStatusBadge status={workflow.status} />
                          </div>
                          <div className="flex items-center text-sm text-gray-500 space-x-4">
                            <span>Type: {workflow.type}</span>
                            <span>Duration: {Math.floor(workflow.execution_time / 60)}m</span>
                            <span>{new Date(workflow.created_at).toLocaleDateString()}</span>
                          </div>
                          {workflow.result && (
                            <p className="text-sm text-gray-600 mt-2">{workflow.result}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-8 text-center text-gray-500">
                      <Clock className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      <p>No workflow history</p>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default EkoAutomationPanel; 