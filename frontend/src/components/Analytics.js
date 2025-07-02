import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart,
  LineChart,
  TrendingUp,
  Clock,
  AlertTriangle,
  CheckCircle,
  Target,
  Calendar
} from 'lucide-react';
import toast from 'react-hot-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Analytics = ({ clientId }) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (clientId) {
      fetchAnalytics();
    }
  }, [clientId]);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API}/analytics/${clientId}`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      toast.error('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="text-center py-8 text-gray-500">
        No analytics data available
      </div>
    );
  }

  const { analytics: data, insights, deadlines } = analytics;

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('overview')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'overview'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('insights')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'insights'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Insights
          </button>
          <button
            onClick={() => setActiveTab('deadlines')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'deadlines'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Deadlines
          </button>
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Success Rate Card */}
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Success Rate</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {data.success_rate?.toFixed(1)}%
                </p>
              </div>
              <div className={`p-3 rounded-full ${
                data.success_rate > 30 ? 'bg-green-100' : 'bg-yellow-100'
              }`}>
                <Target className={`h-6 w-6 ${
                  data.success_rate > 30 ? 'text-green-600' : 'text-yellow-600'
                }`} />
              </div>
            </div>
          </div>

          {/* Total Applications Card */}
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Applications</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {data.total_applications}
                </p>
              </div>
              <div className="p-3 rounded-full bg-blue-100">
                <BarChart className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Average Response Time Card */}
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {data.average_response_time ? `${Math.round(data.average_response_time)} days` : 'N/A'}
                </p>
              </div>
              <div className="p-3 rounded-full bg-purple-100">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>

          {/* Pending Applications Card */}
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {(data.status_breakdown?.pending || 0) + (data.status_breakdown?.submitted || 0)}
                </p>
              </div>
              <div className="p-3 rounded-full bg-orange-100">
                <Clock className="h-6 w-6 text-orange-600" />
              </div>
            </div>
          </div>

          {/* Status Breakdown Chart */}
          <div className="col-span-full bg-white p-6 rounded-lg shadow-sm border">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Application Status Distribution</h3>
            <div className="space-y-4">
              {Object.entries(data.status_breakdown || {}).map(([status, count]) => (
                <div key={status}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="capitalize text-gray-600">{status.replace('_', ' ')}</span>
                    <span className="font-medium">{count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        status === 'accepted' ? 'bg-green-600' :
                        status === 'rejected' ? 'bg-red-600' :
                        status === 'interview_scheduled' ? 'bg-blue-600' :
                        'bg-gray-400'
                      }`}
                      style={{ width: `${(count / data.total_applications) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* University Breakdown */}
          <div className="col-span-full bg-white p-6 rounded-lg shadow-sm border">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Applications by University</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(data.university_breakdown || {}).map(([university, count]) => (
                <div key={university} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm font-medium text-gray-700">{university}</span>
                  <span className="text-sm font-semibold text-gray-900">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Insights Tab */}
      {activeTab === 'insights' && (
        <div className="space-y-4">
          {insights && insights.length > 0 ? (
            insights.map((insight, index) => (
              <div key={index} className="bg-white p-4 rounded-lg shadow-sm border flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <TrendingUp className="h-5 w-5 text-blue-600 mt-0.5" />
                </div>
                <p className="text-gray-700">{insight}</p>
              </div>
            ))
          ) : (
            <div className="bg-white p-8 rounded-lg shadow-sm border text-center text-gray-500">
              No insights available yet. Check back after submitting applications.
            </div>
          )}
        </div>
      )}

      {/* Deadlines Tab */}
      {activeTab === 'deadlines' && (
        <div className="space-y-4">
          {deadlines && deadlines.length > 0 ? (
            deadlines.map((deadline, index) => (
              <div key={index} className={`bg-white p-4 rounded-lg shadow-sm border ${
                deadline.urgency === 'high' ? 'border-red-300' : 'border-gray-200'
              }`}>
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3">
                    <div className={`flex-shrink-0 p-2 rounded-full ${
                      deadline.urgency === 'high' ? 'bg-red-100' : 'bg-yellow-100'
                    }`}>
                      <Calendar className={`h-5 w-5 ${
                        deadline.urgency === 'high' ? 'text-red-600' : 'text-yellow-600'
                      }`} />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{deadline.university}</h4>
                      <p className="text-sm text-gray-600 mt-1">{deadline.action}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        Deadline: {new Date(deadline.deadline).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      deadline.urgency === 'high' 
                        ? 'bg-red-100 text-red-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {deadline.days_remaining} days left
                    </span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="bg-white p-8 rounded-lg shadow-sm border text-center text-gray-500">
              No upcoming deadlines
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Analytics; 