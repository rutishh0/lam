# Autonomous University Application Agent

An AI-powered system for automating UK university application submissions with enterprise-grade security, monitoring, and analytics.

## 🚨 IMPORTANT LEGAL DISCLAIMER

**WARNING: This system may violate UCAS Terms of Service**

Before using this system, please be aware that:

1. **UCAS Terms of Service Compliance**: UCAS (Universities and Colleges Admissions Service) terms may prohibit automated submissions or third-party application submissions.

2. **University-Specific Policies**: Individual universities may have policies against automated applications.

3. **Legal Responsibility**: Users are solely responsible for ensuring compliance with all applicable terms of service, privacy policies, and regulations.

4. **Intended Use**: This system is designed for **educational and research purposes** to demonstrate autonomous automation capabilities.

5. **Recommendation**: Always review and comply with the terms of service of UCAS and individual universities before using this system for actual applications.

## 🏗️ Architecture

The system consists of:
- **Backend**: FastAPI server with Supabase database integration
- **Frontend**: React dashboard with Tailwind CSS
- **Security**: AES-256 encryption for sensitive data
- **Automation**: Playwright-based browser automation with anti-detection
- **Monitoring**: Real-time analytics and performance tracking
- **Notifications**: Email and SMS alerts

## 🗄️ Database Setup (Supabase)

### Prerequisites
1. Create a Supabase account at [https://supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and API keys

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the `backend` directory:
   ```env
   # Supabase Database Configuration
   SUPABASE_URL=https://nwtzhzagqfuedsljngkl.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im53dHpoemFncWZ1ZWRzbGpuZ2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE0NjEwMTQsImV4cCI6MjA2NzAzNzAxNH0.4f0tNJCWwTXFwOb9wjd581RZZhyv3GezW0nGmhDwYAo
   
   # Encryption Configuration
   ENCRYPTION_MASTER_KEY=your-32-char-encryption-key-here
   
   # Email Configuration (Gmail example)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   
   # Twilio Configuration (for SMS)
   TWILIO_ACCOUNT_SID=your-twilio-account-sid
   TWILIO_AUTH_TOKEN=your-twilio-auth-token
   TWILIO_FROM_NUMBER=+1234567890
   
   # Frontend URL
   FRONTEND_URL=http://localhost:3000
   ```

3. **Create Database Tables**:
   
   **Option A: Using Supabase Dashboard** (Recommended)
   1. Go to your Supabase dashboard: [https://supabase.com/dashboard](https://supabase.com/dashboard)
   2. Navigate to your project: `nwtzhzagqfuedsljngkl`
   3. Go to "SQL Editor" in the left sidebar
   4. Copy the contents of `backend/database/setup.sql`
   5. Paste it into the SQL editor and click "Run"

   **Option B: Using Supabase CLI**
   ```bash
   # Install Supabase CLI
   npm install -g supabase
   
   # Login to Supabase
   supabase login
   
   # Link to your project
   supabase link --project-ref nwtzhzagqfuedsljngkl
   
   # Apply the schema
   supabase db push
   ```

4. **Verify Setup**:
   ```bash
   python setup_database.py
   ```

5. **Start the Backend**:
   ```bash
   uvicorn server:app --reload
   ```

## 📱 Frontend Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Access the Dashboard**:
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 🔧 Features

### Security Features
- **Data Encryption**: All sensitive client data encrypted with AES-256
- **Secure Credentials**: University portal credentials stored with additional encryption
- **Privacy Protection**: Email hashing for privacy-compliant lookups

### Browser Automation
- **Anti-Detection**: Disabled webdriver flags, fake user agents, navigator spoofing
- **Human-like Behavior**: Random delays, realistic typing patterns, mouse movements
- **CAPTCHA Detection**: Framework for detecting and handling CAPTCHAs
- **Error Recovery**: Smart retry logic with exponential backoff

### Monitoring & Analytics
- **Real-time Tracking**: Application status and progress monitoring
- **Performance Metrics**: Success rates, response times, error tracking
- **Client Analytics**: Individual insights and deadline tracking
- **System Health**: Comprehensive monitoring and alerting

### Notifications
- **Email Alerts**: Application status updates and summaries
- **SMS Notifications**: Critical alerts via Twilio
- **Template System**: Customizable notification templates

## 🎯 Usage

### Creating a Client
1. Navigate to the dashboard
2. Click "Add New Client"
3. Fill in client information
4. Upload required documents
5. System automatically encrypts and stores data

### Managing Applications
1. Select a client from the dashboard
2. Choose target universities
3. Configure application preferences
4. Start automated application process
5. Monitor progress in real-time

### Analytics & Insights
1. Click on any client to view detailed analytics
2. Review application status and timeline
3. Check performance metrics and insights
4. Track important deadlines

## 🗄️ Database Schema

### Tables Created by Setup Script

- **clients**: Stores encrypted client information
- **application_tasks**: Tracks individual application submissions
- **mock_applications**: Testing and mock university data
- **application_status_log**: Audit trail of status changes
- **performance_metrics**: System performance and analytics

### Key Features of Schema
- UUID primary keys for all tables
- JSONB fields for flexible data storage
- Automatic timestamps with triggers
- Proper indexes for performance
- Foreign key relationships with cascade deletes

## 🔐 Security Considerations

1. **Environment Variables**: Never commit `.env` files with real credentials
2. **API Keys**: Use environment-specific keys (development vs production)
3. **Database Access**: Enable Row Level Security (RLS) for production
4. **Monitoring**: Set up logging and monitoring for security events
5. **Compliance**: Ensure all automation complies with website terms of service

## 🚀 Production Deployment

### Backend Deployment
1. Set up production environment variables
2. Enable RLS policies in Supabase
3. Configure proper CORS settings
4. Set up SSL/TLS certificates
5. Implement rate limiting

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Deploy to static hosting (Vercel, Netlify, etc.)
3. Configure environment-specific API endpoints
4. Set up proper redirects and error pages

## 🧪 Testing

Run the test suite:
```bash
cd backend
python test_enhanced_features.py
```

Test individual components:
```bash
# Test encryption
python -c "from security.encryption import DataEncryption; de = DataEncryption(); print('Encryption test passed')"

# Test database connection
python setup_database.py

# Test notifications
python -c "from notifications.notification_service import NotificationService; ns = NotificationService(); print('Notification service ready')"
```

## 📚 API Documentation

Once the server is running, visit:
- OpenAPI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc Documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with all applicable terms of service and regulations before use.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Review the API documentation
3. Check Supabase dashboard for database issues
4. Verify environment variables are correctly set

## 🔧 Troubleshooting

### Common Issues

**Database Connection Failed**
- Verify SUPABASE_URL and SUPABASE_KEY in .env file
- Check if tables are created (run setup.sql in Supabase dashboard)
- Ensure network connectivity to Supabase

**Browser Automation Errors**
- Install Playwright browsers: `playwright install`
- Check browser timeout settings
- Verify target website accessibility

**Notification Failures**
- Verify SMTP/Twilio credentials
- Check email/phone number formats
- Test with notification test endpoint

**Frontend Connection Issues**
- Verify backend is running on port 8000
- Check CORS configuration
- Ensure frontend is configured for correct API URL

---

**Remember**: This system is designed for educational purposes. Always respect website terms of service and applicable laws when using automation tools.
