-- Create database
CREATE DATABASE IF NOT EXISTS resume_analyzer;
USE resume_analyzer;

-- Users/Candidates table
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    
    -- Resume metadata
    resume_path VARCHAR(500),
    num_pages INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- ML Predictions
    predicted_field VARCHAR(100),
    field_confidence DECIMAL(5,2),
    experience_level VARCHAR(50),
    
    -- Quality Scores
    overall_quality_score DECIMAL(5,2),
    content_quality_score DECIMAL(5,2),
    structure_score DECIMAL(5,2),
    skill_relevance_score DECIMAL(5,2),
    
    -- Extracted data (JSON)
    skills JSON,
    companies JSON,
    education JSON,
    certifications JSON,
    projects JSON,
    
    -- Analysis results (JSON)
    swot_analysis JSON,
    recommendations JSON,
    
    INDEX idx_email (email),
    INDEX idx_field (predicted_field),
    INDEX idx_uploaded (uploaded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Skills table (for analytics)
CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(100),
    frequency INT DEFAULT 0,
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job postings table
CREATE TABLE job_postings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    description TEXT,
    required_skills JSON,
    required_experience INT,
    location VARCHAR(255),
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_company (company),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job matches table
CREATE TABLE job_matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    job_id INT,
    match_score DECIMAL(5,2),
    skill_match_percentage DECIMAL(5,2),
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    INDEX idx_match_score (match_score),
    INDEX idx_candidate (candidate_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Admin users table
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert default admin (password: admin123 - change this!)
INSERT INTO admin_users (username, password_hash, email) 
VALUES ('admin', SHA2('admin123', 256), 'admin@resumeanalyzer.com');