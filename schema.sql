-- FUNDING FINDER DATABASE SCHEMA
-- Built by Jennifer Leigh West
-- Leverages patterns from Alexandria (governance tracking) + MAAT (evidence documentation)

-- =============================================================================
-- USERS & PROFILES
-- =============================================================================

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    subscription_tier TEXT DEFAULT 'free', -- free, premium, b2b
    subscription_expires TIMESTAMP,
    credits_remaining INTEGER DEFAULT 0
);

CREATE TABLE user_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- LOCATION & DEMOGRAPHICS (eligibility factors)
    city TEXT,
    state TEXT,
    county TEXT,
    zip_code TEXT,
    country TEXT DEFAULT 'US',
    age INTEGER,
    gender TEXT,
    ethnicity TEXT,
    veteran_status BOOLEAN DEFAULT 0,
    disability_status BOOLEAN DEFAULT 0,
    
    -- PROJECT INFORMATION
    project_type TEXT, -- business, nonprofit, research, creative, education, personal
    project_description TEXT,
    project_field TEXT, -- tech, agriculture, healthcare, arts, etc.
    project_stage TEXT, -- idea, planning, early, established
    
    -- FINANCIAL SITUATION
    annual_income TEXT, -- ranges for privacy
    credit_score_range TEXT,
    business_revenue TEXT,
    funding_needed_min REAL,
    funding_needed_max REAL,
    
    -- QUALIFICATIONS
    education_level TEXT,
    professional_licenses TEXT, -- JSON array
    certifications TEXT, -- JSON array
    industry_experience_years INTEGER,
    
    -- SPECIAL ELIGIBILITY FACTORS (the magic - what others miss)
    minority_owned BOOLEAN DEFAULT 0,
    women_owned BOOLEAN DEFAULT 0,
    lgbtq_owned BOOLEAN DEFAULT 0,
    rural_location BOOLEAN DEFAULT 0,
    economically_disadvantaged_area BOOLEAN DEFAULT 0,
    first_generation BOOLEAN DEFAULT 0,
    formerly_incarcerated BOOLEAN DEFAULT 0,
    foster_care_background BOOLEAN DEFAULT 0,
    tribal_affiliation TEXT,
    religious_affiliation TEXT,
    
    -- COMPRESSED INTELLIGENCE (West Method - symbolic extraction)
    hidden_eligibility_factors TEXT, -- JSON - AI-discovered factors
    nuanced_qualifications TEXT, -- JSON - subtle matches
    
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =============================================================================
-- FUNDING SOURCES (the universe of money)
-- =============================================================================

CREATE TABLE funding_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_verified TIMESTAMP,
    
    -- BASIC INFO
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL, -- grant, loan, contest, angel, microloan, crowdfund, etc.
    provider_name TEXT, -- foundation, agency, company
    provider_type TEXT, -- federal, state, local, private, corporate
    
    -- AMOUNTS
    min_amount REAL,
    max_amount REAL,
    typical_award REAL,
    
    -- TIMING
    application_opens DATE,
    application_deadline DATE,
    deadline_type TEXT, -- rolling, annual, quarterly, one-time
    decision_timeframe TEXT, -- days/weeks/months
    
    -- ELIGIBILITY (structured)
    eligible_states TEXT, -- JSON array or 'ALL'
    eligible_countries TEXT, -- JSON array
    eligible_age_min INTEGER,
    eligible_age_max INTEGER,
    eligible_genders TEXT, -- JSON or 'ALL'
    eligible_project_types TEXT, -- JSON array
    eligible_fields TEXT, -- JSON array
    
    -- REQUIREMENTS (detailed)
    requirements_text TEXT, -- full eligibility text
    prohibited_uses TEXT, -- what you CAN'T use it for
    matching_funds_required BOOLEAN DEFAULT 0,
    matching_percentage REAL,
    
    -- APPLICATION
    application_url TEXT,
    application_complexity TEXT, -- simple, moderate, complex, very_complex
    application_page_count INTEGER,
    requires_business_plan BOOLEAN DEFAULT 0,
    requires_financial_statements BOOLEAN DEFAULT 0,
    requires_letters_of_support BOOLEAN DEFAULT 0,
    requires_resume BOOLEAN DEFAULT 0,
    estimated_hours_to_complete REAL,
    
    -- SUCCESS DATA
    success_rate REAL, -- percentage if known
    number_awarded_last_year INTEGER,
    total_applicants_last_year INTEGER,
    
    -- METADATA
    source_url TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    notes TEXT,
    tags TEXT, -- JSON array for search
    active BOOLEAN DEFAULT 1,
    
    -- QUALITY SCORE (our assessment)
    quality_score REAL, -- 0-100, based on legitimacy, success rate, clarity
    legitimacy_verified BOOLEAN DEFAULT 0
);

-- =============================================================================
-- MATCHES & REPORTS (the core output)
-- =============================================================================

CREATE TABLE funding_matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    source_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- MATCH SCORING (Mirror Protocol consistency)
    overall_score REAL NOT NULL, -- 0-100
    eligibility_score REAL, -- do they qualify?
    success_probability REAL, -- likelihood of winning
    effort_score REAL, -- how hard is application?
    timeline_score REAL, -- can they meet deadline?
    
    -- DETAILED MATCH REASONS (why this recommendation)
    match_reasons TEXT, -- JSON array of specific reasons
    eligibility_gaps TEXT, -- JSON array of missing requirements
    competitive_advantages TEXT, -- JSON array of strengths
    
    -- STATUS TRACKING
    status TEXT DEFAULT 'recommended', -- recommended, saved, applied, awarded, rejected
    user_notes TEXT,
    application_started DATE,
    application_submitted DATE,
    decision_received DATE,
    outcome TEXT, -- awarded, rejected, waitlisted
    amount_awarded REAL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (profile_id) REFERENCES user_profiles(profile_id),
    FOREIGN KEY (source_id) REFERENCES funding_sources(source_id)
);

CREATE TABLE funding_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- REPORT METADATA
    report_type TEXT DEFAULT 'comprehensive', -- quick, comprehensive, specialized
    num_opportunities INTEGER,
    total_potential_funding REAL,
    
    -- REPORT CONTENT (stored as structured data)
    executive_summary TEXT,
    top_matches TEXT, -- JSON array of match_ids with details
    application_roadmap TEXT, -- JSON timeline
    required_documents TEXT, -- JSON checklist
    budget_template TEXT, -- structured data
    success_stories TEXT, -- JSON array of similar winner profiles
    
    -- DELIVERABLE
    report_html TEXT, -- rendered HTML
    report_pdf_path TEXT, -- file path if generated
    
    -- ANALYTICS
    report_opened BOOLEAN DEFAULT 0,
    report_opened_at TIMESTAMP,
    opportunities_acted_on INTEGER DEFAULT 0,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (profile_id) REFERENCES user_profiles(profile_id)
);

-- =============================================================================
-- AUDIT TRAIL (Alexandria-style governance tracking)
-- =============================================================================

CREATE TABLE audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    action_type TEXT NOT NULL, -- profile_created, search_run, report_generated, etc.
    action_details TEXT, -- JSON
    ip_address TEXT,
    user_agent TEXT
);

CREATE TABLE system_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    metric_context TEXT -- JSON
);

-- =============================================================================
-- INDEXES FOR PERFORMANCE
-- =============================================================================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_funding_sources_type ON funding_sources(source_type);
CREATE INDEX idx_funding_sources_deadline ON funding_sources(application_deadline);
CREATE INDEX idx_funding_sources_active ON funding_sources(active);
CREATE INDEX idx_funding_matches_user ON funding_matches(user_id);
CREATE INDEX idx_funding_matches_score ON funding_matches(overall_score);
CREATE INDEX idx_funding_matches_status ON funding_matches(status);

-- =============================================================================
-- DATA: Loaded by load_batches.py from batch_11..batch_20 (and BATCH_*.json)
-- =============================================================================

-- =============================================================================
-- VIEWS FOR COMMON QUERIES
-- =============================================================================

CREATE VIEW active_deadlines AS
SELECT 
    source_id,
    source_name,
    provider_name,
    application_deadline,
    CAST((julianday(application_deadline) - julianday('now')) AS INTEGER) as days_remaining,
    min_amount,
    max_amount,
    application_url
FROM funding_sources
WHERE active = 1 
  AND application_deadline >= date('now')
ORDER BY application_deadline ASC;

CREATE VIEW user_match_summary AS
SELECT 
    u.user_id,
    u.email,
    up.project_type,
    COUNT(fm.match_id) as total_matches,
    AVG(fm.overall_score) as avg_match_score,
    SUM(CASE WHEN fm.status = 'applied' THEN 1 ELSE 0 END) as applications_submitted,
    SUM(CASE WHEN fm.outcome = 'awarded' THEN 1 ELSE 0 END) as awards_received,
    COALESCE(SUM(fm.amount_awarded), 0) as total_awarded
FROM users u
LEFT JOIN user_profiles up ON u.user_id = up.user_id
LEFT JOIN funding_matches fm ON u.user_id = fm.user_id
GROUP BY u.user_id;

-- =============================================================================
-- DONE
-- =============================================================================

-- This schema is ready for:
-- 1. User intake data storage
-- 2. Funding source aggregation
-- 3. Intelligent matching
-- 4. Report generation
-- 5. Audit trailing (Alexandria pattern)
-- 6. Success tracking
