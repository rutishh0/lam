# 🎓 AI LAM - Autonomous University Application Management System

A comprehensive SaaS platform for managing and automating university applications with advanced browser automation, real-time monitoring, and intelligent processing.

## 🌟 Features

### 🤖 **Autonomous Browser Automation**
- Real-time browser automation using Playwright
- Cross-browser compatibility (Chromium, Firefox, WebKit)
- Anti-detection measures and human-like behavior simulation
- Live screenshot capture and progress monitoring
- WebSocket-based real-time updates

### 👥 **User Management & Authentication**
- JWT-based authentication with refresh tokens
- Role-based access control (Admin, User)
- User registration and email verification
- Secure session management

### 📊 **Advanced Admin Dashboard**
- Real-time system monitoring and analytics
- User management and application tracking
- System health monitoring with alerts
- Performance metrics and resource usage
- Audit logs and security monitoring

### 🎯 **Application Processing**
- Multi-university application support
- Document upload and management
- Application status tracking
- Automated form filling and submission
- Progress notifications via email/SMS

## 🏗 Architecture

### **Frontend** (React + TypeScript)
- Modern React 18 with hooks and context
- Real-time updates via WebSocket connections
- Responsive design with Tailwind CSS
- Component-based architecture
- Advanced state management

### **Backend** (Python + FastAPI)
- Async FastAPI with high performance
- Supabase PostgreSQL database
- Real-time WebSocket communication
- Advanced browser automation engine
- Comprehensive monitoring and logging

### **Database** (Supabase)
- PostgreSQL with real-time subscriptions
- Row-level security (RLS)
- Automatic API generation
- Built-in authentication
- Real-time database updates

## 🚀 Quick Start

### **Prerequisites**
- Python 3.9+
- Node.js 16+
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/your-username/ai-lam.git
cd ai-lam
```

### **2. Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file and configure
cp env.example .env
# Edit .env with your Supabase credentials
```

### **3. Frontend Setup**
```bash
cd ../frontend
npm install
# Copy environment file and configure
cp .env.example .env
# Edit .env with your backend URL
```

### **4. Database Setup**
```bash
cd ../backend
python setup_supabase.py
python create_admin.py
```

### **5. Run Development Servers**

**Backend:**
```bash
cd backend
uvicorn server:app --reload --port 8001
```

**Frontend:**
```bash
cd frontend
npm start
```

Visit `http://localhost:3000` to access the application.

## 🌐 Deployment

### **Recommended: Railway + Vercel**

**Backend (Railway.com):**
1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Configure environment variables
4. Deploy automatically with `railway.toml`

**Frontend (Vercel):**
1. Create account at [vercel.com](https://vercel.com)
2. Import your repository
3. Configure build settings for `frontend` directory
4. Set environment variables

📖 **Detailed Guide**: See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

### **Alternative Deployments**
- **Render + Netlify**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Docker**: See [Dockerfile](Dockerfile)

## 🔧 Configuration

### **Environment Variables**

**Backend (.env):**
```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key

# JWT
JWT_SECRET=your_jwt_secret
JWT_REFRESH_SECRET=your_refresh_secret

# Optional Services
STRIPE_SECRET_KEY=your_stripe_key
SENDGRID_API_KEY=your_sendgrid_key
SENTRY_DSN=your_sentry_dsn
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:8001
REACT_APP_SUPABASE_URL=your_supabase_url
REACT_APP_SUPABASE_ANON_KEY=your_anon_key
```

## 🛠 Development

### **Project Structure**
```
ai-lam/
├── backend/                 # Python FastAPI backend
│   ├── auth/               # Authentication services
│   ├── automation/         # Browser automation engine
│   ├── database/           # Database models and clients
│   ├── monitoring/         # System monitoring
│   ├── notifications/      # Email/SMS services
│   ├── security/           # Encryption and security
│   └── server.py          # Main FastAPI application
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   └── App.js         # Main React application
│   └── public/            # Static assets
├── tests/                  # Test files
├── railway.toml           # Railway deployment config
└── RAILWAY_DEPLOYMENT.md  # Deployment guide
```

### **Key Components**

**Browser Automation Engine:**
- `automation/browser_automation.py`: Core automation logic
- `automation/websocket_handler.py`: Real-time communication
- `automation/automation_manager.py`: Session management

**Authentication System:**
- `auth/auth_service.py`: JWT authentication
- `security/encryption.py`: Data encryption
- Role-based access control

**Monitoring System:**
- `monitoring/enhanced_monitor.py`: System metrics
- `monitoring/status_monitor.py`: Application health
- Real-time alerts and notifications

## 🧪 Testing

### **Backend Tests**
```bash
cd backend
python -m pytest tests/ -v
```

### **Frontend Tests**
```bash
cd frontend
npm test
```

### **End-to-End Tests**
```bash
# Start both frontend and backend
npm run test:e2e
```

## 📊 Monitoring & Analytics

### **Built-in Monitoring**
- System resource monitoring (CPU, Memory, Disk)
- Application performance metrics
- Real-time alerts and notifications
- Audit logs and security monitoring

### **External Integrations**
- **Sentry**: Error tracking and performance monitoring
- **Stripe**: Payment processing and analytics
- **SendGrid**: Email delivery and analytics

## 🔒 Security Features

- JWT authentication with refresh tokens
- Rate limiting and DDoS protection
- Data encryption at rest and in transit
- Secure credential storage
- CORS configuration
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Documentation**: See docs in the repository
- **Issues**: [GitHub Issues](https://github.com/your-username/ai-lam/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/ai-lam/discussions)

## 🙏 Acknowledgments

- **Supabase**: For the amazing database and auth platform
- **Railway.com**: For simple and powerful deployment
- **Playwright**: For robust browser automation
- **FastAPI**: For the high-performance Python framework
- **React**: For the flexible frontend framework

---

**Built with ❤️ for streamlining university applications and helping students achieve their dreams!**
