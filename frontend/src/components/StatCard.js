import React from 'react';

const StatCard = ({ 
  title, 
  value, 
  change, 
  changeType, 
  icon: Icon, 
  color = 'blue',
  size = 'default'
}) => {
  const getColorClasses = (color) => {
    const colors = {
      blue: 'text-blue-600 bg-blue-50',
      green: 'text-green-600 bg-green-50',
      yellow: 'text-yellow-600 bg-yellow-50',
      red: 'text-red-600 bg-red-50',
      purple: 'text-purple-600 bg-purple-50',
      orange: 'text-orange-600 bg-orange-50',
      indigo: 'text-indigo-600 bg-indigo-50',
      gray: 'text-gray-600 bg-gray-50'
    };
    return colors[color] || colors.blue;
  };

  const getChangeColorClasses = (changeType) => {
    if (changeType === 'positive') {
      return 'text-green-600 bg-green-100';
    } else if (changeType === 'negative') {
      return 'text-red-600 bg-red-100';
    }
    return 'text-gray-600 bg-gray-100';
  };

  const sizeClasses = {
    small: 'p-4',
    default: 'p-6',
    large: 'p-8'
  };

  const iconSizes = {
    small: 'h-8 w-8',
    default: 'h-12 w-12',
    large: 'h-16 w-16'
  };

  const valueSizes = {
    small: 'text-2xl',
    default: 'text-3xl',
    large: 'text-4xl'
  };

  return (
    <div className={`bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow ${sizeClasses[size]}`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-gray-600 text-sm font-medium mb-2">{title}</p>
          <p className={`font-bold text-gray-900 mb-2 ${valueSizes[size]}`}>
            {value}
          </p>
          {change && (
            <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${getChangeColorClasses(changeType)}`}>
              {changeType === 'positive' && '↗'}
              {changeType === 'negative' && '↘'}
              {changeType === 'neutral' && '→'}
              <span className="ml-1">{change}</span>
            </div>
          )}
        </div>
        {Icon && (
          <div className={`${getColorClasses(color)} ${iconSizes[size]} rounded-lg flex items-center justify-center flex-shrink-0`}>
            <Icon className={`${iconSizes[size]}`} />
          </div>
        )}
      </div>
    </div>
  );
};

export default StatCard;