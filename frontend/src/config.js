/**
 * Configuration for Elevate Frontend
 */

const config = {
  // API Configuration
  apiUrl: process.env.REACT_APP_API_URL || (
    process.env.NODE_ENV === 'production' 
      ? 'https://your-app.railway.app'  // Replace with your Railway backend URL
      : 'http://localhost:8000'
  ),
  
  // WebSocket Configuration
  wsUrl: process.env.REACT_APP_WS_URL || (
    process.env.NODE_ENV === 'production'
      ? 'wss://your-app.railway.app'  // Replace with your Railway backend URL
      : 'ws://localhost:8000'
  ),
  
  // Environment
  environment: process.env.NODE_ENV || 'development',
  
  // App Configuration
  app: {
    name: 'Elevate Ed',
    version: '2.0.0',
    description: 'Universal Form Automation Platform'
  },
  
  // Features
  features: {
    aiAutomation: true,
    multiFileUpload: true,
    realTimeProgress: true,
    ocrSupport: true
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
    }
  }
};

export default config;
