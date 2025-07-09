import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import toast, { Toaster } from 'react-hot-toast';

// Context Providers
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Layout Components
import DashboardLayout from './components/layout/DashboardLayout';

// Page Components
import ModernDashboard from './components/dashboard/ModernDashboard';
import AutomationPanel from './components/automation/AutomationPanel';

// Existing Components (will gradually migrate these)
import Analytics from './components/Analytics';
import DocumentUpload from './components/DocumentUpload';
import AdminPanel from './components/AdminPanel';
import NewClientPage from './pages/NewClientPage';

// Auth Components (keeping simplified versions for now)
import SignInPage from './components/auth/SignInPage';
import SignUpPage from './components/auth/SignUpPage';
import LandingPage from './components/landing/LandingPage';

// Protected Route Component
const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/signin" replace />;
  }

  if (adminOnly && !isAdmin) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// Public Route Component (redirects if authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

function AppModern() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={
            <PublicRoute>
              <LandingPage />
            </PublicRoute>
          } />
          <Route path="/signin" element={
            <PublicRoute>
              <SignInPage />
            </PublicRoute>
          } />
          <Route path="/signup" element={
            <PublicRoute>
              <SignUpPage />
            </PublicRoute>
          } />

          {/* Protected Routes with Dashboard Layout */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <DashboardLayout>
                <ModernDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          } />
          
          <Route path="/automation" element={
            <ProtectedRoute>
              <DashboardLayout>
                <AutomationPanel />
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/analytics" element={
            <ProtectedRoute>
              <DashboardLayout>
                <Analytics />
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/clients" element={
            <ProtectedRoute>
              <DashboardLayout>
                <NewClientPage />
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/applications" element={
            <ProtectedRoute>
              <DashboardLayout>
                <DocumentUpload />
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/admin" element={
            <ProtectedRoute adminOnly>
              <DashboardLayout>
                <AdminPanel />
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/monitor" element={
            <ProtectedRoute>
              <DashboardLayout>
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">System Monitor</h2>
                  <p className="text-gray-600">Real-time system monitoring coming soon...</p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/settings" element={
            <ProtectedRoute>
              <DashboardLayout>
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Settings</h2>
                  <p className="text-gray-600">Application settings coming soon...</p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } />

          <Route path="/help" element={
            <ProtectedRoute>
              <DashboardLayout>
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Help & Support</h2>
                  <p className="text-gray-600">Help documentation coming soon...</p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } />

          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#fff',
              color: '#374151',
              borderRadius: '12px',
              boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
              border: '1px solid #e5e7eb'
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default AppModern; 