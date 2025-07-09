"use client"

import { useState, useEffect } from "react"
import {
  FileText,
  Zap,
  Activity,
  TrendingUp,
  ArrowRight,
  Play,
  Pause,
  RefreshCw,
  Plus,
  Brain,
  Sparkles,
  Cpu,
  Database,
  BarChart3,
  Target,
  Workflow,
} from "lucide-react"
import EkoAutomationPanel from "../automation/EkoAutomationPanel"
import EnhancedEkoPanel from "../automation/EnhancedEkoPanel"

const ModernDashboard = () => {
  const [currentView, setCurrentView] = useState("dashboard")
  const [metrics, setMetrics] = useState({
    totalApplications: 47,
    completedApplications: 12,
    pendingApplications: 23,
    activeAutomations: 8,
    automationSuccess: 94.5,
    documentsProcessed: 156,
  })
  const [isLoading, setIsLoading] = useState(true)
  const [automationStatus, setAutomationStatus] = useState("active")

  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true)
      await new Promise((resolve) => setTimeout(resolve, 1000))

      setMetrics({
        totalApplications: 142,
        completedApplications: 38,
        pendingApplications: 12,
        activeAutomations: 8,
        automationSuccess: 94.5,
        documentsProcessed: 156,
      })
      setIsLoading(false)
    }

    fetchDashboardData()
  }, [])

  const recentApplications = [
    {
      id: 1,
      client: "Sarah Chen",
      university: "Oxford University",
      status: "submitted",
      submittedAt: "2 hours ago",
      progress: 100,
      aiScore: 98,
    },
    {
      id: 2,
      client: "James Wilson",
      university: "Cambridge University",
      status: "processing",
      submittedAt: "4 hours ago",
      progress: 75,
      aiScore: 92,
    },
    {
      id: 3,
      client: "Priya Patel",
      university: "Imperial College",
      status: "accepted",
      submittedAt: "1 day ago",
      progress: 100,
      aiScore: 96,
    },
    {
      id: 4,
      client: "Mohammed Al-Ahmad",
      university: "UCL",
      status: "submitted",
      submittedAt: "1 day ago",
      progress: 100,
      aiScore: 94,
    },
  ]

  const aiTasks = [
    {
      id: 1,
      task: "Neural Processing: Personal Statement Analysis",
      progress: 85,
      client: "Sarah Chen",
      estimatedCompletion: "15 min",
      type: "analysis",
      priority: "high",
    },
    {
      id: 2,
      task: "Document Intelligence: Verification & Parsing",
      progress: 60,
      client: "James Wilson",
      estimatedCompletion: "30 min",
      type: "processing",
      priority: "medium",
    },
    {
      id: 3,
      task: "Auto-Fill Engine: Form Completion",
      progress: 95,
      client: "Lisa Zhang",
      estimatedCompletion: "5 min",
      type: "automation",
      priority: "high",
    },
  ]

  const getStatusColor = (status) => {
    switch (status) {
      case "submitted":
        return "bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-400 border-blue-500/30"
      case "processing":
        return "bg-gradient-to-r from-yellow-500/20 to-orange-500/20 text-yellow-400 border-yellow-500/30"
      case "accepted":
        return "bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-400 border-green-500/30"
      case "rejected":
        return "bg-gradient-to-r from-red-500/20 to-pink-500/20 text-red-400 border-red-500/30"
      default:
        return "bg-gradient-to-r from-gray-500/20 to-slate-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case "high":
        return "bg-red-500/20 text-red-400"
      case "medium":
        return "bg-yellow-500/20 text-yellow-400"
      case "low":
        return "bg-green-500/20 text-green-400"
      default:
        return "bg-gray-500/20 text-gray-400"
    }
  }

  const quickActions = [
    {
      title: "New Application",
      description: "AI-powered application creation",
      icon: Plus,
      gradient: "from-blue-500 to-cyan-500",
      action: () => console.log("New application"),
    },
    {
      title: "Neural Automation",
      description: "Advanced AI workflow engine",
      icon: Brain,
      gradient: "from-purple-500 to-pink-500",
      action: () => setCurrentView("eko-automation"),
    },
    {
      title: "Multi-Agent System",
      description: "Parallel processing network",
      icon: Workflow,
      gradient: "from-emerald-500 to-teal-500",
      action: () => setCurrentView("enhanced-eko"),
    },
    {
      title: "Intelligence Hub",
      description: "Real-time analytics & insights",
      icon: BarChart3,
      gradient: "from-orange-500 to-red-500",
      action: () => console.log("Analytics"),
    },
  ]

  if (currentView === "eko-automation") {
    return <EkoAutomationPanel onBack={() => setCurrentView("dashboard")} />
  }

  if (currentView === "enhanced-eko") {
    return <EnhancedEkoPanel onBack={() => setCurrentView("dashboard")} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      <div className="relative z-10">
        {/* Header Section */}
        <div className="flex items-center justify-between mb-8">
          <div className="space-y-2">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/25">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-white via-cyan-200 to-blue-200 bg-clip-text text-transparent">
                  Neural Command Center
                </h1>
                <p className="text-slate-400 text-lg">AI-Powered University Application Intelligence</p>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* AI Status */}
            <div className="flex items-center space-x-3 px-6 py-3 bg-gradient-to-r from-slate-800/50 to-slate-700/50 backdrop-blur-xl rounded-2xl border border-slate-600/30">
              <div className="relative">
                <Cpu className="w-5 h-5 text-cyan-400" />
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              </div>
              <div>
                <div className="text-sm font-semibold text-cyan-400">Neural Network</div>
                <div className="text-xs text-slate-400">Active • 8 Agents</div>
              </div>
            </div>

            {/* Control Buttons */}
            <button
              className={`flex items-center space-x-2 px-6 py-3 rounded-2xl font-semibold transition-all duration-300 backdrop-blur-xl border ${
                automationStatus === "active"
                  ? "bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-400 border-green-500/30 hover:from-green-500/30 hover:to-emerald-500/30"
                  : "bg-gradient-to-r from-slate-800/50 to-slate-700/50 text-slate-400 border-slate-600/30 hover:border-slate-500/50"
              }`}
              onClick={() => setAutomationStatus(automationStatus === "active" ? "paused" : "active")}
            >
              {automationStatus === "active" ? (
                <>
                  <Pause className="w-4 h-4" />
                  <span>Pause Neural Net</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  <span>Activate Neural Net</span>
                </>
              )}
            </button>

            <button className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-400 rounded-2xl hover:from-blue-500/30 hover:to-cyan-500/30 transition-all duration-300 backdrop-blur-xl border border-blue-500/30">
              <RefreshCw className="w-4 h-4" />
              <span>Sync Data</span>
            </button>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 hover:border-cyan-500/50 transition-all duration-300 group">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <FileText className="w-6 h-6 text-cyan-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-white">{metrics.totalApplications}</div>
                <div className="text-xs text-green-400 flex items-center">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  +12%
                </div>
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-slate-300 font-medium">Total Applications</div>
              <div className="text-xs text-slate-400">Neural processing pipeline</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 hover:border-purple-500/50 transition-all duration-300 group">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Brain className="w-6 h-6 text-purple-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-white">{metrics.activeAutomations}</div>
                <div className="text-xs text-green-400 flex items-center">
                  <Activity className="w-3 h-3 mr-1" />
                  Live
                </div>
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-slate-300 font-medium">AI Agents Active</div>
              <div className="text-xs text-slate-400">Autonomous processing units</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 hover:border-emerald-500/50 transition-all duration-300 group">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-emerald-500/20 to-teal-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Target className="w-6 h-6 text-emerald-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-white">{metrics.automationSuccess}%</div>
                <div className="text-xs text-green-400 flex items-center">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  +2.3%
                </div>
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-slate-300 font-medium">Success Rate</div>
              <div className="text-xs text-slate-400">Neural accuracy metrics</div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30 hover:border-orange-500/50 transition-all duration-300 group">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-gradient-to-r from-orange-500/20 to-red-500/20 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Database className="w-6 h-6 text-orange-400" />
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-white">{metrics.documentsProcessed}</div>
                <div className="text-xs text-green-400 flex items-center">
                  <Activity className="w-3 h-3 mr-1" />
                  +45
                </div>
              </div>
            </div>
            <div className="space-y-1">
              <div className="text-slate-300 font-medium">Documents Processed</div>
              <div className="text-xs text-slate-400">Intelligence extraction</div>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Recent Applications */}
          <div className="lg:col-span-2 bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 rounded-lg flex items-center justify-center">
                  <Activity className="w-4 h-4 text-blue-400" />
                </div>
                <h2 className="text-xl font-bold text-white">Neural Processing Queue</h2>
              </div>
              <button className="text-cyan-400 hover:text-cyan-300 text-sm font-medium flex items-center space-x-1 px-3 py-1 rounded-lg hover:bg-cyan-500/10 transition-all">
                <span>View All</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4">
              {recentApplications.map((app) => (
                <div
                  key={app.id}
                  className="group p-4 bg-gradient-to-r from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/20 hover:border-cyan-500/30 transition-all duration-300"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="relative">
                        <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                          <span className="text-white text-sm font-bold">
                            {app.client
                              .split(" ")
                              .map((n) => n[0])
                              .join("")}
                          </span>
                        </div>
                        <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center">
                          <span className="text-xs font-bold text-white">{app.aiScore}</span>
                        </div>
                      </div>
                      <div>
                        <p className="font-semibold text-white">{app.client}</p>
                        <p className="text-sm text-slate-300">{app.university}</p>
                        <div className="flex items-center space-x-2 mt-1">
                          <div className="w-16 bg-slate-600 rounded-full h-1">
                            <div
                              className="bg-gradient-to-r from-cyan-500 to-blue-500 h-1 rounded-full transition-all duration-500"
                              style={{ width: `${app.progress}%` }}
                            />
                          </div>
                          <span className="text-xs text-slate-400">{app.progress}%</span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right space-y-2">
                      <span
                        className={`inline-block px-3 py-1 rounded-full text-xs font-semibold border ${getStatusColor(app.status)}`}
                      >
                        {app.status.toUpperCase()}
                      </span>
                      <p className="text-xs text-slate-400">{app.submittedAt}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Task Monitor */}
          <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-lg flex items-center justify-center">
                  <Cpu className="w-4 h-4 text-purple-400" />
                </div>
                <h2 className="text-xl font-bold text-white">Neural Tasks</h2>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-400 font-medium">Processing</span>
              </div>
            </div>

            <div className="space-y-4">
              {aiTasks.map((task) => (
                <div
                  key={task.id}
                  className="space-y-3 p-4 bg-gradient-to-r from-slate-700/20 to-slate-600/10 rounded-xl border border-slate-600/20"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center space-x-2">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}
                        >
                          {task.priority.toUpperCase()}
                        </span>
                        <span className="text-xs text-slate-400">{task.estimatedCompletion}</span>
                      </div>
                      <p className="text-sm font-medium text-white leading-relaxed">{task.task}</p>
                      <p className="text-xs text-cyan-400">Agent: {task.client}</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Neural Progress</span>
                      <span className="font-medium text-white">{task.progress}%</span>
                    </div>
                    <div className="w-full bg-slate-600 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500 relative overflow-hidden"
                        style={{ width: `${task.progress}%` }}
                      >
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full mt-4 py-3 text-sm text-purple-400 hover:text-purple-300 font-medium border border-purple-500/30 rounded-xl hover:bg-purple-500/10 transition-all duration-300">
              Access Neural Network
            </button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gradient-to-br from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl p-6 border border-slate-600/30">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-8 h-8 bg-gradient-to-r from-cyan-500/20 to-blue-500/20 rounded-lg flex items-center justify-center">
              <Zap className="w-4 h-4 text-cyan-400" />
            </div>
            <h2 className="text-xl font-bold text-white">Neural Command Interface</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <button
                key={index}
                className="group relative overflow-hidden p-6 bg-gradient-to-br from-slate-700/30 to-slate-600/20 rounded-xl border border-slate-600/30 hover:border-slate-500/50 transition-all duration-300 hover:scale-105"
                onClick={action.action}
              >
                <div className="relative z-10">
                  <div
                    className={`w-12 h-12 bg-gradient-to-r ${action.gradient} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg`}
                  >
                    <action.icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="text-left">
                    <p className="font-bold text-white mb-1">{action.title}</p>
                    <p className="text-sm text-slate-400">{action.description}</p>
                  </div>
                </div>
                <div
                  className={`absolute inset-0 bg-gradient-to-r ${action.gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}
                ></div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ModernDashboard
