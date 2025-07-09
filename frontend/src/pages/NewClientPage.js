import React from 'react';
import { useNavigate } from 'react-router-dom';
import ClientForm from '../components/ClientForm';
import toast from 'react-hot-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

const NewClientPage = () => {
  const navigate = useNavigate();

  const handleSubmit = async (clientData) => {
    try {
      // Simulate API call to create client
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // In real implementation, you would call:
      // const response = await axios.post(`${API}/clients`, clientData);
      
      console.log('Creating client:', clientData);
      toast.success('Client created successfully!');
      navigate('/clients');
    } catch (error) {
      console.error('Error creating client:', error);
      throw error;
    }
  };

  const handleCancel = () => {
    navigate('/clients');
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Add New Client</h1>
          <p className="text-gray-600 mt-2">
            Enter the student's information to create a new client profile
          </p>
        </div>

        {/* Form */}
        <ClientForm 
          onSubmit={handleSubmit}
          onCancel={handleCancel}
        />
      </div>
    </div>
  );
};

export default NewClientPage;
