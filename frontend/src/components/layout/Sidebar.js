import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Bot,
  LayoutDashboard,
  Users,
  FileText,
  Settings,
  BarChart3,
  Zap,
  Shield,
  Bell,
  HelpCircle,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Activity
} from 'lucide-react';

const Sidebar = ({ isCollapsed, setIsCollapsed, onLogout }) => {
  const location = useLocation();
  
  const navigationItems = [
    {
      label: 'Dashboard',
      icon: LayoutDashboard,
      path: '/dashboard',
      description: 'Overview & analytics'
    },
    {
      label: 'Automation',
      icon: Zap,
      path: '/automation',
      description: 'AI-powered tasks',
      badge: 'AI'
    },
    {
      label: 'Applications',
      icon: FileText,
      path: '/applications',
      description: 'Application status'
    },
    {
      label: 'Clients',
      icon: Users,
      path: '/clients',
      description: 'Client management'
    },
    {
      label: 'Analytics',
      icon: BarChart3,
      path: '/analytics',
      description: 'Performance insights'
    },
    {
      label: 'Monitor',
      icon: Activity,
      path: '/monitor',
      description: 'System health',
      badge: 'Live'
    }
  ];

  const secondaryItems = [
    {
      label: 'Settings',
      icon: Settings,
      path: '/settings',
      description: 'App configuration'
    },
    {
      label: 'Admin',
      icon: Shield,
      path: '/admin',
      description: 'Admin panel',
      adminOnly: true
    },
    {
      label: 'Help',
      icon: HelpCircle,
      path: '/help',
      description: 'Support & docs'
    }
  ];

  const isActiveRoute = (path) => {
    return location.pathname === path || 
           (path !== '/dashboard' && location.pathname.startsWith(path));
  };

  const NavItem = ({ item, isActive }) => (
    <Link
      to={item.path}
      className={`
        group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-200
        ${isActive 
          ? 'bg-gradient-to-r from-blue-500/10 to-purple-500/10 text-blue-600 shadow-sm' 
          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
        }
        ${isCollapsed ? 'justify-center' : ''}
      `}
    >
      <div className={`
        relative flex items-center justify-center w-5 h-5
        ${isActive ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600'}
      `}>
        <item.icon className="w-5 h-5" />
        {item.badge && !isCollapsed && (
          <span className={`
            absolute -top-1 -right-1 px-1 py-0.5 text-xs font-medium rounded-full
            ${item.badge === 'AI' ? 'bg-purple-100 text-purple-600' : 'bg-green-100 text-green-600'}
          `}>
            {item.badge}
          </span>
        )}
      </div>
      
      {!isCollapsed && (
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <span className="truncate">{item.label}</span>
            {item.badge && (
              <span className={`
                px-1.5 py-0.5 text-xs font-medium rounded-full
                ${item.badge === 'AI' ? 'bg-purple-100 text-purple-600' : 'bg-green-100 text-green-600'}
              `}>
                {item.badge}
              </span>
            )}
          </div>
          <p className="text-xs text-gray-400 truncate mt-0.5">
            {item.description}
          </p>
        </div>
      )}

      {/* Active indicator */}
      {isActive && (
        <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1 h-6 bg-gradient-to-b from-blue-500 to-purple-500 rounded-r-full" />
      )}

      {/* Tooltip for collapsed sidebar */}
      {isCollapsed && (
        <div className="absolute left-14 bg-gray-900 text-white text-sm rounded-lg px-2 py-1 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 whitespace-nowrap">
          {item.label}
          <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 border-4 border-transparent border-r-gray-900" />
        </div>
      )}
    </Link>
  );

  return (
    <div className={`
      relative bg-white border-r border-gray-200 transition-all duration-300 ease-in-out z-40
      ${isCollapsed ? 'w-16' : 'w-64'}
    `}>
      {/* Header */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <Link to="/dashboard" className={`flex items-center space-x-3 ${isCollapsed ? 'justify-center' : ''}`}>
            <div className="relative">
              <div className="w-8 h-8 bg-gradient-to-r from-teal-600 to-cyan-600 rounded-lg flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <Sparkles className="absolute -top-1 -right-1 w-3 h-3 text-yellow-500" />
            </div>
            {!isCollapsed && (
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent">
                  Elevate Ed
                </h1>
                <p className="text-xs text-gray-500">University Applications</p>
              </div>
            )}
          </Link>
          
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {isCollapsed ? (
              <ChevronRight className="w-4 h-4 text-gray-400" />
            ) : (
              <ChevronLeft className="w-4 h-4 text-gray-400" />
            )}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 p-4 space-y-8">
        {/* Main Navigation */}
        <div className="space-y-1">
          {!isCollapsed && (
            <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
              Main
            </h2>
          )}
          {navigationItems.map((item) => (
            <NavItem
              key={item.path}
              item={item}
              isActive={isActiveRoute(item.path)}
            />
          ))}
        </div>

        {/* Secondary Navigation */}
        <div className="space-y-1">
          {!isCollapsed && (
            <h2 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
              System
            </h2>
          )}
          {secondaryItems.map((item) => (
            <NavItem
              key={item.path}
              item={item}
              isActive={isActiveRoute(item.path)}
            />
          ))}
        </div>
      </div>

      {/* User Section */}
      <div className="p-4 border-t border-gray-100">
        <div className={`flex items-center ${isCollapsed ? 'justify-center' : 'space-x-3'}`}>
          <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium text-white">U</span>
          </div>
          {!isCollapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">User</p>
              <p className="text-xs text-gray-500 truncate">Active Session</p>
            </div>
          )}
        </div>
        
        {!isCollapsed && (
          <button
            onClick={onLogout}
            className="mt-3 w-full flex items-center justify-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default Sidebar; 