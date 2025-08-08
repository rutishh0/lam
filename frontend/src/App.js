import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, Navigate } from 'react-router-dom';
import { 
  Bot, 
  Users, 
  FileText, 
  Settings, 
  Play, 
  Pause, 
  CheckCircle, 
  AlertCircle,
  Clock,
  University,
  Upload,
  Eye,
  Plus,
  Monitor,
  BarChart,
  Shield,
  Star,
  Check,
  Menu,
  X,
  ArrowRight,
  Zap,
  Globe,
  Smartphone,
  BookOpen,
  Award,
  TrendingUp,
  LogOut,
  Mail,
  Phone,
  MapPin,
  Calendar,
  DollarSign,
  Target,
  Briefcase,
  GraduationCap,
  Clock4,
  Database,
  Lock,
  MessageCircle,
  HeadphonesIcon,
  Download,
  ExternalLink,
  Heart,
  Share2,
  Bookmark,
  Filter,
  Search,
  Edit,
  Trash2,
  UserPlus,
  Bell,
  HelpCircle
} from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Analytics from './components/Analytics';
import DocumentUpload from './components/DocumentUpload';
import AdminPanel from './components/AdminPanel';
import AgentChat from './components/AgentChat';
import NewClientPage from './pages/NewClientPage';
import './App.css';



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

// Navigation Component
const Navigation = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    toast.success('Logged out successfully');
  };

  return (
    <nav className="bg-white shadow-lg fixed w-full z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                <Bot className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                UniAgent
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {!isAuthenticated ? (
              <>
                <Link to="/features" className="text-gray-700 hover:text-blue-600 transition-colors">
                  Features
                </Link>
                <Link to="/pricing" className="text-gray-700 hover:text-blue-600 transition-colors">
                  Pricing
                </Link>
                <Link to="/about" className="text-gray-700 hover:text-blue-600 transition-colors">
                  About
                </Link>
                <Link to="/contact" className="text-gray-700 hover:text-blue-600 transition-colors">
                  Contact
                </Link>
                <Link to="/signin" className="text-gray-700 hover:text-blue-600 transition-colors">
                  Sign In
                </Link>
                <Link 
                  to="/signup" 
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105"
                >
                  Get Started
                </Link>
              </>
            ) : (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
                  <Monitor className="h-4 w-4" />
                  <span>Dashboard</span>
                </Link>
                <Link to="/clients" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
                  <Users className="h-4 w-4" />
                  <span>Clients</span>
                </Link>
                <Link to="/applications" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
                  <FileText className="h-4 w-4" />
                  <span>Applications</span>
                </Link>
                {user?.role === 'admin' && (
                  <Link to="/admin" className="text-gray-700 hover:text-blue-600 flex items-center space-x-1">
                    <Shield className="h-4 w-4" />
                    <span>Admin</span>
                  </Link>
                )}
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user?.name?.charAt(0)?.toUpperCase() || 'U'}
                    </span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="text-gray-700 hover:text-red-600 flex items-center space-x-1"
                  >
                    <LogOut className="h-4 w-4" />
                    <span>Logout</span>
                  </button>
                </div>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-blue-600"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {isMenuOpen && (
          <div className="md:hidden absolute top-16 left-0 right-0 bg-white shadow-lg border-t">
            <div className="px-4 py-2 space-y-2">
              {!isAuthenticated ? (
                <>
                  <Link to="/features" className="block py-2 text-gray-700 hover:text-blue-600">Features</Link>
                  <Link to="/pricing" className="block py-2 text-gray-700 hover:text-blue-600">Pricing</Link>
                  <Link to="/about" className="block py-2 text-gray-700 hover:text-blue-600">About</Link>
                  <Link to="/contact" className="block py-2 text-gray-700 hover:text-blue-600">Contact</Link>
                  <Link to="/signin" className="block py-2 text-gray-700 hover:text-blue-600">Sign In</Link>
                  <Link to="/signup" className="block py-2 bg-blue-600 text-white rounded-lg text-center">Get Started</Link>
                </>
              ) : (
                <>
                  <Link to="/dashboard" className="block py-2 text-gray-700 hover:text-blue-600">Dashboard</Link>
                  <Link to="/clients" className="block py-2 text-gray-700 hover:text-blue-600">Clients</Link>
                  <Link to="/applications" className="block py-2 text-gray-700 hover:text-blue-600">Applications</Link>
                  {user?.role === 'admin' && (
                    <Link to="/admin" className="block py-2 text-gray-700 hover:text-blue-600">Admin</Link>
                  )}
                  <button onClick={handleLogout} className="block w-full text-left py-2 text-red-600 hover:text-red-700">
                    Logout
                  </button>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

// Landing Page Component
const LandingPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  const features = [
    {
      icon: <Bot className="h-8 w-8 text-blue-600" />,
      title: "AI-Powered Automation",
      description: "Advanced artificial intelligence handles your university applications with precision and speed"
    },
    {
      icon: <Shield className="h-8 w-8 text-green-600" />,
      title: "Secure & Compliant",
      description: "Bank-grade encryption and GDPR compliance ensure your data is always protected"
    },
    {
      icon: <Clock className="h-8 w-8 text-purple-600" />,
      title: "24/7 Monitoring",
      description: "Real-time tracking and status updates keep you informed throughout the process"
    },
    {
      icon: <University className="h-8 w-8 text-indigo-600" />,
      title: "Multi-University Support",
      description: "Apply to multiple UK universities simultaneously with automated form filling"
    },
    {
      icon: <BarChart className="h-8 w-8 text-orange-600" />,
      title: "Analytics Dashboard",
      description: "Detailed insights and success metrics to optimize your application strategy"
    },
    {
      icon: <Star className="h-8 w-8 text-yellow-600" />,
      title: "Success Optimization",
      description: "AI-driven recommendations to improve your application success rate"
    }
  ];

  const stats = [
    { number: "10,000+", label: "Applications Processed" },
    { number: "95%", label: "Success Rate" },
    { number: "150+", label: "Universities Supported" },
    { number: "24/7", label: "Support Available" }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      university: "Oxford University",
      quote: "UniAgent made my application process seamless. I got accepted to my dream university!",
      avatar: "SC"
    },
    {
      name: "James Wilson",
      university: "Cambridge University", 
      quote: "The AI automation saved me weeks of work. Highly recommend for any serious applicant.",
      avatar: "JW"
    },
    {
      name: "Priya Patel",
      university: "Imperial College London",
      quote: "Outstanding service! The real-time tracking kept me informed every step of the way.",
      avatar: "PP"
    }
  ];

  return (
    <div className="min-h-screen bg-white pt-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Automate Your UK University Applications
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              AI-powered automation for seamless university applications. Get accepted faster with intelligent form filling and real-time tracking.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button 
                onClick={() => navigate('/signup')}
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105 flex items-center justify-center space-x-2"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="h-5 w-5" />
              </button>
              <button 
                onClick={() => navigate('/features')}
                className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-all"
              >
                Learn More
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-blue-600 mb-2">{stat.number}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Success
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to automate and optimize your university applications
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Success Stories
            </h2>
            <p className="text-xl text-gray-600">
              See how students achieved their university dreams with UniAgent
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white p-8 rounded-xl shadow-lg">
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {testimonial.avatar}
                  </div>
                  <div className="ml-4">
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-gray-600 text-sm">{testimonial.university}</div>
                  </div>
                </div>
                <p className="text-gray-700 italic">"{testimonial.quote}"</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of students who have successfully automated their university applications
          </p>
          <button 
            onClick={() => navigate('/signup')}
            className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105"
          >
            Start Your Application Today
          </button>
        </div>
      </section>
    </div>
  );
};

// Features Page Component
const FeaturesPage = () => {
  const features = [
    {
      icon: <Bot className="h-12 w-12 text-blue-600" />,
      title: "Advanced AI Automation",
      description: "Our cutting-edge AI technology automatically fills out university application forms with unprecedented accuracy.",
      benefits: [
        "Intelligent form recognition and field mapping",
        "Context-aware data entry and validation",
        "Error detection and correction",
        "Multi-language support for international applications"
      ]
    },
    {
      icon: <Shield className="h-12 w-12 text-green-600" />,
      title: "Enterprise Security",
      description: "Bank-grade security measures protect your personal information and application data.",
      benefits: [
        "AES-256 bit encryption for data at rest",
        "TLS 1.3 for secure data transmission",
        "GDPR compliant data handling",
        "Regular security audits and penetration testing"
      ]
    },
    {
      icon: <University className="h-12 w-12 text-purple-600" />,
      title: "University Network",
      description: "Direct integration with 150+ UK universities and colleges for seamless applications.",
      benefits: [
        "UCAS integration for centralized applications",
        "Direct university portal connections",
        "Real-time application status updates",
        "Automated deadline tracking and reminders"
      ]
    },
    {
      icon: <BarChart className="h-12 w-12 text-orange-600" />,
      title: "Analytics Dashboard", 
      description: "Comprehensive insights and analytics to track your application progress and success rates.",
      benefits: [
        "Real-time application status monitoring",
        "Success rate predictions and optimization",
        "Detailed performance metrics",
        "Comparative analysis with similar profiles"
      ]
    },
    {
      icon: <Clock className="h-12 w-12 text-indigo-600" />,
      title: "24/7 Monitoring",
      description: "Continuous monitoring ensures your applications are processed without delays.",
      benefits: [
        "Automated retry mechanisms for failed submissions",
        "Instant notifications for status changes",
        "Proactive issue detection and resolution",
        "Global infrastructure for 99.9% uptime"
      ]
    },
    {
      icon: <Star className="h-12 w-12 text-yellow-600" />,
      title: "Success Optimization",
      description: "AI-driven recommendations to improve your chances of admission success.",
      benefits: [
        "Application strength analysis",
        "Personal statement optimization suggestions",
        "Course recommendation based on profile",
        "Interview preparation resources"
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Powerful Features</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Discover the comprehensive suite of tools and technologies that make UniAgent the most advanced university application platform
          </p>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {features.map((feature, index) => (
              <div key={index} className="bg-white rounded-xl shadow-lg p-8 hover:shadow-xl transition-shadow">
                <div className="flex items-start space-x-6">
                  <div className="flex-shrink-0">
                    {feature.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                    <p className="text-gray-600 mb-6">{feature.description}</p>
                    <ul className="space-y-2">
                      {feature.benefits.map((benefit, idx) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <Check className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700">{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Built with Modern Technology
            </h2>
            <p className="text-xl text-gray-600">
              Powered by cutting-edge technologies for reliability and performance
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { name: "React", description: "Modern Frontend Framework" },
              { name: "FastAPI", description: "High-Performance Backend" },
              { name: "Playwright", description: "Web Automation Engine" },
              { name: "MongoDB", description: "Flexible Database" },
              { name: "AWS", description: "Cloud Infrastructure" },
              { name: "Docker", description: "Containerization" },
              { name: "Redis", description: "Caching & Sessions" },
              { name: "Stripe", description: "Secure Payments" }
            ].map((tech, index) => (
              <div key={index} className="text-center p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
                <div className="text-lg font-semibold text-gray-900 mb-2">{tech.name}</div>
                <div className="text-sm text-gray-600">{tech.description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

// About Page Component  
const AboutPage = () => {
  const team = [
    {
      name: "Dr. Sarah Johnson",
      role: "CEO & Founder",
      bio: "Former Cambridge admissions officer with 15 years of experience in university applications",
      avatar: "SJ"
    },
    {
      name: "Michael Chen",
      role: "CTO",
      bio: "AI researcher and former Google engineer specializing in automation and machine learning",
      avatar: "MC"
    },
    {
      name: "Emma Williams",
      role: "Head of Education",
      bio: "Educational consultant with expertise in UK higher education and student success",
      avatar: "EW"
    },
    {
      name: "David Kumar",
      role: "Lead Developer",
      bio: "Full-stack developer with expertise in web automation and security systems",
      avatar: "DK"
    }
  ];

  const milestones = [
    { year: "2020", event: "Company founded with vision to democratize university applications" },
    { year: "2021", event: "First successful automated application to Oxford University" },
    { year: "2022", event: "Partnership with UCAS for direct integration" },
    { year: "2023", event: "Expanded to all 150+ UK universities and colleges" },
    { year: "2024", event: "10,000+ successful applications processed" }
  ];

  return (
    <div className="min-h-screen bg-white pt-16">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">About UniAgent</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            We're on a mission to make university applications accessible, efficient, and stress-free for students worldwide
          </p>
        </div>
      </section>

      {/* Mission */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">Our Mission</h2>
              <p className="text-lg text-gray-700 mb-6">
                At UniAgent, we believe that every student deserves equal access to higher education opportunities. 
                Traditional university application processes are often complex, time-consuming, and prone to errors 
                that can impact a student's future.
              </p>
              <p className="text-lg text-gray-700 mb-6">
                Our AI-powered platform eliminates these barriers by automating the application process while 
                maintaining the highest standards of accuracy and security. We're not just building software – 
                we're democratizing access to education.
              </p>
              <div className="flex space-x-8">
                <div>
                  <div className="text-2xl font-bold text-blue-600 mb-2">95%</div>
                  <div className="text-gray-600">Success Rate</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-600 mb-2">10,000+</div>
                  <div className="text-gray-600">Applications</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-blue-600 mb-2">150+</div>
                  <div className="text-gray-600">Universities</div>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-8 rounded-xl">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Our Values</h3>
              <ul className="space-y-4">
                <li className="flex items-start space-x-3">
                  <Check className="h-6 w-6 text-green-600 mt-0.5" />
                  <div>
                    <div className="font-semibold text-gray-900">Accessibility</div>
                    <div className="text-gray-700">Making university applications accessible to all students</div>
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <Check className="h-6 w-6 text-green-600 mt-0.5" />
                  <div>
                    <div className="font-semibold text-gray-900">Innovation</div>
                    <div className="text-gray-700">Leveraging cutting-edge technology for better outcomes</div>
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <Check className="h-6 w-6 text-green-600 mt-0.5" />
                  <div>
                    <div className="font-semibold text-gray-900">Integrity</div>
                    <div className="text-gray-700">Maintaining transparency and ethical practices</div>
                  </div>
                </li>
                <li className="flex items-start space-x-3">
                  <Check className="h-6 w-6 text-green-600 mt-0.5" />
                  <div>
                    <div className="font-semibold text-gray-900">Security</div>
                    <div className="text-gray-700">Protecting student data with enterprise-grade security</div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600">
              Experienced professionals dedicated to transforming university applications
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <div key={index} className="bg-white rounded-xl shadow-lg p-8 text-center">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  {member.avatar}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{member.name}</h3>
                <div className="text-blue-600 font-semibold mb-4">{member.role}</div>
                <p className="text-gray-600">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Our Journey</h2>
            <p className="text-xl text-gray-600">
              Key milestones in our mission to transform university applications
            </p>
          </div>
          <div className="space-y-8">
            {milestones.map((milestone, index) => (
              <div key={index} className="flex items-center space-x-8">
                <div className="w-24 h-24 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
                  {milestone.year}
                </div>
                <div className="flex-1 bg-white p-6 rounded-xl shadow-lg">
                  <p className="text-lg text-gray-700">{milestone.event}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

// Contact Page Component
const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    toast.success('Message sent successfully! We\'ll get back to you soon.');
    setFormData({ name: '', email: '', subject: '', message: '' });
    setLoading(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Contact Us</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Have questions about our services? We're here to help you succeed in your university applications
          </p>
        </div>
      </section>

      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
            {/* Contact Information */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-lg p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Get in Touch</h3>
                
                <div className="space-y-6">
                  <div className="flex items-start space-x-4">
                    <Mail className="h-6 w-6 text-blue-600 mt-1" />
                    <div>
                      <div className="font-semibold text-gray-900">Email</div>
                      <div className="text-gray-600">support@uniagent.com</div>
                      <div className="text-gray-600">hello@uniagent.com</div>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-4">
                    <Phone className="h-6 w-6 text-blue-600 mt-1" />
                    <div>
                      <div className="font-semibold text-gray-900">Phone</div>
                      <div className="text-gray-600">+44 (0) 20 7946 0958</div>
                      <div className="text-gray-600">Mon-Fri, 9 AM - 6 PM GMT</div>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-4">
                    <MapPin className="h-6 w-6 text-blue-600 mt-1" />
                    <div>
                      <div className="font-semibold text-gray-900">Address</div>
                      <div className="text-gray-600">
                        123 Education Street<br />
                        London, UK W1C 2AB
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-start space-x-4">
                    <Clock className="h-6 w-6 text-blue-600 mt-1" />
                    <div>
                      <div className="font-semibold text-gray-900">Support Hours</div>
                      <div className="text-gray-600">
                        Monday - Friday: 9 AM - 6 PM<br />
                        Saturday: 10 AM - 4 PM<br />
                        Sunday: Closed
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-8 pt-8 border-t border-gray-200">
                  <h4 className="font-semibold text-gray-900 mb-4">Quick Links</h4>
                  <div className="space-y-2">
                    <Link to="/help" className="block text-blue-600 hover:text-blue-700">Help Center</Link>
                    <Link to="/faq" className="block text-blue-600 hover:text-blue-700">FAQ</Link>
                    <Link to="/status" className="block text-blue-600 hover:text-blue-700">System Status</Link>
                    <a href="https://docs.uniagent.com" className="block text-blue-600 hover:text-blue-700">Documentation</a>
                  </div>
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-lg p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Send us a Message</h3>
                
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Full Name *
                      </label>
                      <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter your full name"
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
                        placeholder="Enter your email"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Subject *
                    </label>
                    <select
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Select a subject</option>
                      <option value="general">General Inquiry</option>
                      <option value="support">Technical Support</option>
                      <option value="billing">Billing Question</option>
                      <option value="partnership">Partnership Inquiry</option>
                      <option value="feedback">Feedback</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Message *
                    </label>
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      required
                      rows={6}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Tell us how we can help you..."
                    />
                  </div>
                  
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Sending...' : 'Send Message'}
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600">
              Quick answers to common questions about our services
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {[
              {
                question: "How does the automated application process work?",
                answer: "Our AI system securely accesses university portals, fills out applications using your provided information, and submits them according to your preferences and deadlines."
              },
              {
                question: "Is my personal data secure?",
                answer: "Yes, we use bank-grade encryption and follow GDPR compliance standards. Your data is encrypted both in transit and at rest, and we never share your information with third parties."
              },
              {
                question: "Which universities do you support?",
                answer: "We support 150+ UK universities and colleges, including all Russell Group institutions. We also integrate with UCAS for centralized applications."
              },
              {
                question: "How much does the service cost?",
                answer: "We offer flexible pricing plans starting from £29/month. Check our pricing page for detailed information about features included in each plan."
              },
              {
                question: "Can I track my application status?",
                answer: "Yes, our dashboard provides real-time tracking of all your applications, including submission status, university responses, and important deadlines."
              },
              {
                question: "What if an application fails to submit?",
                answer: "Our system has automated retry mechanisms and monitors all submissions. If an issue occurs, you'll be notified immediately and our support team will assist with manual submission if needed."
              }
            ].map((faq, index) => (
              <div key={index} className="bg-gray-50 p-6 rounded-xl">
                <h4 className="font-semibold text-gray-900 mb-3">{faq.question}</h4>
                <p className="text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

// Pricing Page Component
const PricingPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const plans = [
    {
      name: "Starter",
      price: "£29",
      period: "per month",
      description: "Perfect for students applying to 1-3 universities",
      features: [
        "Up to 3 university applications",
        "Basic automation features",
        "Email support",
        "Application tracking dashboard",
        "Document storage (500MB)",
        "Standard processing speed"
      ],
      recommended: false,
      cta: "Start Free Trial"
    },
    {
      name: "Professional",
      price: "£79",
      period: "per month", 
      description: "Ideal for students applying to multiple universities",
      features: [
        "Up to 10 university applications",
        "Advanced AI automation",
        "Priority email & chat support",
        "Real-time application monitoring",
        "Document storage (5GB)",
        "Faster processing speed",
        "Personal statement optimization",
        "Interview preparation resources"
      ],
      recommended: true,
      cta: "Start Free Trial"
    },
    {
      name: "Premium",
      price: "£149",
      period: "per month",
      description: "For students who want maximum support and features",
      features: [
        "Unlimited university applications",
        "Premium AI automation with custom logic",
        "24/7 priority support",
        "Advanced analytics and insights",
        "Unlimited document storage",
        "Fastest processing speed",
        "Dedicated account manager",
        "Custom application strategies",
        "Success guarantee program"
      ],
      recommended: false,
      cta: "Start Free Trial"
    }
  ];

  const faqs = [
    {
      question: "Is there a free trial?",
      answer: "Yes! We offer a 14-day free trial for all plans. No credit card required to start."
    },
    {
      question: "Can I change plans anytime?",
      answer: "Absolutely. You can upgrade or downgrade your plan at any time. Changes take effect immediately."
    },
    {
      question: "What payment methods do you accept?",
      answer: "We accept all major credit cards, PayPal, and bank transfers for annual plans."
    },
    {
      question: "Is there a setup fee?",
      answer: "No setup fees. You only pay for your chosen monthly or annual subscription."
    },
    {
      question: "Can I cancel anytime?",
      answer: "Yes, you can cancel your subscription at any time. No long-term contracts or cancellation fees."
    },
    {
      question: "Do you offer student discounts?",
      answer: "Yes! We offer a 20% student discount. Contact us with your student ID for verification."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Simple, Transparent Pricing</h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto mb-8">
            Choose the perfect plan for your university application needs. All plans include our core automation features.
          </p>
          <div className="inline-flex bg-white bg-opacity-20 rounded-lg p-1">
            <button className="px-6 py-2 rounded-md bg-white text-blue-600 font-semibold">
              Monthly
            </button>
            <button className="px-6 py-2 rounded-md text-white">
              Annual (Save 20%)
            </button>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <div 
                key={index} 
                className={`bg-white rounded-xl shadow-lg p-8 relative ${
                  plan.recommended ? 'ring-2 ring-blue-600 transform scale-105' : ''
                }`}
              >
                {plan.recommended && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                  <div className="flex items-center justify-center mb-2">
                    <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                    <span className="text-gray-600 ml-2">/{plan.period}</span>
                  </div>
                  <p className="text-gray-600">{plan.description}</p>
                </div>
                
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start space-x-3">
                      <Check className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <button
                  onClick={() => navigate(isAuthenticated ? '/dashboard' : '/signup')}
                  className={`w-full py-3 px-6 rounded-lg font-semibold transition-all ${
                    plan.recommended
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {plan.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Feature Comparison
            </h2>
            <p className="text-xl text-gray-600">
              See what's included in each plan
            </p>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Features</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900">Starter</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900">Professional</th>
                  <th className="text-center py-4 px-6 font-semibold text-gray-900">Premium</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {[
                  { feature: "University Applications", starter: "3", professional: "10", premium: "Unlimited" },
                  { feature: "AI Automation", starter: "Basic", professional: "Advanced", premium: "Premium" },
                  { feature: "Support", starter: "Email", professional: "Email & Chat", premium: "24/7 Priority" },
                  { feature: "Document Storage", starter: "500MB", professional: "5GB", premium: "Unlimited" },
                  { feature: "Processing Speed", starter: "Standard", professional: "Fast", premium: "Fastest" },
                  { feature: "Analytics", starter: "Basic", professional: "Advanced", premium: "Premium" },
                  { feature: "Account Manager", starter: false, professional: false, premium: true },
                  { feature: "Success Guarantee", starter: false, professional: false, premium: true }
                ].map((row, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="py-4 px-6 font-medium text-gray-900">{row.feature}</td>
                    <td className="py-4 px-6 text-center">
                      {typeof row.starter === 'boolean' ? (
                        row.starter ? <Check className="h-5 w-5 text-green-600 mx-auto" /> : <X className="h-5 w-5 text-gray-400 mx-auto" />
                      ) : (
                        <span className="text-gray-700">{row.starter}</span>
                      )}
                    </td>
                    <td className="py-4 px-6 text-center">
                      {typeof row.professional === 'boolean' ? (
                        row.professional ? <Check className="h-5 w-5 text-green-600 mx-auto" /> : <X className="h-5 w-5 text-gray-400 mx-auto" />
                      ) : (
                        <span className="text-gray-700">{row.professional}</span>
                      )}
                    </td>
                    <td className="py-4 px-6 text-center">
                      {typeof row.premium === 'boolean' ? (
                        row.premium ? <Check className="h-5 w-5 text-green-600 mx-auto" /> : <X className="h-5 w-5 text-gray-400 mx-auto" />
                      ) : (
                        <span className="text-gray-700">{row.premium}</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600">
              Got questions about pricing? We've got answers.
            </p>
          </div>
          
          <div className="space-y-8">
            {faqs.map((faq, index) => (
              <div key={index} className="bg-white rounded-xl shadow-lg p-8">
                <h4 className="text-xl font-semibold text-gray-900 mb-4">{faq.question}</h4>
                <p className="text-gray-600">{faq.answer}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Start Your Application Journey?
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of students who have successfully automated their university applications
          </p>
          <button 
            onClick={() => navigate('/signup')}
            className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-all transform hover:scale-105"
          >
            Start Free Trial Today
          </button>
        </div>
      </section>
    </div>
  );
};

// Sign Up Page Component
const SignUpPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false
  });
  const [loading, setLoading] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    if (!formData.acceptTerms) {
      toast.error('Please accept the terms and conditions');
      return;
    }

    setLoading(true);
    
    const result = await signup({
      name: formData.name,
      email: formData.email,
      password: formData.password
    });

    if (result.success) {
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } else {
      toast.error(result.error);
    }
    
    setLoading(false);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-lg inline-block mb-4">
            <Bot className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Create Your Account</h2>
          <p className="text-gray-600">Start your university application journey today</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your full name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Create a secure password"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Confirm your password"
              />
            </div>

            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                name="acceptTerms"
                checked={formData.acceptTerms}
                onChange={handleChange}
                required
                className="mt-1 h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              <label className="text-sm text-gray-700">
                I agree to the{' '}
                <Link to="/terms" className="text-blue-600 hover:text-blue-700">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link to="/privacy" className="text-blue-600 hover:text-blue-700">
                  Privacy Policy
                </Link>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link to="/signin" className="text-blue-600 hover:text-blue-700 font-semibold">
                Sign In
              </Link>
            </p>
          </div>
        </div>

        {/* Benefits */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Why Choose UniAgent?</h3>
          <ul className="space-y-3">
            <li className="flex items-center space-x-3">
              <Check className="h-5 w-5 text-green-600" />
              <span className="text-gray-700">14-day free trial</span>
            </li>
            <li className="flex items-center space-x-3">
              <Check className="h-5 w-5 text-green-600" />
              <span className="text-gray-700">95% application success rate</span>
            </li>
            <li className="flex items-center space-x-3">
              <Check className="h-5 w-5 text-green-600" />
              <span className="text-gray-700">24/7 customer support</span>
            </li>
            <li className="flex items-center space-x-3">
              <Check className="h-5 w-5 text-green-600" />
              <span className="text-gray-700">Bank-grade security</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

// Sign In Page Component
const SignInPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const result = await login(formData.email, formData.password);

    if (result.success) {
      toast.success('Welcome back!');
      navigate('/dashboard');
    } else {
      toast.error(result.error);
    }
    
    setLoading(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-16 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-lg inline-block mb-4">
            <Bot className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h2>
          <p className="text-gray-600">Sign in to your UniAgent account</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your password"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label className="ml-2 text-sm text-gray-700">
                  Remember me
                </label>
              </div>
              <Link to="/forgot-password" className="text-sm text-blue-600 hover:text-blue-700">
                Forgot password?
              </Link>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <Link to="/signup" className="text-blue-600 hover:text-blue-700 font-semibold">
                Sign Up
              </Link>
            </p>
          </div>
        </div>

        {/* Quick Demo */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Try Demo Account</h3>
          <p className="text-gray-600 mb-4">Explore all features with our demo account</p>
          <button
            onClick={() => {
              setFormData({ email: 'demo@uniagent.com', password: 'demo123' });
              toast.info('Demo credentials loaded. Click Sign In to continue.');
            }}
            className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Load Demo Credentials
          </button>
        </div>
      </div>
    </div>
  );
};

// Enhanced Dashboard Component
const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalClients: 0,
    activeApplications: 0,
    successfulApplications: 0,
    pendingApplications: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Simulate API calls
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setStats({
        totalClients: 12,
        activeApplications: 8,
        successfulApplications: 25,
        pendingApplications: 3
      });

      setRecentActivity([
        {
          id: 1,
          type: 'application_submitted',
          message: 'Application submitted to Oxford University',
          client: 'Sarah Johnson',
          timestamp: '2 hours ago',
          status: 'success'
        },
        {
          id: 2,
          type: 'client_added',
          message: 'New client added to the system',
          client: 'Michael Chen',
          timestamp: '4 hours ago',
          status: 'info'
        },
        {
          id: 3,
          type: 'application_accepted',
          message: 'Application accepted by Cambridge University',
          client: 'Emma Wilson',
          timestamp: '1 day ago',
          status: 'success'
        }
      ]);
    } catch (error) {
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pt-16 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's an overview of your university application automation system
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Total Clients</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalClients}</p>
              </div>
              <Users className="h-12 w-12 text-blue-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Active Applications</p>
                <p className="text-3xl font-bold text-gray-900">{stats.activeApplications}</p>
              </div>
              <Clock className="h-12 w-12 text-orange-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Successful</p>
                <p className="text-3xl font-bold text-gray-900">{stats.successfulApplications}</p>
              </div>
              <CheckCircle className="h-12 w-12 text-green-600" />
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">Pending Review</p>
                <p className="text-3xl font-bold text-gray-900">{stats.pendingApplications}</p>
              </div>
              <AlertCircle className="h-12 w-12 text-yellow-600" />
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Link
                  to="/clients/new"
                  className="flex items-center space-x-4 p-4 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg hover:from-blue-100 hover:to-blue-200 transition-colors"
                >
                  <UserPlus className="h-8 w-8 text-blue-600" />
                  <div>
                    <div className="font-semibold text-gray-900">Add New Client</div>
                    <div className="text-gray-600 text-sm">Register a new student</div>
                  </div>
                </Link>

                <Link
                  to="/applications/new"
                  className="flex items-center space-x-4 p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg hover:from-green-100 hover:to-green-200 transition-colors"
                >
                  <Plus className="h-8 w-8 text-green-600" />
                  <div>
                    <div className="font-semibold text-gray-900">Create Application</div>
                    <div className="text-gray-600 text-sm">Start new university application</div>
                  </div>
                </Link>

                <Link
                  to="/applications"
                  className="flex items-center space-x-4 p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg hover:from-purple-100 hover:to-purple-200 transition-colors"
                >
                  <Monitor className="h-8 w-8 text-purple-600" />
                  <div>
                    <div className="font-semibold text-gray-900">Monitor Applications</div>
                    <div className="text-gray-600 text-sm">Track application status</div>
                  </div>
                </Link>

                <Link
                  to="/analytics"
                  className="flex items-center space-x-4 p-4 bg-gradient-to-r from-orange-50 to-orange-100 rounded-lg hover:from-orange-100 hover:to-orange-200 transition-colors"
                >
                  <BarChart className="h-8 w-8 text-orange-600" />
                  <div>
                    <div className="font-semibold text-gray-900">View Analytics</div>
                    <div className="text-gray-600 text-sm">Performance insights</div>
                  </div>
                </Link>
              </div>
            </div>
          </div>

          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-6">System Status</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Automation Engine</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-600 text-sm">Online</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Database</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-600 text-sm">Connected</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Monitoring</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-600 text-sm">Active</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">API Services</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-600 text-sm">Healthy</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">Recent Activity</h3>
            <Link to="/activity" className="text-blue-600 hover:text-blue-700 flex items-center space-x-1">
              <span>View All</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                <div className={`w-3 h-3 rounded-full mt-2 ${
                  activity.status === 'success' ? 'bg-green-500' : 
                  activity.status === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                }`}></div>
                <div className="flex-1">
                  <p className="text-gray-900 font-medium">{activity.message}</p>
                  <p className="text-gray-600 text-sm">Client: {activity.client}</p>
                  <p className="text-gray-500 text-xs">{activity.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Clients Page Component
const ClientsPage = () => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setClients([
        {
          id: '1',
          name: 'Sarah Johnson',
          email: 'sarah.johnson@email.com',
          phone: '+44 7700 900123',
          status: 'active',
          applications: 3,
          successRate: 100,
          createdAt: '2024-01-15',
          lastActivity: '2 hours ago'
        },
        {
          id: '2',
          name: 'Michael Chen',
          email: 'michael.chen@email.com',
          phone: '+44 7700 900124',
          status: 'pending',
          applications: 1,
          successRate: 0,
          createdAt: '2024-01-20',
          lastActivity: '1 day ago'
        },
        {
          id: '3',
          name: 'Emma Wilson',
          email: 'emma.wilson@email.com',
          phone: '+44 7700 900125',
          status: 'active',
          applications: 5,
          successRate: 80,
          createdAt: '2024-01-10',
          lastActivity: '3 hours ago'
        }
      ]);
    } catch (error) {
      toast.error('Failed to load clients');
    } finally {
      setLoading(false);
    }
  };

  const filteredClients = clients.filter(client => {
    const matchesSearch = client.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         client.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || client.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pt-16 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading clients...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Clients</h1>
              <p className="text-gray-600 mt-2">Manage your student clients and their applications</p>
            </div>
            <Link
              to="/clients/new"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all flex items-center space-x-2"
            >
              <Plus className="h-5 w-5" />
              <span>Add Client</span>
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search clients..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="pending">Pending</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-gray-600">Total: {filteredClients.length} clients</span>
            </div>
          </div>
        </div>

        {/* Clients Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredClients.map((client) => (
            <div key={client.id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {client.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{client.name}</h3>
                    <p className="text-gray-600 text-sm">{client.email}</p>
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  client.status === 'active' ? 'bg-green-100 text-green-800' :
                  client.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {client.status}
                </div>
              </div>

              <div className="space-y-3 mb-6">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Applications</span>
                  <span className="font-semibold text-gray-900">{client.applications}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Success Rate</span>
                  <span className="font-semibold text-gray-900">{client.successRate}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Last Activity</span>
                  <span className="text-gray-900">{client.lastActivity}</span>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Link
                  to={`/clients/${client.id}`}
                  className="flex-1 bg-blue-50 text-blue-600 py-2 px-4 rounded-lg text-center hover:bg-blue-100 transition-colors flex items-center justify-center space-x-1"
                >
                  <Eye className="h-4 w-4" />
                  <span>View</span>
                </Link>
                <Link
                  to={`/clients/${client.id}/edit`}
                  className="bg-gray-50 text-gray-600 py-2 px-4 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <Edit className="h-4 w-4" />
                </Link>
                <button className="bg-red-50 text-red-600 py-2 px-4 rounded-lg hover:bg-red-100 transition-colors">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredClients.length === 0 && (
          <div className="text-center py-12">
            <Users className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No clients found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm || filterStatus !== 'all' 
                ? 'Try adjusting your search or filters'
                : 'Get started by adding your first client'
              }
            </p>
            {!searchTerm && filterStatus === 'all' && (
              <Link
                to="/clients/new"
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all inline-flex items-center space-x-2"
              >
                <Plus className="h-5 w-5" />
                <span>Add Your First Client</span>
              </Link>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// Applications Page Component
const ApplicationsPage = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setApplications([
        {
          id: '1',
          clientName: 'Sarah Johnson',
          university: 'University of Oxford',
          course: 'Computer Science',
          status: 'submitted',
          submittedAt: '2024-01-15',
          deadline: '2024-02-01',
          progress: 100
        },
        {
          id: '2',
          clientName: 'Michael Chen',
          university: 'University of Cambridge',
          course: 'Engineering',
          status: 'in_progress',
          submittedAt: null,
          deadline: '2024-02-15',
          progress: 60
        },
        {
          id: '3',
          clientName: 'Emma Wilson',
          university: 'Imperial College London',
          course: 'Medicine',
          status: 'accepted',
          submittedAt: '2024-01-10',
          deadline: '2024-01-31',
          progress: 100
        }
      ]);
    } catch (error) {
      toast.error('Failed to load applications');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'accepted': return 'bg-green-100 text-green-800';
      case 'submitted': return 'bg-blue-100 text-blue-800';
      case 'in_progress': return 'bg-yellow-100 text-yellow-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pt-16 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading applications...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Applications</h1>
              <p className="text-gray-600 mt-2">Track and manage university applications</p>
            </div>
            <Link
              to="/applications/new"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all flex items-center space-x-2"
            >
              <Plus className="h-5 w-5" />
              <span>New Application</span>
            </Link>
          </div>
        </div>

        {/* Applications Table */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Client</th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">University</th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Course</th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Status</th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Progress</th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Deadline</th>
                  <th className="text-left py-4 px-6 font-semibold text-gray-900">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {applications.map((application) => (
                  <tr key={application.id} className="hover:bg-gray-50">
                    <td className="py-4 px-6">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                          {application.clientName.split(' ').map(n => n[0]).join('')}
                        </div>
                        <span className="font-medium text-gray-900">{application.clientName}</span>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-gray-900">{application.university}</td>
                    <td className="py-4 px-6 text-gray-900">{application.course}</td>
                    <td className="py-4 px-6">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(application.status)}`}>
                        {application.status.replace('_', ' ').toUpperCase()}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center space-x-2">
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${application.progress}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-600">{application.progress}%</span>
                      </div>
                    </td>
                    <td className="py-4 px-6 text-gray-900">{application.deadline}</td>
                    <td className="py-4 px-6">
                      <div className="flex items-center space-x-2">
                        <Link
                          to={`/applications/${application.id}`}
                          className="bg-blue-50 text-blue-600 py-1 px-3 rounded hover:bg-blue-100 transition-colors"
                        >
                          <Eye className="h-4 w-4" />
                        </Link>
                        <button className="bg-gray-50 text-gray-600 py-1 px-3 rounded hover:bg-gray-100 transition-colors">
                          <Edit className="h-4 w-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {applications.length === 0 && (
          <div className="text-center py-12">
            <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No applications yet</h3>
            <p className="text-gray-600 mb-6">Start by creating your first university application</p>
            <Link
              to="/applications/new"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all inline-flex items-center space-x-2"
            >
              <Plus className="h-5 w-5" />
              <span>Create First Application</span>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <BrowserRouter>
          <Navigation />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/features" element={<FeaturesPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/pricing" element={<PricingPage />} />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/signin" element={<SignInPage />} />
            <Route 
              path="/dashboard/chat" 
              element={
                <ProtectedRoute>
                  <div className="min-h-screen bg-gray-50 pt-16">
                    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                      <AgentChat token={localStorage.getItem('token') || ''} />
                    </div>
                  </div>
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/clients" 
              element={
                <ProtectedRoute>
                  <ClientsPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/clients/new" 
              element={
                <ProtectedRoute>
                  <NewClientPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/applications" 
              element={
                <ProtectedRoute>
                  <ApplicationsPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/admin" 
              element={
                <ProtectedRoute adminOnly>
                  <AdminPanel />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" />
      </div>
    </AuthProvider>
  );
}

export default App;
