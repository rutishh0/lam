# 🚀 **Running the Autonomous University Application System Locally**

Here's a comprehensive guide to set up and run this project on your local laptop after cloning the repository.

## 📋 **Prerequisites**

### **Required Software:**
```bash
# 1. Python 3.11+ 
python --version  # Should be 3.11 or higher

# 2. Node.js 18+ and npm/yarn
node --version    # Should be 18 or higher
npm --version     # Or yarn --version

# 3. Git
git --version
```

**Installation Links:**
- **Python**: https://python.org/downloads/
- **Node.js**: https://nodejs.org/
- **Git**: https://git-scm.com/downloads

---

## 📁 **Step 1: Clone and Setup**

```bash
# Clone your repository
git clone <your-repo-url>
cd <your-repo-name>

# Verify project structure
ls -la
# Should show: backend/, frontend/, README.md, etc.
```

---

## 🐍 **Step 2: Backend Setup**

### **Create Virtual Environment:**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate


# Verify activation (should show (venv) in prompt)
```

### **Install Dependencies:**
```bash
# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```


## ⚛️ **Step 3: Frontend Setup**

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies using npm
npm install


# Should show: REACT_APP_BACKEND_URL=http://localhost:8001
```

---


## 🏃‍♂️ **Step 4: Running the Application**

### **Terminal 1: Start Backend**
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows

# Start FastAPI server
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# You should see:
# INFO: Uvicorn running on http://0.0.0.0:8001
```

### **Terminal 2: Start Frontend**
```bash
# Navigate to frontend directory
cd frontend

# Start React development server
npm start

# Browser should automatically open http://localhost:3000
```

---

## ✅ **Step 6: Verify Installation**

### **Backend Health Check:**
```bash
# Test API health
curl http://localhost:8001/health

# Expected response:
# {"status":"healthy","timestamp":"2024-...","services":{"database":"connected","api":"running"}}
```

### **Frontend Access:**
- Open browser to http://localhost:3000
- You should see the admin dashboard
- Test navigation between different sections

### **API Documentation:**
- Visit http://localhost:8001/docs for interactive API documentation

---

## 🔧 **Development Workflow**

### **Making Changes:**
```bash
# Backend changes auto-reload with --reload flag
# Frontend changes auto-reload with yarn start

# To restart backend:
# Ctrl+C to stop, then run uvicorn command again

# To restart frontend:
# Ctrl+C to stop, then yarn start again
```

### **Installing New Dependencies:**
```bash
# Backend:
cd backend
pip install new-package
pip freeze > requirements.txt

# Frontend:
cd frontend
npm add new-package
# or npm install new-package
```

---

## 🔍 **Troubleshooting**

### **Common Issues:**

**1. Port Already in Use:**
```bash
# Backend port 8001 busy:
lsof -ti:8001 | xargs kill -9

# Frontend port 3000 busy:
lsof -ti:3000 | xargs kill -9
```

**2. Python Virtual Environment Issues:**
```bash
# Recreate virtual environment:
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Node Modules Issues:**
```bash
# Clear and reinstall:
rm -rf node_modules package-lock.json yarn.lock
npm install
```

**4. FastAPI Middleware Error:**
```bash
# If you get middleware errors, ensure FastAPI version:
pip install fastapi==0.100.0
```

**5. Database Connection Issues:**
```bash
# Check Supabase credentials in .env
# Verify network connectivity
# Check Supabase dashboard for project status
```

### **Checking Logs:**
```bash
# Backend logs appear in terminal
# Frontend logs appear in browser console (F12)

# For detailed debugging:
# Set LOG_LEVEL=DEBUG in backend/.env
```

---

## 🎯 **Quick Start Commands**

**Complete setup in one go:**
```bash
# 1. Clone and setup
git clone <your-repo-url>
cd <your-repo-name>

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
playwright install

# Edit .env with your settings

# 3. Frontend setup  
cd ../frontend
npm install

# 4. Run (in separate terminals)
# Terminal 1:
cd backend && source venv/bin/activate && uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 2:
cd frontend && npm start
```

---

## 🚀 **Production Deployment**

For production deployment, refer to:
- `DEPLOYMENT.md` - General deployment guide
- `VERCEL_SETUP.md` - Frontend deployment to Vercel
- `SUPABASE_SETUP.md` - Database setup details

---

**🎉 You're all set! Your Autonomous University Application System should now be running locally.**

**Access URLs:**
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

Need help with any specific step? Let me know!
