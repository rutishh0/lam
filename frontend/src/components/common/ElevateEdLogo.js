import React from 'react';

const ElevateEdLogo = ({ size = 'md', showText = true, className = '' }) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8', 
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const textSizeClasses = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-xl',
    xl: 'text-2xl'
  };

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      {/* Logo Icon - Inspired by the stacked circular design */}
      <div className={`relative ${sizeClasses[size]} flex items-center justify-center`}>
        {/* Stacked circular elements representing elevation/progress */}
        <div className="absolute inset-0 flex flex-col justify-center items-center space-y-0.5">
          {/* Top circle - lightest */}
          <div className="w-full h-1 bg-gradient-to-r from-teal-200 to-cyan-200 rounded-full opacity-60"></div>
          {/* Second circle */}
          <div className="w-full h-1 bg-gradient-to-r from-teal-300 to-cyan-300 rounded-full opacity-70"></div>
          {/* Third circle */}
          <div className="w-full h-1.5 bg-gradient-to-r from-teal-400 to-cyan-400 rounded-full opacity-80"></div>
          {/* Fourth circle */}
          <div className="w-full h-1.5 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-full opacity-90"></div>
          {/* Bottom circle - darkest/strongest */}
          <div className="w-full h-2 bg-gradient-to-r from-teal-600 to-cyan-600 rounded-full"></div>
        </div>
      </div>
      
      {/* Company Name */}
      {showText && (
        <span className={`font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent ${textSizeClasses[size]}`}>
          Elevate Ed
        </span>
      )}
    </div>
  );
};

export default ElevateEdLogo; 