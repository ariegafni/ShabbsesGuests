-- Database schema for ShabbesGuests application

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    profile_image TEXT,
    bio TEXT,
    social_links JSONB,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for email lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index for created_at for sorting
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Countries table
CREATE TABLE IF NOT EXISTS countries (
    country_place_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hosts table
CREATE TABLE IF NOT EXISTS hosts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    country_place_id VARCHAR(255) NOT NULL REFERENCES countries(country_place_id),
    city_place_id VARCHAR(255) NOT NULL,
    area VARCHAR(255),
    address TEXT,
    description TEXT,
    bio TEXT,
    max_guests INTEGER NOT NULL,
    hosting_type TEXT[] DEFAULT '{}',
    kashrut_level VARCHAR(50),
    languages TEXT[] DEFAULT '{}',
    total_hostings INTEGER DEFAULT 0,
    is_always_available BOOLEAN DEFAULT FALSE,
    available BOOLEAN,
    photo_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for hosts table
CREATE INDEX IF NOT EXISTS idx_hosts_user_id ON hosts(user_id);
CREATE INDEX IF NOT EXISTS idx_hosts_country ON hosts(country_place_id);
CREATE INDEX IF NOT EXISTS idx_hosts_created_at ON hosts(created_at);

-- Trigger to automatically update hosts updated_at
CREATE TRIGGER update_hosts_updated_at 
    BEFORE UPDATE ON hosts 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Accommodation requests table
CREATE TABLE IF NOT EXISTS accommodation_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    host_id UUID NOT NULL REFERENCES hosts(id) ON DELETE CASCADE,
    request_date DATE NOT NULL,
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'cancelled', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for accommodation_requests table
CREATE INDEX IF NOT EXISTS idx_accommodation_requests_guest_id ON accommodation_requests(guest_id);
CREATE INDEX IF NOT EXISTS idx_accommodation_requests_host_id ON accommodation_requests(host_id);
CREATE INDEX IF NOT EXISTS idx_accommodation_requests_status ON accommodation_requests(status);
CREATE INDEX IF NOT EXISTS idx_accommodation_requests_created_at ON accommodation_requests(created_at);

-- Trigger to automatically update accommodation_requests updated_at
CREATE TRIGGER update_accommodation_requests_updated_at 
    BEFORE UPDATE ON accommodation_requests 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
