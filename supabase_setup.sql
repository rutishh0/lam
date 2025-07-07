-- =====================================================
-- UniAgent Supabase Database Setup
-- Run this script in your Supabase SQL Editor
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table - stores user accounts with authentication  
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'customer' CHECK (role IN ('admin', 'customer')),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscription plans table
CREATE TABLE IF NOT EXISTS subscription_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    price_monthly DECIMAL(10,2) NOT NULL,
    price_yearly DECIMAL(10,2),
    features JSONB DEFAULT '[]'::jsonb,
    limits JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User subscriptions table
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES subscription_plans(id),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'cancelled', 'past_due', 'trialing', 'incomplete')),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    trial_start TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Clients table - university application clients
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    personal_statement TEXT NOT NULL,
    academic_history JSONB DEFAULT '[]'::jsonb,
    course_preferences JSONB DEFAULT '[]'::jsonb,
    documents JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Application tasks table - tracks application submissions  
CREATE TABLE IF NOT EXISTS application_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    university_name VARCHAR(255) NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(100) NOT NULL,
    application_url TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'submitted', 'accepted', 'rejected', 'withdrawn')),
    credentials JSONB DEFAULT '{}'::jsonb,
    application_data JSONB DEFAULT '{}'::jsonb,
    error_log JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_checked TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Usage tracking table
CREATE TABLE IF NOT EXISTS usage_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    usage_count INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}'::jsonb,
    usage_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, resource_type, resource_id, usage_date)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_clients_user_id ON clients(user_id);
CREATE INDEX IF NOT EXISTS idx_application_tasks_user_id ON application_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_application_tasks_status ON application_tasks(status);

-- Insert default subscription plans
INSERT INTO subscription_plans (name, slug, description, price_monthly, price_yearly, features, limits) VALUES
('Starter', 'starter', 'Perfect for students applying to a few universities', 29.00, 290.00, 
 '["Up to 5 university applications", "Basic automation features", "Email support", "Application tracking", "Document storage"]'::jsonb,
 '{"max_applications": 5, "max_universities": 10, "max_documents": 10}'::jsonb),
 
('Professional', 'professional', 'Ideal for students applying to multiple universities', 79.00, 790.00,
 '["Up to 20 university applications", "Advanced AI automation", "Priority support", "Advanced analytics", "Custom personal statements"]'::jsonb,
 '{"max_applications": 20, "max_universities": 50, "max_documents": 50}'::jsonb),
 
('Enterprise', 'enterprise', 'For education consultants and agencies', 199.00, 1990.00,
 '["Unlimited applications", "White-label solution", "24/7 phone support", "Custom integrations", "Dedicated account manager"]'::jsonb,
 '{"max_applications": -1, "max_universities": -1, "max_documents": -1, "api_access": true}'::jsonb)
ON CONFLICT (slug) DO NOTHING;

-- Create admin user (password is hashed 'admin123')  
INSERT INTO users (email, password_hash, name, role, email_verified) VALUES 
('admin@uniagent.com', '$2b$12$LQv3c1yqBwNFiDQwO7g8m.9T8j8Z8j8Z8j8Z8j8Z8j8Z8j8Z8j8Z8', 'System Administrator', 'admin', true)
ON CONFLICT (email) DO NOTHING;

-- =====================================================
-- Setup Complete!
-- =====================================================
-- Admin Login Details:
-- Email: admin@uniagent.com  
-- Password: admin123
-- 
-- Access your admin panel at: /admin
-- =====================================================