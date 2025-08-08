# 🤖 AI LAM - The Autonomous University Application Agent

AI LAM is a sophisticated SaaS platform designed to automate the tedious and time-consuming process of filling out university applications. Leveraging a powerful Large Action Model (LAM), this system can intelligently parse user-provided documents and autonomously navigate complex web forms, providing a seamless and efficient experience for students and educational consultants.

**LEGAL DISCLAIMER**: This project is for educational and research purposes. Automated submissions may violate the Terms of Service of university application portals like UCAS. Users must ensure compliance before use.

## ✨ Core Features

- **Autonomous Web Automation**: The LAM backend uses Playwright to intelligently identify and fill form fields, handle multi-step processes, and manage complex UI interactions.
- **Multi-Source Data Entry**: Users can provide their information in various formats (CSV, PDF, DOC, TXT, MD), and the system will parse and utilize it for form filling.
- **Real-time Browser Streaming**: Customers can watch the Playwright browser session live in their dashboard, seeing the automation happen in real-time.
- **SaaS-Ready Architecture**: Built with a multi-tenant architecture, ready for subscription-based access, with user authentication and role-based permissions.
- **Modern & Sleek UI**: The frontend is designed to be beautiful, futuristic, and intuitive, inspired by modern platforms like OpenAI, Adaline, and Reflect.

## 🏗️ System Architecture

AI LAM is built with a modern, scalable, and secure architecture designed for a production-ready SaaS application.

- **Frontend**: A sleek **React 18** application built with **Tailwind CSS** for a futuristic UI. Deployed on **Vercel** for a fast, global CDN.
- **Backend**: A high-performance **FastAPI** (Python 3.11+) server that orchestrates the automation tasks. Can be deployed on **Koyeb**, **Railway**, or **Cloud Run**.
- **Database & Authentication**: **Supabase** (PostgreSQL) provides a robust database, user authentication, and real-time capabilities.
- **Automation Engine**: The core of the system is a powerful **Playwright** engine that runs headless browser sessions in a custom VM environment.
- **Real-time Streaming**: WebSockets are used to stream the live browser session from the backend to the customer's dashboard.

## 📋 Getting Started

### 1. Database Setup (Supabase)

- **Create a Supabase Project**: Go to the [Supabase Dashboard](https://supabase.com/dashboard) and create a new project.
- **Run the Schema**: In the SQL Editor, copy and paste the contents of `backend/database/setup.sql` to create all the necessary tables for users, subscriptions, and applications.

### 2. Environment Setup

- Create a `.env` file in the `backend` directory (use `ENV_SETUP.md` as a template).
- Create a `.env` file in the `frontend` directory (use `ENV_SETUP.md` as a template).
- Add your Supabase keys, generate JWT secrets, and configure any other services.

### 3. Running Locally

**Start the Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload
```

**Start the Frontend:**
```bash
cd frontend
npm install
npm start
```

Your application will be available at `http://localhost:3000`.

### 4. Deployment

- **One-container (Koyeb)**: Build the included multi-stage Dockerfile in `backend/`. This serves the React build via FastAPI and runs the API.
  - Set secrets in Koyeb (e.g., `SUPABASE_URL`, `SUPABASE_KEY`, `GOOGLE_API_KEY`, `JWT_SECRET`).
  - Exposed port is `8080`.
- **Split deploy**: Backend to Railway/Cloud Run using `backend/Dockerfile`, frontend to Vercel using `frontend/vercel.json`.

## 🔧 Technologies Used

- **React**: For building a modern and interactive user interface.
- **FastAPI**: A high-performance Python framework for the backend API.
- **Supabase**: For a scalable PostgreSQL database and user authentication.
- **Playwright**: For robust and intelligent browser automation.
- **Stripe**: Ready for integration for subscription management.
- **Docker**: For containerizing the backend for consistent deployments.
- **GitHub Actions**: For a full CI/CD pipeline.

## 🎯 What The System Can Do

- **For Customers**:
  - Sign up for a subscription plan.
  - Upload their personal and academic information in various document formats.
  - Specify the universities they want to apply to.
  - Watch in real-time as the AI LAM fills out their applications.
  - Track the status of all their applications in a beautiful dashboard.

- **For Admins**:
  - A comprehensive admin panel to manage users, subscriptions, and monitor system health.
  - Analytics on application success rates and system performance.
  - The ability to intervene or assist with customer applications if needed.

## 🚀 Future Vision

- **Enhanced AI Capabilities**: Integrate more advanced AI models for parsing complex documents and handling dynamic web forms.
- **Stripe Integration**: Complete the subscription and payment system with Stripe.
- **Expanded University Support**: Add more university application portals to the automation engine.
- **White-Label Solution**: Offer a white-label version for educational consultants and agencies.

## 🤝 Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Make your changes and submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

This project was built with the assistance of an AI pair programmer and inspired by the vision of a truly autonomous web agent. It utilizes a powerful stack of open-source technologies.
