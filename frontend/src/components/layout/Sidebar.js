"use client"
import { Link, useLocation } from "react-router-dom"
import {
  Bot,
  LayoutDashboard,
  Users,
  FileText,
  Settings,
  BarChart3,
  Shield,
  HelpCircle,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Activity,
  Brain,
} from "lucide-react"

const Sidebar = ({ isCollapsed, setIsCollapsed, onLogout }) => {
  const location = useLocation()

  const navigationItems = [
    {
      label: "Neural Hub",
      icon: LayoutDashboard,
      path: "/dashboard",
      description: "Command center",
      gradient: "from-cyan-500 to-blue-500",
    },
    {
      label: "AI Automation",
      icon: Brain,
      path: "/automation",
      description: "Neural networks",
      badge: "AI",
      gradient: "from-purple-500 to-pink-500",
    },
    {
      label: "Applications",
      icon: FileText,
      path: "/applications",
      description: "Processing queue",
      gradient: "from-blue-500 to-indigo-500",
    },
    {
      label: "Clients",
      icon: Users,
      path: "/clients",
      description: "User profiles",
      gradient: "from-emerald-500 to-teal-500",
    },
    {
      label: "Intelligence",
      icon: BarChart3,
      path: "/analytics",
      description: "Data insights",
      gradient: "from-orange-500 to-red-500",
    },
    {
      label: "System Monitor",
      icon: Activity,
      path: "/monitor",
      description: "Live metrics",
      badge: "Live",
      gradient: "from-green-500 to-emerald-500",
    },
  ]

  const secondaryItems = [
    {
      label: "Configuration",
      icon: Settings,
      path: "/settings",
      description: "System config",
      gradient: "from-gray-500 to-slate-500",
    },
    {
      label: "Admin Core",
      icon: Shield,
      path: "/admin",
      description: "Control panel",
      adminOnly: true,
      gradient: "from-red-500 to-pink-500",
    },
    {
      label: "Neural Docs",
      icon: HelpCircle,
      path: "/help",
      description: "Knowledge base",
      gradient: "from-indigo-500 to-purple-500",
    },
  ]

  const isActiveRoute = (path) => {
    return location.pathname === path || (path !== "/dashboard" && location.pathname.startsWith(path))
  }

  const NavItem = ({ item, isActive }) => (
    <Link
      to={item.path}
      className={`
        group relative flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition-all duration-300
        ${
          isActive
            ? "bg-gradient-to-r from-slate-700/50 to-slate-600/30 text-white shadow-lg border border-slate-500/30"
            : "text-slate-400 hover:text-white hover:bg-gradient-to-r hover:from-slate-700/30 hover:to-slate-600/20"
        }
        ${isCollapsed ? "justify-center" : ""}
      `}
    >
      <div
        className={`
        relative flex items-center justify-center w-6 h-6 transition-all duration-300
        ${isActive ? "scale-110" : "group-hover:scale-105"}
      `}
      >
        <div
          className={`absolute inset-0 bg-gradient-to-r ${item.gradient} rounded-lg opacity-20 ${isActive ? "opacity-30" : "group-hover:opacity-25"}`}
        ></div>
        <item.icon
          className={`w-5 h-5 relative z-10 ${isActive ? "text-white" : "text-slate-400 group-hover:text-white"}`}
        />
        {item.badge && !isCollapsed && (
          <span
            className={`
            absolute -top-2 -right-2 px-1.5 py-0.5 text-xs font-bold rounded-full
            ${item.badge === "AI" ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white" : "bg-gradient-to-r from-green-500 to-emerald-500 text-white"}
          `}
          >
            {item.badge}
          </span>
        )}
      </div>

      {!isCollapsed && (
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <span className="truncate font-semibold">{item.label}</span>
            {item.badge && (
              <span
                className={`
                px-2 py-0.5 text-xs font-bold rounded-full
                ${item.badge === "AI" ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white" : "bg-gradient-to-r from-green-500 to-emerald-500 text-white"}
              `}
              >
                {item.badge}
              </span>
            )}
          </div>
          <p className="text-xs text-slate-500 truncate mt-0.5">{item.description}</p>
        </div>
      )}

      {/* Active indicator */}
      {isActive && (
        <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-cyan-500 to-blue-500 rounded-r-full shadow-lg shadow-cyan-500/50" />
      )}

      {/* Tooltip for collapsed sidebar */}
      {isCollapsed && (
        <div className="absolute left-16 bg-gradient-to-r from-slate-800 to-slate-700 text-white text-sm rounded-xl px-3 py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 whitespace-nowrap border border-slate-600/50 shadow-xl">
          <div className="font-semibold">{item.label}</div>
          <div className="text-xs text-slate-300">{item.description}</div>
          <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-2 border-4 border-transparent border-r-slate-700" />
        </div>
      )}
    </Link>
  )

  return (
    <div
      className={`
      relative bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 border-r border-slate-700/50 transition-all duration-300 ease-in-out z-40 backdrop-blur-xl
      ${isCollapsed ? "w-20" : "w-72"}
    `}
    >
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-cyan-500/5 to-transparent"></div>
        <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-purple-500/5 to-transparent"></div>
      </div>

      {/* Header */}
      <div className="relative p-6 border-b border-slate-700/50">
        <div className="flex items-center justify-between">
          <Link to="/dashboard" className={`flex items-center space-x-3 ${isCollapsed ? "justify-center" : ""}`}>
            <div className="relative">
              <div className="w-10 h-10 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/25">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <Sparkles className="absolute -top-1 -right-1 w-4 h-4 text-yellow-400 animate-pulse" />
            </div>
            {!isCollapsed && (
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-white via-cyan-200 to-blue-200 bg-clip-text text-transparent">
                  Elevate Ed
                </h1>
                <p className="text-xs text-slate-400">Neural Intelligence Platform</p>
              </div>
            )}
          </Link>

          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-2 rounded-xl hover:bg-slate-700/50 transition-all duration-300 border border-slate-600/30 hover:border-slate-500/50"
          >
            {isCollapsed ? (
              <ChevronRight className="w-4 h-4 text-slate-400" />
            ) : (
              <ChevronLeft className="w-4 h-4 text-slate-400" />
            )}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <div className="relative flex-1 p-4 space-y-8">
        {/* Main Navigation */}
        <div className="space-y-2">
          {!isCollapsed && (
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 px-2">Neural Interface</h2>
          )}
          {navigationItems.map((item) => (
            <NavItem key={item.path} item={item} isActive={isActiveRoute(item.path)} />
          ))}
        </div>

        {/* Secondary Navigation */}
        <div className="space-y-2">
          {!isCollapsed && (
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-4 px-2">System Core</h2>
          )}
          {secondaryItems.map((item) => (
            <NavItem key={item.path} item={item} isActive={isActiveRoute(item.path)} />
          ))}
        </div>
      </div>

      {/* User Section */}
      <div className="relative p-4 border-t border-slate-700/50">
        <div className={`flex items-center ${isCollapsed ? "justify-center" : "space-x-3"} mb-4`}>
          <div className="relative">
            <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-lg">
              <span className="text-sm font-bold text-white">U</span>
            </div>
            <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-slate-800"></div>
          </div>
          {!isCollapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-white truncate">Neural User</p>
              <p className="text-xs text-slate-400 truncate">Active Session</p>
            </div>
          )}
        </div>

        {!isCollapsed && (
          <button
            onClick={onLogout}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 text-sm text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-2xl transition-all duration-300 border border-slate-600/30 hover:border-red-500/30"
          >
            <LogOut className="w-4 h-4" />
            <span>Disconnect</span>
          </button>
        )}
      </div>
    </div>
  )
}

export default Sidebar
