"use client"

import { useState } from "react"
import {
  Search,
  Bell,
  Settings,
  User,
  HelpCircle,
  LogOut,
  ChevronDown,
  Sparkles,
  Cpu,
  Brain,
  Shield,
} from "lucide-react"

const Header = ({ user, onLogout }) => {
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")

  const notifications = [
    {
      id: 1,
      type: "success",
      title: "Neural Processing Complete",
      message: "Oxford University application successfully processed by AI Agent #7",
      time: "2 minutes ago",
      unread: true,
    },
    {
      id: 2,
      type: "info",
      title: "Intelligence Analysis Ready",
      message: "Document parsing completed for client Sarah Chen - 98% accuracy",
      time: "5 minutes ago",
      unread: true,
    },
    {
      id: 3,
      type: "warning",
      title: "Neural Network Update",
      message: "System optimization scheduled in 2 hours - Enhanced AI capabilities",
      time: "1 hour ago",
      unread: false,
    },
  ]

  const unreadCount = notifications.filter((n) => n.unread).length

  const getNotificationIcon = (type) => {
    switch (type) {
      case "success":
        return <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full animate-pulse" />
      case "warning":
        return <div className="w-3 h-3 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full animate-pulse" />
      case "info":
        return <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-cyan-500 rounded-full animate-pulse" />
      default:
        return <div className="w-3 h-3 bg-gradient-to-r from-gray-400 to-slate-500 rounded-full" />
    }
  }

  return (
    <header className="bg-gradient-to-r from-slate-900/95 via-slate-800/95 to-slate-900/95 backdrop-blur-xl border-b border-slate-700/50 px-6 py-4">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-32 h-32 bg-cyan-500/5 rounded-full blur-3xl"></div>
        <div className="absolute top-0 right-1/4 w-32 h-32 bg-purple-500/5 rounded-full blur-3xl"></div>
      </div>

      <div className="relative flex items-center justify-between">
        {/* Search Bar */}
        <div className="flex-1 max-w-2xl">
          <div className="relative">
            <div className="absolute left-4 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
              <Search className="text-slate-400 w-5 h-5" />
              <div className="w-px h-5 bg-slate-600"></div>
            </div>
            <input
              type="text"
              placeholder="Search neural networks, applications, or intelligence data..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-16 pr-6 py-4 bg-gradient-to-r from-slate-800/50 to-slate-700/30 backdrop-blur-xl border border-slate-600/30 rounded-2xl focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 text-white placeholder-slate-400 transition-all duration-300"
            />
            {searchQuery && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-gradient-to-br from-slate-800/95 to-slate-700/95 backdrop-blur-xl border border-slate-600/50 rounded-2xl shadow-2xl z-50 p-4">
                <div className="text-sm text-slate-400 mb-2">Neural search results for "{searchQuery}"...</div>
                <div className="space-y-2">
                  <div className="p-3 bg-slate-700/30 rounded-xl hover:bg-slate-600/30 transition-colors cursor-pointer">
                    <div className="text-white font-medium">AI Agent Processing</div>
                    <div className="text-xs text-slate-400">Neural network automation</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-4">
          {/* System Status */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-slate-800/50 to-slate-700/30 backdrop-blur-xl rounded-2xl border border-slate-600/30">
              <div className="relative">
                <Cpu className="w-5 h-5 text-cyan-400" />
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              </div>
              <div className="text-sm">
                <div className="text-cyan-400 font-semibold">Neural Core</div>
                <div className="text-xs text-slate-400">Online</div>
              </div>
            </div>

            <div className="flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-purple-500/10 to-pink-500/10 backdrop-blur-xl rounded-2xl border border-purple-500/30">
              <div className="relative">
                <Brain className="w-5 h-5 text-purple-400" />
                <Sparkles className="absolute -top-1 -right-1 w-3 h-3 text-yellow-400 animate-pulse" />
              </div>
              <div className="text-sm">
                <div className="text-purple-400 font-semibold">AI Active</div>
                <div className="text-xs text-slate-400">8 Agents</div>
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => {
                setShowNotifications(!showNotifications)
                setShowUserMenu(false)
              }}
              className="relative p-3 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-2xl transition-all duration-300 border border-slate-600/30 hover:border-slate-500/50"
            >
              <Bell className="w-6 h-6" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 w-6 h-6 bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs rounded-full flex items-center justify-center font-bold shadow-lg">
                  {unreadCount}
                </span>
              )}
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-96 bg-gradient-to-br from-slate-800/95 to-slate-700/95 backdrop-blur-xl border border-slate-600/50 rounded-2xl shadow-2xl z-50">
                <div className="p-6 border-b border-slate-600/50">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-white">Neural Alerts</h3>
                    {unreadCount > 0 && (
                      <span className="px-3 py-1 bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-xs font-bold rounded-full">
                        {unreadCount} new
                      </span>
                    )}
                  </div>
                </div>
                <div className="max-h-80 overflow-y-auto">
                  {notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`p-4 border-b border-slate-600/30 hover:bg-slate-700/30 transition-colors ${
                        notification.unread ? "bg-cyan-500/5" : ""
                      }`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className="mt-2">{getNotificationIcon(notification.type)}</div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-white">{notification.title}</p>
                          <p className="text-sm text-slate-300 mt-1 leading-relaxed">{notification.message}</p>
                          <p className="text-xs text-slate-400 mt-2">{notification.time}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="p-4 border-t border-slate-600/50">
                  <button className="text-sm text-cyan-400 hover:text-cyan-300 font-semibold transition-colors">
                    Access Neural Command Center
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => {
                setShowUserMenu(!showUserMenu)
                setShowNotifications(false)
              }}
              className="flex items-center space-x-3 p-3 text-slate-300 hover:text-white hover:bg-slate-700/50 rounded-2xl transition-all duration-300 border border-slate-600/30 hover:border-slate-500/50"
            >
              <div className="relative">
                <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg">
                  <span className="text-sm font-bold text-white">{user?.name?.charAt(0)?.toUpperCase() || "U"}</span>
                </div>
                <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-slate-800"></div>
              </div>
              <div className="hidden md:block text-left">
                <p className="text-sm font-semibold text-white">{user?.name || "Neural User"}</p>
                <p className="text-xs text-slate-400">{user?.role || "Agent"} • Active</p>
              </div>
              <ChevronDown className="w-4 h-4 text-slate-400" />
            </button>

            {/* User Dropdown */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-64 bg-gradient-to-br from-slate-800/95 to-slate-700/95 backdrop-blur-xl border border-slate-600/50 rounded-2xl shadow-2xl z-50">
                <div className="p-6 border-b border-slate-600/50">
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <div className="w-12 h-12 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg">
                        <span className="text-lg font-bold text-white">
                          {user?.name?.charAt(0)?.toUpperCase() || "U"}
                        </span>
                      </div>
                      <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-slate-800"></div>
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-white">{user?.name || "Neural User"}</p>
                      <p className="text-xs text-slate-400">{user?.email || "user@neural.ai"}</p>
                      <div className="flex items-center space-x-1 mt-1">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span className="text-xs text-green-400">Active Session</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="py-2">
                  <button className="w-full flex items-center space-x-3 px-6 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors">
                    <User className="w-4 h-4 text-slate-400" />
                    <span>Neural Profile</span>
                  </button>
                  <button className="w-full flex items-center space-x-3 px-6 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors">
                    <Settings className="w-4 h-4 text-slate-400" />
                    <span>System Preferences</span>
                  </button>
                  <button className="w-full flex items-center space-x-3 px-6 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors">
                    <Shield className="w-4 h-4 text-slate-400" />
                    <span>Security Center</span>
                  </button>
                  <button className="w-full flex items-center space-x-3 px-6 py-3 text-sm text-slate-300 hover:text-white hover:bg-slate-700/50 transition-colors">
                    <HelpCircle className="w-4 h-4 text-slate-400" />
                    <span>Neural Support</span>
                  </button>
                </div>

                <div className="py-2 border-t border-slate-600/50">
                  <button
                    onClick={onLogout}
                    className="w-full flex items-center space-x-3 px-6 py-3 text-sm text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Disconnect Session</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
