import React, { useState, useEffect } from 'react';
import { BarChart, LineChart, PieChart, TrendingUp, Users, FileText, CheckCircle, Clock } from 'lucide-react';

const Analytics = () => {
  const [timeframe, setTimeframe] = useState('30days');
  const [data, setData] = useState({
    overview: {
      totalApplications: 156,
      successRate: 87.2,
      averageProcessingTime: 3.2,
      activeClients: 42
    },
    trends: {
      applications: [65, 59, 80, 81, 56, 55, 40],
      success: [85, 88, 90, 87, 89, 86, 92]
    },
    universities: [
      { name: 'Oxford', applications: 23, success: 91 },
      { name: 'Cambridge', applications: 19, success: 89 },
      { name: 'Imperial', applications: 18, success: 85 },
      { name: 'LSE', applications: 15, success: 87 },
      { name: 'UCL', applications: 14, success: 83 }
    ],
    courses: [
      { name: 'Computer Science', count: 28 },
      { name: 'Medicine', count: 22 },
      { name: 'Engineering', count: 19 },
      { name: 'Law', count: 15 },
      { name: 'Business', count: 12 }
    ]
  });

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Comprehensive insights into your university application performance
          </p>
        </div>

        {/* Timeframe Selector */}
        <div className="mb-8">
          <div className="flex space-x-2">
            {['7days', '30days', '90days', 'year'].map((period) => (
              <button
                key={period}
                onClick={() => setTimeframe(period)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  timeframe === period
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {period === '7days' && 'Last 7 Days'}
                {period === '30days' && 'Last 30 Days'}
                {period === '90days' && 'Last 90 Days'}
                {period === 'year' && 'This Year'}
              </button>
            ))}
          </div>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Applications</p>
                <p className="text-3xl font-bold text-gray-900">{data.overview.totalApplications}</p>
                <p className="text-green-600 text-sm flex items-center mt-1">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  +12% from last month
                </p>
              </div>
              <FileText className="h-12 w-12 text-blue-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Success Rate</p>
                <p className="text-3xl font-bold text-gray-900">{data.overview.successRate}%</p>
                <p className="text-green-600 text-sm flex items-center mt-1">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  +5.2% from last month
                </p>
              </div>
              <CheckCircle className="h-12 w-12 text-green-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Avg. Processing Time</p>
                <p className="text-3xl font-bold text-gray-900">{data.overview.averageProcessingTime} days</p>
                <p className="text-green-600 text-sm flex items-center mt-1">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  -0.8 days improvement
                </p>
              </div>
              <Clock className="h-12 w-12 text-orange-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Active Clients</p>
                <p className="text-3xl font-bold text-gray-900">{data.overview.activeClients}</p>
                <p className="text-green-600 text-sm flex items-center mt-1">
                  <TrendingUp className="h-4 w-4 mr-1" />
                  +8 new this month
                </p>
              </div>
              <Users className="h-12 w-12 text-purple-600" />
            </div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Application Trends */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Application Trends</h3>
            <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
              <div className="text-center">
                <BarChart className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">Application trend chart would be displayed here</p>
                <p className="text-sm text-gray-500 mt-2">
                  Integration with chart library (Chart.js, Recharts, etc.)
                </p>
              </div>
            </div>
          </div>

          {/* Success Rate Trends */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Success Rate Trends</h3>
            <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
              <div className="text-center">
                <LineChart className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600">Success rate trend chart would be displayed here</p>
                <p className="text-sm text-gray-500 mt-2">
                  Shows success rate progression over time
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* University Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Top Universities by Applications</h3>
            <div className="space-y-4">
              {data.universities.map((uni, index) => (
                <div key={uni.name} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {index + 1}
                    </div>
                    <span className="font-medium text-gray-900">{uni.name}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-semibold text-gray-900">{uni.applications} apps</div>
                    <div className="text-sm text-green-600">{uni.success}% success</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6">Popular Courses</h3>
            <div className="space-y-4">
              {data.courses.map((course, index) => (
                <div key={course.name} className="flex items-center justify-between">
                  <span className="font-medium text-gray-900">{course.name}</span>
                  <div className="flex items-center space-x-3">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full" 
                        style={{ width: `${(course.count / 28) * 100}%` }}
                      ></div>
                    </div>
                    <span className="font-semibold text-gray-900 w-8">{course.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Performance Insights */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Key Insights</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-green-50 p-6 rounded-lg">
              <div className="flex items-center space-x-3 mb-3">
                <CheckCircle className="h-8 w-8 text-green-600" />
                <h4 className="font-semibold text-green-900">High Performance</h4>
              </div>
              <p className="text-green-700">
                Oxford applications show 91% success rate, 6% above average. Consider promoting Oxford-focused services.
              </p>
            </div>

            <div className="bg-blue-50 p-6 rounded-lg">
              <div className="flex items-center space-x-3 mb-3">
                <TrendingUp className="h-8 w-8 text-blue-600" />
                <h4 className="font-semibold text-blue-900">Growth Opportunity</h4>
              </div>
              <p className="text-blue-700">
                Computer Science applications increased 25% this month. Consider expanding technical course offerings.
              </p>
            </div>

            <div className="bg-orange-50 p-6 rounded-lg">
              <div className="flex items-center space-x-3 mb-3">
                <Clock className="h-8 w-8 text-orange-600" />
                <h4 className="font-semibold text-orange-900">Efficiency Gain</h4>
              </div>
              <p className="text-orange-700">
                Processing time reduced by 0.8 days. New automation features are improving turnaround times.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics; 