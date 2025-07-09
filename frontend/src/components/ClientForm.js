import React, { useState } from 'react';
import { User, Mail, Phone, MapPin, Calendar, Upload, FileText } from 'lucide-react';
import toast from 'react-hot-toast';

const ClientForm = ({ client = null, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    fullName: client?.fullName || '',
    email: client?.email || '',
    phone: client?.phone || '',
    dateOfBirth: client?.dateOfBirth || '',
    nationality: client?.nationality || '',
    address: client?.address || '',
    personalStatement: client?.personalStatement || '',
    academicHistory: client?.academicHistory || [
      {
        institution: '',
        qualification: '',
        grade: '',
        year: '',
        subjects: ''
      }
    ],
    coursePreferences: client?.coursePreferences || [
      {
        university: '',
        course: '',
        courseCode: '',
        entryYear: ''
      }
    ],
    documents: client?.documents || {}
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleArrayChange = (arrayName, index, field, value) => {
    setFormData(prev => ({
      ...prev,
      [arrayName]: prev[arrayName].map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const addArrayItem = (arrayName, template) => {
    setFormData(prev => ({
      ...prev,
      [arrayName]: [...prev[arrayName], template]
    }));
  };

  const removeArrayItem = (arrayName, index) => {
    setFormData(prev => ({
      ...prev,
      [arrayName]: prev[arrayName].filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await onSubmit(formData);
      toast.success(client ? 'Client updated successfully!' : 'Client created successfully!');
    } catch (error) {
      toast.error('Failed to save client');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {/* Personal Information */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <User className="h-6 w-6 text-blue-600 mr-2" />
          Personal Information
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name *
            </label>
            <input
              type="text"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter full name"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter email address"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number *
            </label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="+44 7700 900123"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date of Birth *
            </label>
            <input
              type="date"
              name="dateOfBirth"
              value={formData.dateOfBirth}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nationality *
            </label>
            <select
              name="nationality"
              value={formData.nationality}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Select nationality</option>
              <option value="British">British</option>
              <option value="American">American</option>
              <option value="Canadian">Canadian</option>
              <option value="Australian">Australian</option>
              <option value="Indian">Indian</option>
              <option value="Chinese">Chinese</option>
              <option value="Other">Other</option>
            </select>
          </div>
        </div>
        
        <div className="mt-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Address *
          </label>
          <textarea
            name="address"
            value={formData.address}
            onChange={handleChange}
            required
            rows={3}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter full address"
          />
        </div>
      </div>

      {/* Academic History */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-900 flex items-center">
            <Calendar className="h-6 w-6 text-blue-600 mr-2" />
            Academic History
          </h3>
          <button
            type="button"
            onClick={() => addArrayItem('academicHistory', {
              institution: '',
              qualification: '',
              grade: '',
              year: '',
              subjects: ''
            })}
            className="bg-blue-50 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors"
          >
            Add Education
          </button>
        </div>
        
        {formData.academicHistory.map((edu, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-6 mb-4">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-gray-900">Education {index + 1}</h4>
              {formData.academicHistory.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('academicHistory', index)}
                  className="text-red-600 hover:text-red-700"
                >
                  Remove
                </button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Institution Name"
                value={edu.institution}
                onChange={(e) => handleArrayChange('academicHistory', index, 'institution', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                placeholder="Qualification (e.g., A-Levels, GCSE)"
                value={edu.qualification}
                onChange={(e) => handleArrayChange('academicHistory', index, 'qualification', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                placeholder="Grade (e.g., A*AA, 9876)"
                value={edu.grade}
                onChange={(e) => handleArrayChange('academicHistory', index, 'grade', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="number"
                placeholder="Year"
                value={edu.year}
                onChange={(e) => handleArrayChange('academicHistory', index, 'year', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <input
              type="text"
              placeholder="Subjects (e.g., Mathematics, Physics, Chemistry)"
              value={edu.subjects}
              onChange={(e) => handleArrayChange('academicHistory', index, 'subjects', e.target.value)}
              className="w-full mt-4 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        ))}
      </div>

      {/* Course Preferences */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-900 flex items-center">
            <FileText className="h-6 w-6 text-blue-600 mr-2" />
            Course Preferences
          </h3>
          <button
            type="button"
            onClick={() => addArrayItem('coursePreferences', {
              university: '',
              course: '',
              courseCode: '',
              entryYear: ''
            })}
            className="bg-blue-50 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors"
          >
            Add Course
          </button>
        </div>
        
        {formData.coursePreferences.map((course, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-6 mb-4">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-gray-900">Course Choice {index + 1}</h4>
              {formData.coursePreferences.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('coursePreferences', index)}
                  className="text-red-600 hover:text-red-700"
                >
                  Remove
                </button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <select
                value={course.university}
                onChange={(e) => handleArrayChange('coursePreferences', index, 'university', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select University</option>
                <option value="University of Oxford">University of Oxford</option>
                <option value="University of Cambridge">University of Cambridge</option>
                <option value="Imperial College London">Imperial College London</option>
                <option value="London School of Economics">London School of Economics</option>
                <option value="University College London">University College London</option>
                <option value="King's College London">King's College London</option>
                <option value="University of Edinburgh">University of Edinburgh</option>
                <option value="University of Manchester">University of Manchester</option>
                <option value="University of Warwick">University of Warwick</option>
                <option value="University of Bristol">University of Bristol</option>
              </select>
              <input
                type="text"
                placeholder="Course Name"
                value={course.course}
                onChange={(e) => handleArrayChange('coursePreferences', index, 'course', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="text"
                placeholder="Course Code"
                value={course.courseCode}
                onChange={(e) => handleArrayChange('coursePreferences', index, 'courseCode', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <input
                type="number"
                placeholder="Entry Year"
                value={course.entryYear}
                onChange={(e) => handleArrayChange('coursePreferences', index, 'entryYear', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        ))}
      </div>

      {/* Personal Statement */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
          <FileText className="h-6 w-6 text-blue-600 mr-2" />
          Personal Statement
        </h3>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Personal Statement *
          </label>
          <textarea
            name="personalStatement"
            value={formData.personalStatement}
            onChange={handleChange}
            required
            rows={8}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Write your personal statement here. Explain your motivation, achievements, and aspirations..."
          />
          <p className="text-sm text-gray-500 mt-2">
            Recommended length: 4000 characters (approximately 500-600 words)
          </p>
        </div>
      </div>

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
          disabled={loading}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Saving...' : (client ? 'Update Client' : 'Create Client')}
        </button>
      </div>
    </form>
  );
};

export default ClientForm;
