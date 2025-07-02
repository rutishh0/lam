# Autonomous University Application Agent

An AI-powered system that automates UK university application submissions, monitoring, and status tracking. The system can autonomously create accounts, fill applications, and monitor admission status across multiple university portals.

⚠️ **LEGAL DISCLAIMER**: This project is for educational and research purposes only. Automated submissions to UCAS and university portals may violate their terms of service. Always ensure you have proper authorization before deploying this system.

## 🚀 Features

### Core Functionality
- **Autonomous Application Submission**: Automatically fills and submits university applications
- **Multi-University Support**: Handles applications to top 10 UK universities simultaneously
- **Status Monitoring**: Daily automated checks for application status updates
- **Secure Data Storage**: End-to-end encryption for sensitive student information
- **Real-time Notifications**: Email and SMS alerts for status changes
- **Analytics Dashboard**: Comprehensive insights and application tracking

### Enhanced Features (New)
- **Advanced Browser Automation**: Stealth mode with anti-detection measures
- **Document Management**: Drag-and-drop file upload with validation
- **Performance Monitoring**: Track automation success rates and system health
- **CAPTCHA Handling**: Integration ready for 2Captcha/Anti-Captcha services
- **Retry Logic**: Intelligent retry mechanisms with exponential backoff
- **Audit Trail**: Complete logging of all system actions for compliance

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React UI      │────▶│  FastAPI Backend │────▶│  Playwright     │
│   (Frontend)    │     │     (API)        │     │  Automation     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                         │
         │                       ▼                         ▼
         │              ┌─────────────────┐      ┌─────────────────┐
         │              │    MongoDB      │      │  University     │
         └─────────────▶│   (Database)    │      │   Portals       │
                        └─────────────────┘      └─────────────────┘
```

### Technology Stack
- **Frontend**: React 19, Tailwind CSS, Recharts, React Router
- **Backend**: FastAPI, Python 3.11+, Motor (async MongoDB)
- **Automation**: Playwright, Browser stealth techniques
- **Database**: MongoDB with field-level encryption
- **Notifications**: Twilio (SMS), SMTP (Email)
- **Security**: Cryptography, JWT tokens, secure credential storage

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18+ and Yarn
- MongoDB (local or cloud instance)
- Gmail account with app password (for email notifications)
- Twilio account (optional, for SMS)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/wendwise112/lam.git
cd lam
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Copy environment variables
cp env.example .env

# Edit .env with your configuration
# - Set MongoDB connection string
# - Add email credentials
# - Generate encryption key
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# Create .env file
echo "REACT_APP_BACKEND_URL=http://localhost:8000" > .env

# Build for production (optional)
yarn build
```

### 4. Database Setup

Ensure MongoDB is running and create the required indexes:

```javascript
// In MongoDB shell or compass
use university_agent_db

// Create indexes
db.clients.createIndex({ "email_hash": 1 })
db.application_tasks.createIndex({ "client_id": 1 })
db.application_tasks.createIndex({ "status": 1 })
```

## 🚀 Running the Application

### Development Mode

1. **Start Backend**:
```bash
cd backend
uvicorn server:app --reload --port 8000
```

2. **Start Frontend**:
```bash
cd frontend
yarn start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment instructions using Google Cloud Platform.

## 📱 Usage Guide

### 1. Adding a Client
- Navigate to "Clients" → "Add Client"
- Fill in personal information, academic history, and course preferences
- Upload required documents (transcripts, personal statement, etc.)
- Submit to store encrypted data

### 2. Running the Agent
- Go to "Agent Control"
- Select a client and target universities
- Click "Create Applications" to start the autonomous process
- Monitor progress in real-time

### 3. Monitoring Applications
- Visit "Monitor" to see all active applications
- Check "Analytics" for insights and performance metrics
- Receive notifications for status changes

### 4. Security Best Practices
- Regularly rotate encryption keys
- Use strong passwords for university accounts
- Enable 2FA where available
- Review audit logs periodically

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Encryption
ENCRYPTION_MASTER_KEY=<generate-using-setup-script>

# Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Browser Automation
MAX_CONCURRENT_BROWSERS=3
BROWSER_TIMEOUT=30000

# Proxy Configuration (optional)
PROXY_POOL=proxy1:port,proxy2:port
```

### University Configuration

Universities are configured in `backend/server.py`:

```python
TOP_UNIVERSITIES = [
    {"name": "University of Oxford", "code": "oxford", "url": "..."},
    {"name": "University of Cambridge", "code": "cambridge", "url": "..."},
    # ... more universities
]
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python backend_test.py
```

### Frontend Tests
```bash
cd frontend
yarn test
```

### Integration Tests
See `tests/` directory for end-to-end test scenarios.

## 📊 API Documentation

### Key Endpoints

- `POST /api/clients` - Create new client with encrypted data
- `GET /api/clients` - List all clients
- `POST /api/agent/execute` - Execute agent commands
- `GET /api/applications` - Get all applications
- `GET /api/analytics/{client_id}` - Get client analytics
- `GET /api/performance/report` - System performance metrics

Full API documentation available at http://localhost:8000/docs when running.

## 🔒 Security Considerations

1. **Data Encryption**: All sensitive data is encrypted at rest using AES-256
2. **Credential Storage**: Application passwords stored separately with additional encryption
3. **HTTPS Required**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting to avoid detection
5. **Audit Logging**: All actions are logged for compliance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Notice

This software is provided for educational purposes only. Users are responsible for ensuring compliance with:
- UCAS Terms of Service
- Individual university application policies
- UK Computer Misuse Act 1990
- GDPR and data protection regulations

Always obtain explicit permission before automating interactions with third-party websites.

## 🙏 Acknowledgments

- Playwright team for the excellent automation framework
- FastAPI for the modern Python web framework
- The open-source community for various libraries used

## 📧 Support

For questions or support, please open an issue on GitHub or contact the maintainers.

---

**Remember**: With great automation comes great responsibility. Use this tool ethically and legally!
