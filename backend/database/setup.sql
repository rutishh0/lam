-- Autonomous University Application Agent - SaaS Database Setup
-- This script creates all necessary tables for the SaaS application

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users table - stores user accounts with authentication
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'customer' CHECK (role IN ('admin', 'customer')),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    email_verification_token VARCHAR(255),
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP WITH TIME ZONE,
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
    limits JSONB DEFAULT '{}'::jsonb, -- e.g., {"max_applications": 5, "max_universities": 10}
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
    stripe_subscription_id VARCHAR(255) UNIQUE,
    stripe_customer_id VARCHAR(255),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    trial_start TIMESTAMP WITH TIME ZONE,
    trial_end TIMESTAMP WITH TIME ZONE,
    cancelled_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Billing history table
CREATE TABLE IF NOT EXISTS billing_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES user_subscriptions(id),
    stripe_invoice_id VARCHAR(255),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'GBP',
    status VARCHAR(50) NOT NULL, -- paid, pending, failed, etc.
    description TEXT,
    invoice_url TEXT,
    invoice_pdf TEXT,
    billing_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Usage tracking table
CREATE TABLE IF NOT EXISTS usage_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resource_type VARCHAR(100) NOT NULL, -- 'application', 'university', 'document_upload', etc.
    resource_id UUID,
    usage_count INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}'::jsonb,
    usage_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Create unique constraint to prevent duplicate counting per day
    UNIQUE(user_id, resource_type, resource_id, usage_date)
);

-- Clients table - modified to be owned by users
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

-- Application tasks table - tracks application submissions (modified)
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
    progress_percentage INTEGER DEFAULT 0,
    estimated_completion TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_checked TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Mock applications table - for testing university portals (modified)
CREATE TABLE IF NOT EXISTS mock_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    university_code VARCHAR(20) NOT NULL,
    university_name VARCHAR(255) NOT NULL,
    application_data JSONB NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processing_time_seconds INTEGER,
    status VARCHAR(50) DEFAULT 'submitted',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Application status log - audit trail (modified)
CREATE TABLE IF NOT EXISTS application_status_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    application_id UUID REFERENCES application_tasks(id) ON DELETE CASCADE,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by VARCHAR(100) DEFAULT 'system',
    change_reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance metrics table (modified)
CREATE TABLE IF NOT EXISTS performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    metric_type VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    metric_unit VARCHAR(50),
    dimensions JSONB DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API usage logs table
CREATE TABLE IF NOT EXISTS api_usage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    ip_address INET,
    user_agent TEXT,
    request_size INTEGER,
    response_size INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Webhooks table for handling Stripe events
CREATE TABLE IF NOT EXISTS webhooks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    webhook_type VARCHAR(100) NOT NULL, -- 'stripe', 'payment', etc.
    event_type VARCHAR(255) NOT NULL,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(100) NOT NULL, -- 'email', 'sms', 'in_app'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    read BOOLEAN DEFAULT false,
    sent BOOLEAN DEFAULT false,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit logs table for compliance and security
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status ON user_subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_billing_history_user_id ON billing_history(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_id ON usage_tracking(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_date ON usage_tracking(usage_date);
CREATE INDEX IF NOT EXISTS idx_clients_user_id ON clients(user_id);
CREATE INDEX IF NOT EXISTS idx_application_tasks_user_id ON application_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_application_tasks_status ON application_tasks(status);
CREATE INDEX IF NOT EXISTS idx_application_status_log_application_id ON application_status_log(application_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_user_id ON performance_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_recorded_at ON performance_metrics(recorded_at);
CREATE INDEX IF NOT EXISTS idx_api_usage_logs_user_id ON api_usage_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_logs_created_at ON api_usage_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_subscription_plans_updated_at BEFORE UPDATE ON subscription_plans FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_user_subscriptions_updated_at BEFORE UPDATE ON user_subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_application_tasks_updated_at BEFORE UPDATE ON application_tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default subscription plans
INSERT INTO subscription_plans (name, slug, description, price_monthly, price_yearly, features, limits) VALUES
('Starter', 'starter', 'Perfect for students applying to a few universities', 29.00, 290.00, 
 '["Up to 5 university applications", "Basic automation features", "Email support", "Application tracking", "Document storage"]'::jsonb,
 '{"max_applications": 5, "max_universities": 10, "max_documents": 10}'::jsonb),
 
('Professional', 'professional', 'Ideal for students applying to multiple universities', 79.00, 790.00,
 '["Up to 20 university applications", "Advanced AI automation", "Priority support", "Advanced analytics", "Custom personal statements", "UCAS integration", "SMS notifications"]'::jsonb,
 '{"max_applications": 20, "max_universities": 50, "max_documents": 50, "sms_notifications": true}'::jsonb),
 
('Enterprise', 'enterprise', 'For education consultants and agencies', 199.00, 1990.00,
 '["Unlimited applications", "White-label solution", "24/7 phone support", "Custom integrations", "Dedicated account manager", "Bulk client management", "Advanced reporting", "API access"]'::jsonb,
 '{"max_applications": -1, "max_universities": -1, "max_documents": -1, "api_access": true, "white_label": true}'::jsonb)
ON CONFLICT (slug) DO NOTHING;

-- Create admin user (password: 'admin123' - change this in production!)
INSERT INTO users (email, password_hash, name, role, email_verified) VALUES 
('admin@uniagent.com', crypt('admin123', gen_salt('bf')), 'System Administrator', 'admin', true)
ON CONFLICT (email) DO NOTHING;

-- Enable Row Level Security (RLS) for multi-tenancy
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE mock_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_status_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE billing_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for user data isolation
CREATE POLICY user_clients_policy ON clients FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_applications_policy ON application_tasks FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_mock_applications_policy ON mock_applications FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_status_log_policy ON application_status_log FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_metrics_policy ON performance_metrics FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_usage_policy ON usage_tracking FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_billing_policy ON billing_history FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);
CREATE POLICY user_notifications_policy ON notifications FOR ALL USING (user_id = current_setting('app.current_user_id')::uuid);

-- Add sample data for testing (optional)
-- This will be populated by the application setup

COMMENT ON TABLE users IS 'User accounts with authentication and authorization';
COMMENT ON TABLE subscription_plans IS 'Available subscription plans and pricing';
COMMENT ON TABLE user_subscriptions IS 'User subscription status and billing information';
COMMENT ON TABLE billing_history IS 'Payment and billing transaction history';
COMMENT ON TABLE usage_tracking IS 'Track user resource usage for billing and limits';
COMMENT ON TABLE clients IS 'Client information for university applications (now user-owned)';
COMMENT ON TABLE application_tasks IS 'Individual application submissions and their status (now user-owned)';
COMMENT ON TABLE mock_applications IS 'Mock university application data for testing (now user-owned)';
COMMENT ON TABLE application_status_log IS 'Audit log of application status changes (now user-owned)';
COMMENT ON TABLE performance_metrics IS 'System performance and analytics metrics (now user-owned)';
COMMENT ON TABLE api_usage_logs IS 'API endpoint usage logs for monitoring and rate limiting';
COMMENT ON TABLE webhooks IS 'Webhook events from external services like Stripe';
COMMENT ON TABLE notifications IS 'User notifications (email, SMS, in-app)';
COMMENT ON TABLE audit_logs IS 'Security and compliance audit trail'; 