import React, { useState, useEffect } from 'react';
import { University, User, Calendar, Target, Settings, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const ApplicationForm = ({ application = null, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    clientId: application?.clientId || '',
    universities: application?.universities || [],
    applicationSettings: application?.applicationSettings || {
      submissionDate: '',
      priority: 'normal',
      personalStatementOptimization: true,
      documentVerification: true,
      statusNotifications: true
    }
  });

  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingClients, setLoadingClients] = useState(true);

  const universities = [
    { code: 'oxford', name: 'University of Oxford', courses: ['Computer Science', 'Mathematics', 'Physics', 'Medicine', 'Law'] },
    { code: 'cambridge', name: 'University of Cambridge', courses: ['Engineering', 'Natural Sciences', 'Mathematics', 'Medicine', 'Law'] },
    { code: 'imperial', name: 'Imperial College London', courses: ['Engineering', 'Medicine', 'Computing', 'Business', 'Natural Sciences'] },
    { code: 'lse', name: 'London School of Economics', courses: ['Economics', 'Politics', 'Law', 'Management', 'Sociology'] },
    { code: 'ucl', name: 'University College London', courses: ['Medicine', 'Engineering', 'Architecture', 'Psychology', 'Law'] },
    { code: 'kcl', name: "King's College London", courses: ['Medicine', 'Law', 'Business', 'War Studies', 'English'] },
    { code: 'edinburgh', name: 'University of Edinburgh', courses: ['Medicine', 'Law', 'Business', 'Engineering', 'Arts'] },
    { code: 'manchester', name: 'University of Manchester', courses: ['Engineering', 'Business', 'Medicine', 'Computer Science', 'Chemistry'] },
    { code: 'warwick', name: 'University of Warwick', courses: ['Business', 'Engineering', 'Mathematics', 'Computer Science', 'Economics'] },
    { code: 'bristol', name: 'University of Bristol', courses: ['Engineering', 'Medicine', 'Law', 'Economics', 'Computer Science'] }
  ];

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      // Simulate API call to fetch clients
      await new Promise(resolve => setTimeout(resolve, 1000));
      setClients([
        { id: '1', name: 'Sarah Johnson', email: 'sarah.johnson@email.com' },
        { id: '2', name: 'Michael Chen', email: 'michael.chen@email.com' },
        { id: '3', name: 'Emma Wilson', email: 'emma.wilson@email.com' }
      ]);
    } catch (error) {
      toast.error('Failed to load clients');
    } finally {
      setLoadingClients(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.startsWith('settings.')) {
      const settingName = name.replace('settings.', '');
      setFormData(prev => ({
        ...prev,
        applicationSettings: {
          ...prev.applicationSettings,
          [settingName]: type === 'checkbox' ? checked : value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value
      }));
    }
  };

  const handleUniversitySelection = (universityCode, isSelected) => {
    if (isSelected) {
      const university = universities.find(u => u.code === universityCode);
      setFormData(prev => ({
        ...prev,
        universities: [
          ...prev.universities,
          {
            code: universityCode,
            name: university.name,
            course: '',
            courseCode: '',
            entryYear: new Date().getFullYear() + 1,
            priority: prev.universities.length + 1
          }
        ]
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        universities: prev.universities.filter(u => u.code !== universityCode)
      }));
    }
  };

  const updateUniversity = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      universities: prev.universities.map((uni, i) => 
        i === index ? { ...uni, [field]: value } : uni
      )
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.universities.length === 0) {
      toast.error('Please select at least one university');
      return;
    }

    setLoading(true);

    try {
      await onSubmit(formData);
      toast.success(application ? 'Application updated successfully!' : 'Application created successfully!');
    } catch (error) {
      toast.error('Failed to save application');
    } finally {
      setLoading(false);
    }
  };

  if (loadingClients) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Loading clients...</span>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Client Selection */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <User className="h-6 w-6 text-blue-600 mr-2" />
          Select Client
        </h3>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Client *
          </label>
          <select
            name="clientId"
            value={formData.clientId}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select a client</option>
            {clients.map((client) => (
              <option key={client.id} value={client.id}>
                {client.name} ({client.email})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* University Selection */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <University className="h-6 w-6 text-blue-600 mr-2" />
          Select Universities
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {universities.map((university) => {
            const isSelected = formData.universities.some(u => u.code === university.code);
            return (
              <div
                key={university.code}
                className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                  isSelected 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => handleUniversitySelection(university.code, !isSelected)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-semibold text-gray-900">{university.name}</h4>
                    <p className="text-sm text-gray-600">{university.courses.length} courses available</p>
                  </div>
                  {isSelected && <CheckCircle className="h-6 w-6 text-blue-600" />}
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Universities Details */}
        {formData.universities.length > 0 && (
          <div className="space-y-6">
            <h4 className="text-lg font-semibold text-gray-900">Configure Selected Universities</h4>
            {formData.universities.map((uni, index) => {
              const university = universities.find(u => u.code === uni.code);
              return (
                <div key={uni.code} className="border border-gray-200 rounded-lg p-6">
                  <h5 className="font-semibold text-gray-900 mb-4">{uni.name}</h5>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Course *
                      </label>
                      <select
                        value={uni.course}
                        onChange={(e) => updateUniversity(index, 'course', e.target.value)}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="">Select course</option>
                        {university?.courses.map(course => (
                          <option key={course} value={course}>{course}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Course Code
                      </label>
                      <input
                        type="text"
                        value={uni.courseCode}
                        onChange={(e) => updateUniversity(index, 'courseCode', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="e.g., CS101"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Entry Year *
                      </label>
                      <input
                        type="number"
                        value={uni.entryYear}
                        onChange={(e) => updateUniversity(index, 'entryYear', parseInt(e.target.value))}
                        required
                        min={new Date().getFullYear()}
                        max={new Date().getFullYear() + 3}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Application Settings */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <Settings className="h-6 w-6 text-blue-600 mr-2" />
          Application Settings
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Submission Date
            </label>
            <input
              type="date"
              name="settings.submissionDate"
              value={formData.applicationSettings.submissionDate}
              onChange={handleChange}
              min={new Date().toISOString().split('T')[0]}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Processing Priority
            </label>
            <select
              name="settings.priority"
              value={formData.applicationSettings.priority}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="low">Low Priority</option>
              <option value="normal">Normal Priority</option>
              <option value="high">High Priority</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
        </div>

        <div className="mt-6 space-y-4">
          <div className="flex items-center">
            <input
              type="checkbox"
              name="settings.personalStatementOptimization"
              checked={formData.applicationSettings.personalStatementOptimization}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label className="ml-2 text-sm text-gray-700">
              Enable AI personal statement optimization
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              name="settings.documentVerification"
              checked={formData.applicationSettings.documentVerification}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label className="ml-2 text-sm text-gray-700">
              Automatic document verification
            </label>
          </div>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              name="settings.statusNotifications"
              checked={formData.applicationSettings.statusNotifications}
              onChange={handleChange}
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label className="ml-2 text-sm text-gray-700">
              Send status update notifications
            </label>
          </div>
        </div>
      </div>

      {/* Summary */}
      {formData.universities.length > 0 && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <Target className="h-6 w-6 text-blue-600 mr-2" />
            Application Summary
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl font-bold text-blue-600">{formData.universities.length}</div>
              <div className="text-gray-600">Universities Selected</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl font-bold text-green-600">{formData.applicationSettings.priority}</div>
              <div className="text-gray-600">Processing Priority</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="text-2xl font-bold text-purple-600">
                {formData.applicationSettings.submissionDate || 'ASAP'}
              </div>
              <div className="text-gray-600">Submission Date</div>
            </div>
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-end space-x-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading || formData.universities.length === 0}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating...' : (application ? 'Update Application' : 'Create Application')}
        </button>
      </div>
    </form>
  );
};

export default ApplicationForm;
