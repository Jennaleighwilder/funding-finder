# FUNDING FINDER - INTAKE QUESTIONNAIRE
# Repurposed from Jennifer's Mystical Heritage Reports intake system
# Proven pattern: extract nuanced information that reveals hidden eligibility

"""
This intake system uses the same deep-extraction patterns that power
Jennifer's mystical reports business (229+ clients, 97% satisfaction).

The key: Ask questions that reveal HIDDEN eligibility factors others miss.

Standard systems ask:
- "What's your business type?"
- "How much funding do you need?"

Jennifer's system asks:
- "Where did your grandmother live?" (reveals rural eligibility)
- "What makes you different?" (reveals minority/diversity factors)
- "What obstacles have you overcome?" (reveals disadvantaged status)
"""

# =============================================================================
# PHASE 1: BASIC PROFILE (Standard Info)
# =============================================================================

BASIC_QUESTIONS = [
    {
        "id": "full_name",
        "type": "text",
        "question": "What's your full name?",
        "required": True,
        "category": "identity"
    },
    {
        "id": "email",
        "type": "email",
        "question": "Email address (for your funding report)",
        "required": True,
        "category": "contact"
    },
    {
        "id": "phone",
        "type": "phone",
        "question": "Phone number (optional, for follow-up)",
        "required": False,
        "category": "contact"
    },
    {
        "id": "location",
        "type": "address",
        "question": "Where are you located?",
        "fields": ["city", "state", "zip_code"],
        "required": True,
        "category": "location",
        "hidden_extraction": "rural_status"  # automatic eligibility flag
    }
]

# =============================================================================
# PHASE 2: DREAM EXTRACTION (What They Actually Want)
# =============================================================================

DREAM_QUESTIONS = [
    {
        "id": "project_vision",
        "type": "textarea",
        "question": "Tell me about your dream. What do you want to create, build, or achieve?",
        "placeholder": "Don't hold back. Tell me the real vision, not the practical version.",
        "required": True,
        "category": "vision",
        "ai_processing": "extract_project_type_and_field"
    },
    {
        "id": "project_stage",
        "type": "select",
        "question": "Where are you in this journey?",
        "options": [
            "Just an idea I can't stop thinking about",
            "I've been planning this for a while",
            "I've started but need help to grow",
            "I'm already doing this and want to expand"
        ],
        "required": True,
        "category": "stage"
    },
    {
        "id": "funding_purpose",
        "type": "textarea",
        "question": "If you had the money tomorrow, what would you do with it? Be specific.",
        "placeholder": "Equipment? Hire people? Training? Space? Materials?",
        "required": True,
        "category": "purpose",
        "ai_processing": "extract_funding_categories"
    },
    {
        "id": "funding_amount",
        "type": "range_slider",
        "question": "How much money do you need?",
        "min": 500,
        "max": 500000,
        "step": 500,
        "show_ranges": ["$500-$5K", "$5K-$25K", "$25K-$100K", "$100K+"],
        "required": True,
        "category": "amount"
    }
]

# =============================================================================
# PHASE 3: HIDDEN ELIGIBILITY EXTRACTION (The Magic)
# =============================================================================

HIDDEN_ELIGIBILITY_QUESTIONS = [
    {
        "id": "identity_factors",
        "type": "multi_select",
        "question": "Which of these describe you? (Select all that apply - this unlocks specific funding sources)",
        "options": [
            "Woman",
            "Person of color",
            "LGBTQ+",
            "Veteran",
            "Person with disability",
            "First-generation college student",
            "Raised in foster care",
            "Formerly incarcerated",
            "Indigenous/Native American",
            "Immigrant or refugee",
            "None of these"
        ],
        "required": True,
        "category": "identity",
        "hidden_extraction": "diversity_eligibility_flags"
    },
    {
        "id": "family_background",
        "type": "textarea",
        "question": "Where did your family come from? (Grandparents, parents - any heritage that matters to you)",
        "placeholder": "Ex: Appalachian coal miners, Vietnamese immigrants, Irish farmers, etc.",
        "required": False,
        "category": "heritage",
        "hidden_extraction": "ethnic_heritage_foundations"  # unlocks cultural grants
    },
    {
        "id": "obstacles_overcome",
        "type": "textarea",
        "question": "What obstacles have you overcome to get here?",
        "placeholder": "Poverty, discrimination, lack of education, health challenges, geographic isolation, etc.",
        "required": False,
        "category": "hardship",
        "hidden_extraction": "economically_disadvantaged_status"
    },
    {
        "id": "community_ties",
        "type": "textarea",
        "question": "What communities do you belong to? (Religious, cultural, professional, local)",
        "placeholder": "Ex: Church member, tribal member, union member, fraternal organization, etc.",
        "required": False,
        "category": "community",
        "hidden_extraction": "fraternal_religious_eligibility"
    },
    {
        "id": "unique_story",
        "type": "textarea",
        "question": "What makes YOUR story different from everyone else doing something similar?",
        "placeholder": "This is where we find the angle that makes you stand out to funders.",
        "required": True,
        "category": "differentiation",
        "ai_processing": "extract_competitive_advantages"
    }
]

# =============================================================================
# PHASE 4: PRACTICAL QUALIFICATIONS
# =============================================================================

QUALIFICATIONS_QUESTIONS = [
    {
        "id": "education_level",
        "type": "select",
        "question": "Highest education level?",
        "options": [
            "Some high school",
            "High school diploma/GED",
            "Some college",
            "Associate's degree",
            "Bachelor's degree",
            "Master's degree",
            "Doctoral degree",
            "Trade/vocational certification"
        ],
        "required": False,
        "category": "education"
    },
    {
        "id": "professional_experience",
        "type": "number",
        "question": "Years of experience in your field?",
        "min": 0,
        "max": 60,
        "required": False,
        "category": "experience"
    },
    {
        "id": "licenses_certifications",
        "type": "textarea",
        "question": "Any professional licenses or certifications?",
        "placeholder": "Ex: Cosmetology license, teaching credential, contractor license, etc.",
        "required": False,
        "category": "credentials"
    },
    {
        "id": "financial_situation",
        "type": "select",
        "question": "Current financial situation (this helps us find appropriate funding types)",
        "options": [
            "Under $25K household income",
            "$25K-$50K household income",
            "$50K-$100K household income",
            "$100K+ household income",
            "Prefer not to say"
        ],
        "required": False,
        "category": "finances"
    },
    {
        "id": "credit_situation",
        "type": "select",
        "question": "Credit score range (helps us filter loan vs. grant options)",
        "options": [
            "Under 580 (or don't know)",
            "580-669",
            "670-739",
            "740+",
            "Prefer not to say"
        ],
        "required": False,
        "category": "credit"
    }
]

# =============================================================================
# PHASE 5: URGENCY & COMMITMENT
# =============================================================================

COMMITMENT_QUESTIONS = [
    {
        "id": "timeline",
        "type": "select",
        "question": "When do you need the funding?",
        "options": [
            "As soon as possible (emergency)",
            "Within 3 months",
            "Within 6 months",
            "Within a year",
            "No rush, just exploring"
        ],
        "required": True,
        "category": "timeline"
    },
    {
        "id": "application_capacity",
        "type": "select",
        "question": "How much time can you dedicate to applying for funding?",
        "options": [
            "A few hours per week",
            "10-20 hours per week",
            "Full-time (40+ hours)",
            "Very limited time"
        ],
        "required": True,
        "category": "capacity",
        "hidden_extraction": "complexity_filter"  # avoid complex apps if low capacity
    },
    {
        "id": "previous_applications",
        "type": "select",
        "question": "Have you applied for grants or funding before?",
        "options": [
            "Never",
            "Once or twice",
            "Several times",
            "Many times"
        ],
        "required": False,
        "category": "experience"
    }
]

# =============================================================================
# AI PROCESSING INSTRUCTIONS (West Method Compression)
# =============================================================================

AI_EXTRACTION_PROMPTS = {
    "extract_project_type_and_field": """
        Analyze the user's project vision and extract:
        - project_type: business, nonprofit, research, creative, education, or personal
        - project_field: specific industry/domain (agriculture, tech, healthcare, arts, etc.)
        - keywords: list of relevant terms for matching
        
        Return as JSON.
    """,
    
    "extract_funding_categories": """
        From the funding purpose description, identify what they need money for:
        - Equipment/supplies
        - Personnel/hiring
        - Training/education
        - Physical space
        - Marketing
        - Operating expenses
        - Research/development
        
        Return as JSON array.
    """,
    
    "extract_competitive_advantages": """
        Identify unique selling points for grant applications:
        - Personal story angles
        - Underserved market focus
        - Innovation elements
        - Community impact potential
        - Unique qualifications
        
        Return as JSON array with specific phrases to use in applications.
    """,
    
    "diversity_eligibility_flags": """
        Based on selected identity factors, flag eligibility for:
        - Women-owned business programs
        - Minority business development programs
        - Veteran programs
        - Disability entrepreneurship programs
        - LGBTQ+ grants
        - First-generation programs
        
        Return as JSON with specific program types.
    """,
    
    "ethnic_heritage_foundations": """
        From family background, identify potential heritage-based funding:
        - Irish American foundations
        - Italian American organizations
        - Asian American business associations
        - Hispanic/Latino foundations
        - Appalachian development programs
        - Tribal programs
        
        Return as JSON with specific foundation keywords.
    """,
    
    "economically_disadvantaged_status": """
        Based on obstacles overcome, flag eligibility for:
        - Economic development zone programs
        - Poverty alleviation grants
        - Second-chance programs
        - Rural development initiatives
        - Health equity programs
        
        Return as JSON.
    """,
    
    "fraternal_religious_eligibility": """
        From community ties, identify organizational funding sources:
        - Religious organization grants
        - Fraternal order scholarships/grants
        - Professional association funding
        - Union programs
        - Tribal programs
        
        Return as JSON with specific organization types.
    """
}

# =============================================================================
# COMPLETE INTAKE FLOW
# =============================================================================

INTAKE_FLOW = {
    "title": "Find Money for Your Dreams",
    "subtitle": "Answer these questions honestly. The more we know, the more opportunities we can find.",
    "estimated_time": "10-15 minutes",
    "phases": [
        {
            "phase_name": "Who You Are",
            "questions": BASIC_QUESTIONS,
            "progress": 20
        },
        {
            "phase_name": "Your Dream",
            "questions": DREAM_QUESTIONS,
            "progress": 40
        },
        {
            "phase_name": "Your Story",
            "description": "This is where we find funding sources others miss.",
            "questions": HIDDEN_ELIGIBILITY_QUESTIONS,
            "progress": 60
        },
        {
            "phase_name": "Your Qualifications",
            "questions": QUALIFICATIONS_QUESTIONS,
            "progress": 80
        },
        {
            "phase_name": "Your Timeline",
            "questions": COMMITMENT_QUESTIONS,
            "progress": 100
        }
    ],
    "completion_message": "Processing your profile and searching for funding opportunities...",
    "ai_processing_note": "Using AI to identify hidden eligibility factors and unconventional matches."
}

# =============================================================================
# NOTES FOR IMPLEMENTATION
# =============================================================================

"""
WHY THIS WORKS (from Jennifer's mystical reports success):

1. LAYERED EXTRACTION
   - Start easy (name, location)
   - Build trust
   - Go deeper (identity, obstacles)
   - Extract hidden value (heritage, community)

2. NATURAL LANGUAGE vs. CHECKBOXES
   - Open text = nuanced information
   - AI processing = pattern recognition
   - Find eligibility factors they didn't know mattered

3. STORYTELLING FRAME
   - "Tell me your dream" not "business description"
   - "What makes you different" not "competitive advantage"
   - People reveal more when it feels personal

4. COMPREHENSIVE COVERAGE
   - Location → rural programs
   - Heritage → cultural foundations
   - Identity → diversity programs
   - Community → fraternal/religious grants
   - Obstacles → second-chance/development programs

5. AI POST-PROCESSING
   - Extract keywords for matching
   - Flag eligibility categories
   - Identify competitive angles
   - Generate application talking points

This is the SAME pattern that makes Jennifer's heritage reports valuable.
It extracts information people didn't know was valuable.
"""
