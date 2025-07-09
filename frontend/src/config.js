/**
 * Configuration for Elevate Frontend
 */

const config = {
  // API Configuration
  apiUrl: process.env.REACT_APP_API_URL || process.env.REACT_APP_BACKEND_URL || (
    process.env.NODE_ENV === 'production' 
      ? 'https://ai-lam-backend-production-5938.up.railway.app'  // Production Railway backend URL
      : 'http://localhost:8000'
  ),
  
  // WebSocket Configuration
  wsUrl: process.env.REACT_APP_WS_URL || (
    process.env.NODE_ENV === 'production'
      ? 'wss://ai-lam-backend-production-5938.up.railway.app'  // Production Railway WebSocket URL
      : 'ws://localhost:8000'
  ),
  
  // Environment
  environment: process.env.REACT_APP_ENVIRONMENT || process.env.NODE_ENV || 'development',
  
  // App Configuration
  app: {
    name: process.env.REACT_APP_APP_NAME || 'Elevate Ed',
    version: process.env.REACT_APP_VERSION || '2.0.0',
    description: 'Universal Form Automation Platform'
  },
  
  // Features
  features: {
    aiAutomation: process.env.REACT_APP_ENABLE_AI_AUTOMATION === 'true',
    multiBrowser: process.env.REACT_APP_ENABLE_MULTI_BROWSER === 'true',
    ekoFeatures: process.env.REACT_APP_ENABLE_EKO_FEATURES === 'true',
    multiFileUpload: true,
    realTimeProgress: true,
    ocrSupport: true
  },
  
  // Supabase Configuration
  supabase: {
    url: process.env.REACT_APP_SUPABASE_URL || 'https://nwtzhzagqfuedsljngkl.supabase.co',
    anonKey: process.env.REACT_APP_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo'
  },
  
  // File Upload Limits
  upload: {
    maxFileSize: 10 * 1024 * 1024, // 10MB
    supportedFormats: ['csv', 'pdf', 'docx', 'txt', 'md', 'jpg', 'jpeg', 'png', 'gif'],
    maxFiles: 5
  },
  
  // API Endpoints
  endpoints: {
    auth: {
      login: '/auth/login',
      register: '/auth/register',
      refresh: '/auth/refresh',
      me: '/auth/me'
    },
    automation: {
      createSession: '/automation/create-session',
      startSession: '/automation/start',
      getStatus: '/automation/status',
      getScreenshots: '/automation/screenshots',
      cancelSession: '/automation/cancel',
      getHistory: '/automation/history',
      aiStatus: '/automation/ai-status'
    },
    admin: {
      stats: '/admin/stats',
      users: '/admin/users',
      updateUserPlan: '/admin/user'
    },
    eko: {
      createSession: '/eko/create-session',
      startAutomation: '/eko/start-automation',
      getStatus: '/eko/status',
      cancelSession: '/eko/cancel',
      processApplications: '/eko/process-applications',
      getSessionTypes: '/eko/session-types'
    }
  }
};

export default config;
