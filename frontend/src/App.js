import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import { 
  Bot, 
  Users, 
  FileText, 
  Settings, 
  Play, 
  Pause, 
  CheckCircle, 
  AlertCircle,
  Clock,
  University,
  Upload,
  Eye,
  Plus,
  Monitor,
  BarChart,
  Shield
} from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import Analytics from './components/Analytics';
import DocumentUpload from './components/DocumentUpload';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Dashboard Components
const Dashboard = () => {
  const [stats, setStats] = useState({
    totalClients: 0,
    activeApplications: 0,
    successfulApplications: 0,
    pendingApplications: 0
  });

  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [clientsRes, applicationsRes] = await Promise.all([
        axios.get(`${API}/clients`),
        axios.get(`${API}/applications`)
      ]);

      const clients = clientsRes.data;
      const applications = applicationsRes.data;

      setStats({
        totalClients: clients.length,
        activeApplications: applications.filter(app => app.status === 'in_progress').length,
        successfulApplications: applications.filter(app => app.status === 'accepted').length,
        pendingApplications: applications.filter(app => app.status === 'pending').length
      });

      setRecentActivity(applications.slice(0, 5));
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    }
  };

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Agent Dashboard</h1>
        <p className="text-gray-600">Monitor and control your autonomous university application agent</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Clients</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.totalClients}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Applications</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.activeApplications}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Successful</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.successfulApplications}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-yellow-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-2xl font-semibold text-gray-900">{stats.pendingApplications}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Link to="/clients/new" className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <Plus className="h-8 w-8" />
            <div className="ml-4">
              <h3 className="text-lg font-semibold">Add New Client</h3>
              <p className="text-blue-100">Register a new client for applications</p>
            </div>
          </div>
        </Link>

        <Link to="/agent-control" className="bg-gradient-to-r from-green-600 to-green-700 text-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <Bot className="h-8 w-8" />
            <div className="ml-4">
              <h3 className="text-lg font-semibold">Agent Control</h3>
              <p className="text-green-100">Execute agent commands</p>
            </div>
          </div>
        </Link>

        <Link to="/monitor" className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <Monitor className="h-8 w-8" />
            <div className="ml-4">
              <h3 className="text-lg font-semibold">Monitor Applications</h3>
              <p className="text-purple-100">Track application status</p>
            </div>
          </div>
        </Link>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="px-6 py-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
        </div>
        <div className="p-6">
          {recentActivity.length > 0 ? (
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
                  <University className="h-5 w-5 text-gray-600" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{activity.university_name}</p>
                    <p className="text-xs text-gray-600">{activity.course_name}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    activity.status === 'accepted' ? 'bg-green-100 text-green-800' :
                    activity.status === 'rejected' ? 'bg-red-100 text-red-800' :
                    activity.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {activity.status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">No recent activity</p>
          )}
        </div>
      </div>
    </div>
  );
};

const ClientManagement = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
      toast.error('Failed to load clients');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-6">Loading clients...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Client Management</h1>
        <Link
          to="/clients/new"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>Add Client</span>
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-sm border">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Client
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nationality
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {clients.map((client) => (
                <tr key={client.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{client.full_name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">{client.email}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">{client.nationality}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">
                      {new Date(client.created_at).toLocaleDateString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex items-center space-x-3">
                      <Link
                        to={`/analytics/${client.id}`}
                        className="text-green-600 hover:text-green-900"
                        title="View Analytics"
                      >
                        <BarChart className="h-4 w-4" />
                      </Link>
                      <Link
                        to={`/clients/${client.id}`}
                        className="text-blue-600 hover:text-blue-900"
                        title="View Details"
                      >
                        <Eye className="h-4 w-4" />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const NewClientForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    nationality: '',
    address: '',
    personal_statement: '',
    academic_history: [{ institution: '', qualification: '', grade: '', year: '' }],
    course_preferences: [{ university: '', course_name: '', course_code: '', entry_year: '' }],
    documents: {}
  });

  const [submitting, setSubmitting] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAcademicChange = (index, field, value) => {
    const newHistory = [...formData.academic_history];
    newHistory[index][field] = value;
    setFormData(prev => ({
      ...prev,
      academic_history: newHistory
    }));
  };

  const handleCourseChange = (index, field, value) => {
    const newPreferences = [...formData.course_preferences];
    newPreferences[index][field] = value;
    setFormData(prev => ({
      ...prev,
      course_preferences: newPreferences
    }));
  };

  const addAcademicEntry = () => {
    setFormData(prev => ({
      ...prev,
      academic_history: [...prev.academic_history, { institution: '', qualification: '', grade: '', year: '' }]
    }));
  };

  const addCoursePreference = () => {
    setFormData(prev => ({
      ...prev,
      course_preferences: [...prev.course_preferences, { university: '', course_name: '', course_code: '', entry_year: '' }]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await axios.post(`${API}/clients`, formData);
      toast.success('Client created successfully!');
      navigate('/clients');
    } catch (error) {
      console.error('Error creating client:', error);
      toast.error('Failed to create client');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Add New Client</h1>
        <p className="text-gray-600">Enter client information for autonomous applications</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Personal Information */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
              <input
                type="date"
                name="date_of_birth"
                value={formData.date_of_birth}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nationality</label>
              <input
                type="text"
                name="nationality"
                value={formData.nationality}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
              <textarea
                name="address"
                value={formData.address}
                onChange={handleInputChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>
        </div>

        {/* Academic History */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Academic History</h2>
            <button
              type="button"
              onClick={addAcademicEntry}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              + Add Entry
            </button>
          </div>
          {formData.academic_history.map((entry, index) => (
            <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input
                type="text"
                placeholder="Institution"
                value={entry.institution}
                onChange={(e) => handleAcademicChange(index, 'institution', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Qualification"
                value={entry.qualification}
                onChange={(e) => handleAcademicChange(index, 'qualification', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Grade"
                value={entry.grade}
                onChange={(e) => handleAcademicChange(index, 'grade', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Year"
                value={entry.year}
                onChange={(e) => handleAcademicChange(index, 'year', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}
        </div>

        {/* Course Preferences */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Course Preferences</h2>
            <button
              type="button"
              onClick={addCoursePreference}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              + Add Course
            </button>
          </div>
          {formData.course_preferences.map((preference, index) => (
            <div key={index} className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input
                type="text"
                placeholder="University"
                value={preference.university}
                onChange={(e) => handleCourseChange(index, 'university', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Course Name"
                value={preference.course_name}
                onChange={(e) => handleCourseChange(index, 'course_name', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Course Code"
                value={preference.course_code}
                onChange={(e) => handleCourseChange(index, 'course_code', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Entry Year"
                value={preference.entry_year}
                onChange={(e) => handleCourseChange(index, 'entry_year', e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          ))}
        </div>

        {/* Personal Statement */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Personal Statement</h2>
          <textarea
            name="personal_statement"
            value={formData.personal_statement}
            onChange={handleInputChange}
            rows={8}
            placeholder="Enter personal statement..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* Document Upload */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Documents</h2>
          <DocumentUpload 
            onDocumentsChange={(docs) => setFormData(prev => ({ ...prev, documents: docs }))}
            existingDocuments={formData.documents}
          />
        </div>

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
          <Link
            to="/clients"
            className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </Link>
          <button
            type="submit"
            disabled={submitting}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {submitting ? 'Creating...' : 'Create Client'}
          </button>
        </div>
      </form>
    </div>
  );
};

const AgentControl = () => {
  const [clients, setClients] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [selectedClient, setSelectedClient] = useState('');
  const [selectedUniversities, setSelectedUniversities] = useState([]);
  const [courseName, setCourseName] = useState('');
  const [courseCode, setCourseCode] = useState('');
  const [executing, setExecuting] = useState(false);

  useEffect(() => {
    fetchClients();
    fetchUniversities();
  }, []);

  const fetchClients = async () => {
    try {
      const response = await axios.get(`${API}/clients`);
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
    }
  };

  const fetchUniversities = async () => {
    try {
      const response = await axios.get(`${API}/universities`);
      setUniversities(response.data.universities);
    } catch (error) {
      console.error('Error fetching universities:', error);
    }
  };

  const handleUniversitySelection = (universityCode) => {
    setSelectedUniversities(prev => 
      prev.includes(universityCode) 
        ? prev.filter(code => code !== universityCode)
        : [...prev, universityCode]
    );
  };

  const executeApplications = async () => {
    if (!selectedClient || selectedUniversities.length === 0) {
      toast.error('Please select a client and at least one university');
      return;
    }

    setExecuting(true);
    try {
      const command = {
        command_type: 'create_applications',
        client_id: selectedClient,
        parameters: {
          universities: selectedUniversities,
          course_name: courseName || 'Computer Science',
          course_code: courseCode || 'CS101'
        }
      };

      const response = await axios.post(`${API}/agent/execute`, command);
      toast.success('Agent execution started! Applications are being created.');
    } catch (error) {
      console.error('Error executing agent:', error);
      toast.error('Failed to execute agent command');
    } finally {
      setExecuting(false);
    }
  };

  const checkApplicationStatus = async () => {
    if (!selectedClient) {
      toast.error('Please select a client');
      return;
    }

    setExecuting(true);
    try {
      const command = {
        command_type: 'check_status',
        client_id: selectedClient,
        parameters: {}
      };

      const response = await axios.post(`${API}/agent/execute`, command);
      toast.success('Status check started! Results will be updated shortly.');
    } catch (error) {
      console.error('Error checking status:', error);
      toast.error('Failed to check application status');
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Agent Control Panel</h1>
        <p className="text-gray-600">Execute autonomous agent commands</p>
      </div>

      <div className="space-y-6">
        {/* Client Selection */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Client</h2>
          <select
            value={selectedClient}
            onChange={(e) => setSelectedClient(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Choose a client...</option>
            {clients.map(client => (
              <option key={client.id} value={client.id}>
                {client.full_name} - {client.email}
              </option>
            ))}
          </select>
        </div>

        {/* University Selection */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Universities</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {universities.map(university => (
              <label key={university.code} className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50">
                <input
                  type="checkbox"
                  checked={selectedUniversities.includes(university.code)}
                  onChange={() => handleUniversitySelection(university.code)}
                  className="form-checkbox h-4 w-4 text-blue-600"
                />
                <div>
                  <div className="font-medium text-gray-900">{university.name}</div>
                  <div className="text-sm text-gray-500">{university.code}</div>
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Course Details */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Course Details</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Course Name</label>
              <input
                type="text"
                value={courseName}
                onChange={(e) => setCourseName(e.target.value)}
                placeholder="e.g., Computer Science"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Course Code</label>
              <input
                type="text"
                value={courseCode}
                onChange={(e) => setCourseCode(e.target.value)}
                placeholder="e.g., CS101"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Agent Actions */}
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Agent Actions</h2>
          <div className="flex space-x-4">
            <button
              onClick={executeApplications}
              disabled={executing}
              className="flex items-center space-x-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              <Play className="h-4 w-4" />
              <span>{executing ? 'Executing...' : 'Create Applications'}</span>
            </button>
            <button
              onClick={checkApplicationStatus}
              disabled={executing}
              className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              <Monitor className="h-4 w-4" />
              <span>Check Status</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const ApplicationMonitor = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
    // Set up polling for real-time updates
    const interval = setInterval(fetchApplications, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await axios.get(`${API}/applications`);
      setApplications(response.data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'accepted': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'submitted': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return <div className="p-6">Loading applications...</div>;
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Application Monitor</h1>
        <p className="text-gray-600">Real-time monitoring of university applications</p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  University
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Course
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Checked
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {applications.map((app) => (
                <tr key={app.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <University className="h-5 w-5 text-gray-400 mr-2" />
                      <div className="text-sm font-medium text-gray-900">{app.university_name}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{app.course_name}</div>
                    <div className="text-sm text-gray-500">{app.course_code}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(app.status)}`}>
                      {app.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(app.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {app.last_checked ? new Date(app.last_checked).toLocaleDateString() : 'Never'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

// Mock University Portal Component
const MockUniversityPortal = ({ universityCode }) => {
  const [university, setUniversity] = useState(null);
  const [formFields, setFormFields] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUniversityPortal();
  }, [universityCode]);

  const fetchUniversityPortal = async () => {
    try {
      const response = await axios.get(`${API}/mock-university/${universityCode}`);
      setUniversity(response.data.university);
      setFormFields(response.data.form_fields);
    } catch (error) {
      console.error('Error fetching university portal:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-6">Loading university portal...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">{university.name}</h1>
          <p className="text-gray-600">Online Application Portal</p>
        </div>
      </div>
      
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-lg font-semibold mb-4">Application Form</h2>
          <p className="text-gray-600 mb-6">
            This is a mock university portal for testing the autonomous agent. 
            The agent will interact with forms like this to submit applications.
          </p>
          
          <div className="space-y-6">
            {Object.entries(formFields).map(([section, fields]) => (
              <div key={section} className="border rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-3 capitalize">
                  {section.replace('_', ' ')}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {fields.map((field, index) => (
                    <input
                      key={index}
                      type="text"
                      placeholder={field.replace('_', ' ')}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      readOnly
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-6 flex justify-end">
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Submit Application
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Navigation Component
const Navigation = () => {
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Bot className="h-8 w-8 text-blue-600 mr-2" />
            <Link to="/" className="text-xl font-bold text-gray-900">
              UniAgent
            </Link>
          </div>
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
              <Monitor className="h-4 w-4" />
              <span>Dashboard</span>
            </Link>
            <Link to="/clients" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
              <Users className="h-4 w-4" />
              <span>Clients</span>
            </Link>
            <Link to="/agent-control" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
              <Bot className="h-4 w-4" />
              <span>Agent Control</span>
            </Link>
            <Link to="/monitor" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
              <FileText className="h-4 w-4" />
              <span>Monitor</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

// Analytics wrapper component
const ClientAnalytics = () => {
  const { clientId } = useParams();
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Client Analytics</h1>
        <p className="text-gray-600">Insights and performance metrics</p>
      </div>
      <Analytics clientId={clientId} />
    </div>
  );
};

// Main App Component
function App() {
  return (
    <div className="App min-h-screen bg-gray-50">
      <BrowserRouter>
        <Navigation />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/clients" element={<ClientManagement />} />
          <Route path="/clients/new" element={<NewClientForm />} />
          <Route path="/agent-control" element={<AgentControl />} />
          <Route path="/monitor" element={<ApplicationMonitor />} />
          <Route path="/analytics/:clientId" element={<ClientAnalytics />} />
          <Route path="/mock-university/:universityCode" element={
            <MockUniversityPortal universityCode={window.location.pathname.split('/').pop()} />
          } />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;