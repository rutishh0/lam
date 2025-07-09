import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const MetricCard = ({ 
  title, 
  value, 
  previousValue, 
  icon: Icon, 
  trend = 'neutral', 
  trendValue, 
  description,
  color = 'blue',
  isLoading = false 
}) => {
  const colorClasses = {
    blue: {
      bg: 'from-blue-500 to-cyan-500',
      iconBg: 'bg-blue-100',
      iconColor: 'text-blue-600',
      trend: 'text-blue-600'
    },
    purple: {
      bg: 'from-purple-500 to-pink-500',
      iconBg: 'bg-purple-100',
      iconColor: 'text-purple-600',
      trend: 'text-purple-600'
    },
    green: {
      bg: 'from-green-500 to-emerald-500',
      iconBg: 'bg-green-100',
      iconColor: 'text-green-600',
      trend: 'text-green-600'
    },
    orange: {
      bg: 'from-orange-500 to-yellow-500',
      iconBg: 'bg-orange-100',
      iconColor: 'text-orange-600',
      trend: 'text-orange-600'
    },
    red: {
      bg: 'from-red-500 to-pink-500',
      iconBg: 'bg-red-100',
      iconColor: 'text-red-600',
      trend: 'text-red-600'
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4" />;
      case 'down':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-green-600 bg-green-50';
      case 'down':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 animate-pulse">
        <div className="flex items-center justify-between mb-4">
          <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
          <div className="w-16 h-6 bg-gray-200 rounded"></div>
        </div>
        <div className="w-24 h-8 bg-gray-200 rounded mb-2"></div>
        <div className="w-32 h-4 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 group">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 ${colorClasses[color].iconBg} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200`}>
          <Icon className={`w-6 h-6 ${colorClasses[color].iconColor}`} />
        </div>
        
        {trendValue && (
          <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-sm font-medium ${getTrendColor()}`}>
            {getTrendIcon()}
            <span>{trendValue}</span>
          </div>
        )}
      </div>

      {/* Value */}
      <div className="space-y-1">
        <h3 className="text-2xl font-bold text-gray-900 group-hover:text-gray-700 transition-colors">
          {value}
        </h3>
        <p className="text-sm text-gray-600">{title}</p>
        {description && (
          <p className="text-xs text-gray-500 mt-2">{description}</p>
        )}
      </div>

      {/* Progress Bar (if showing trend) */}
      {previousValue && (
        <div className="mt-4">
          <div className="w-full bg-gray-100 rounded-full h-1.5">
            <div 
              className={`h-1.5 rounded-full bg-gradient-to-r ${colorClasses[color].bg} transition-all duration-1000 ease-out`}
              style={{ 
                width: `${Math.min(100, (value / previousValue) * 100)}%` 
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default MetricCard; 