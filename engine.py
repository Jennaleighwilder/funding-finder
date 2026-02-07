#!/usr/bin/env python3
"""
FUNDING FINDER - MATCHING ENGINE
Built by Jennifer Leigh West
The Forgotten Code Research Institute

Uses patterns from:
- Mirror Protocol™ (cross-platform consistency, recursive verification)
- CHIMERA (multi-domain pattern analysis, self-evolving)
- 33 Voices (identical outputs from complex inputs)

This engine doesn't just match keywords.
It UNDERSTANDS why someone qualifies for unconventional funding sources.
"""

import json
import sqlite3
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import re

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class UserProfile:
    """User profile data structure"""
    user_id: int
    profile_id: int
    
    # Basic
    location: Dict[str, str]
    age: int
    
    # Project
    project_type: str
    project_field: str
    project_description: str
    project_stage: str
    funding_needed: Tuple[float, float]
    
    # Qualifications
    education_level: str
    experience_years: int
    licenses: List[str]
    
    # Financial
    income_range: str
    credit_range: str
    
    # Special Eligibility (THE MAGIC)
    identity_factors: List[str]
    heritage: str
    obstacles_overcome: str
    community_ties: str
    unique_story: str
    
    # AI-Extracted (West Method compression)
    hidden_eligibility_factors: Dict
    nuanced_qualifications: Dict
    competitive_advantages: List[str]
    
    # Timeline
    urgency: str
    time_capacity: str

@dataclass
class FundingSource:
    """Funding source data structure"""
    source_id: int
    source_name: str
    source_type: str
    provider_name: str
    provider_type: str
    
    # Amounts
    min_amount: float
    max_amount: float
    
    # Timing
    deadline: Optional[datetime]
    deadline_type: str
    
    # Eligibility
    eligible_states: List[str]
    eligible_project_types: List[str]
    eligible_fields: List[str]
    requirements_text: str
    
    # Application
    application_complexity: str
    estimated_hours: float
    
    # Success
    success_rate: float
    awards_last_year: int
    application_url: Optional[str] = None

@dataclass
class Match:
    """Match result with scoring breakdown"""
    source: FundingSource
    overall_score: float
    
    # Sub-scores
    eligibility_score: float
    success_probability: float
    effort_score: float
    timeline_score: float
    fit_score: float
    
    # Explanations
    match_reasons: List[str]
    eligibility_gaps: List[str]
    competitive_advantages: List[str]

# =============================================================================
# MATCHING ENGINE (Mirror Protocol Logic)
# =============================================================================

class FundingMatchEngine:
    """
    Main matching engine using Mirror Protocol principles:
    - Recursive verification at each layer
    - Cross-domain consistency
    - Pattern recognition across seemingly unrelated factors
    """
    
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        
    def match(self, profile: UserProfile, max_results: int = 50) -> List[Match]:
        """
        Main matching function.
        Uses multi-layer scoring similar to Mirror Protocol's recursive checks.
        Excludes sources that require an identity the user did not select (e.g. veteran-only when not a veteran).
        """
        
        # Get all active funding sources
        sources = self._get_active_sources()
        
        # User's selected identities (normalized lowercase for comparison)
        user_identities = [str(x).lower().strip() for x in (profile.identity_factors or [])]
        
        # Score each source (skip identity-restricted sources user doesn't qualify for)
        matches = []
        for source in sources:
            required = self._source_required_identities(source)
            if required:
                # Source is restricted to a specific identity (e.g. veteran-only, women-only)
                def user_has_required(rid: str) -> bool:
                    if rid in user_identities:
                        return True
                    if rid == "minority" and "person of color" in user_identities:
                        return True
                    return False
                if not any(user_has_required(rid) for rid in required):
                    continue  # User didn't select that identity – don't waste their time
            match = self._score_match(profile, source)
            if match.overall_score >= 15:  # Minimum threshold – show more opportunities
                matches.append(match)
        
        # Sort by overall score
        matches.sort(key=lambda x: x.overall_score, reverse=True)
        
        return matches[:max_results]
    
    def _score_match(self, profile: UserProfile, source: FundingSource) -> Match:
        """
        Score a single profile-source match.
        Five-factor scoring (like Persephone's five phases):
        1. Eligibility (can they apply?)
        2. Success Probability (will they win?)
        3. Effort (can they complete application?)
        4. Timeline (can they meet deadline?)
        5. Fit (is this right for their vision?)
        """
        
        # Layer 1: Eligibility Scoring
        eligibility = self._score_eligibility(profile, source)
        
        # Layer 2: Success Probability (competitive advantage)
        success_prob = self._score_success_probability(profile, source)
        
        # Layer 3: Effort Assessment
        effort = self._score_effort(profile, source)
        
        # Layer 4: Timeline Viability
        timeline = self._score_timeline(profile, source)
        
        # Layer 5: Strategic Fit
        fit = self._score_fit(profile, source)
        
        # Overall Score (weighted combination)
        overall = (
            eligibility * 0.35 +      # Most important - can they apply?
            success_prob * 0.25 +     # Will they win?
            fit * 0.20 +              # Is it right for their vision?
            timeline * 0.10 +         # Can they meet deadline?
            effort * 0.10             # Can they complete application?
        )
        
        # Generate explanations
        reasons = self._generate_match_reasons(profile, source, eligibility, success_prob)
        gaps = self._identify_eligibility_gaps(profile, source)
        advantages = self._identify_competitive_advantages(profile, source)
        
        return Match(
            source=source,
            overall_score=overall,
            eligibility_score=eligibility,
            success_probability=success_prob,
            effort_score=effort,
            timeline_score=timeline,
            fit_score=fit,
            match_reasons=reasons,
            eligibility_gaps=gaps,
            competitive_advantages=advantages
        )
    
    # -------------------------------------------------------------------------
    # REQUIRED IDENTITY (exclude mismatches so we don't waste people's time)
    # -------------------------------------------------------------------------
    
    def _source_required_identities(self, source: FundingSource) -> List[str]:
        """
        If the source is restricted to a specific identity (e.g. veteran-only, women-owned only),
        return the list of identity tags required. Empty list = no identity restriction.
        """
        req = (source.requirements_text or "").lower()
        name = (source.source_name or "").lower()
        combined = req + " " + name
        
        required = []
        # Veteran-only / military-only
        if any(phrase in combined for phrase in (
            "veteran-owned", "veteran only", "veteran business", "veterans only",
            "military veteran", "service-disabled veteran", "for veterans",
            "veteran-owned business", "veteran entrepreneur"
        )) or ("veteran" in name and ("grant" in name or "fund" in name or "loan" in name)):
            required.append("veteran")
        # Women-only / woman-owned
        if any(phrase in combined for phrase in (
            "woman-owned", "women-owned", "female-owned", "women only",
            "for women", "women entrepreneur", "women-owned business"
        )):
            required.append("woman")
        # Minority-owned / specific demographic
        if any(phrase in combined for phrase in (
            "minority-owned", "minority business", "minority entrepreneur",
            "person of color", "underrepresented minority"
        )):
            required.append("minority")
        # Disability / disabled-owned
        if any(phrase in combined for phrase in (
            "disability", "disabled-owned", "service-disabled", "disabled veteran"
        )) and "veteran" not in combined:  # avoid double-tagging veteran-only
            required.append("disability")
        # LGBTQ-specific
        if any(phrase in combined for phrase in (
            "lgbtq", "lgbt ", "lgbtq+", "pride business", "lgbtq-owned"
        )):
            required.append("lgbtq")
        # First-generation (e.g. first-gen college)
        if any(phrase in combined for phrase in (
            "first-generation", "first generation", "first-gen"
        )):
            required.append("first-generation")
        
        return list(dict.fromkeys(required))  # unique, order preserved
    
    # -------------------------------------------------------------------------
    # LAYER 1: ELIGIBILITY SCORING
    # -------------------------------------------------------------------------
    
    def _score_eligibility(self, profile: UserProfile, source: FundingSource) -> float:
        """
        Check if user meets basic eligibility requirements.
        Uses pattern matching similar to 33 Voices Protocol.
        """
        score = 100.0
        
        # Geographic eligibility
        if source.eligible_states and 'ALL' not in source.eligible_states:
            if profile.location['state'] not in source.eligible_states:
                score -= 100  # Instant disqualification
        
        # Project type eligibility
        if source.eligible_project_types and 'ALL' not in source.eligible_project_types:
            if profile.project_type not in source.eligible_project_types:
                score -= 50  # Major penalty but not disqualifying
        
        # Field eligibility: batch data uses tags (small_business, tech_startup) – match tag or tag with spaces
        ef = [str(f).lower() for f in (source.eligible_fields or [])]
        if ef and 'all' not in ef:
            proj = (profile.project_field or '').lower() + ' ' + (profile.project_description or '').lower()
            field_match = any(
                tag in proj or tag.replace('_', ' ') in proj
                for tag in ef
            )
            if not field_match:
                score -= 10  # Light penalty so more matches show
        
        # Funding amount fit (show stretch opportunities too – don't disqualify)
        user_min, user_max = profile.funding_needed
        if source.max_amount < user_min or source.min_amount > user_max:
            score -= 20  # Amount mismatch – lighter so more matches show
        
        # HIDDEN ELIGIBILITY BOOST (Jennifer's secret sauce)
        # This is where we find unconventional matches
        hidden_boost = self._check_hidden_eligibility(profile, source)
        score += hidden_boost
        
        return max(0, min(100, score))
    
    def _check_hidden_eligibility(self, profile: UserProfile, source: FundingSource) -> float:
        """
        THE MAGIC: Find unconventional eligibility others miss.
        Uses West Method pattern extraction.
        """
        boost = 0
        
        # Check requirements text for hidden keywords
        req_lower = source.requirements_text.lower() if source.requirements_text else ""
        
        # Identity-based matching
        if 'woman' in profile.identity_factors or 'women' in req_lower:
            if 'women' in req_lower or 'woman-owned' in req_lower:
                boost += 25
        
        if 'veteran' in profile.identity_factors:
            if 'veteran' in req_lower or 'military' in req_lower:
                boost += 30
        
        if 'minority' in profile.identity_factors or 'person of color' in profile.identity_factors:
            if 'minority' in req_lower or 'diverse' in req_lower or 'underrepresented' in req_lower:
                boost += 25
        
        if 'disability' in profile.identity_factors:
            if 'disability' in req_lower or 'accessible' in req_lower:
                boost += 20
        
        if 'lgbtq' in profile.identity_factors:
            if 'lgbtq' in req_lower or 'pride' in req_lower:
                boost += 20
        
        # Heritage-based matching (from family background)
        heritage_keywords = ['irish', 'italian', 'asian', 'hispanic', 'latino', 'appalachian', 'tribal', 'indigenous']
        for keyword in heritage_keywords:
            if keyword in profile.heritage.lower() and keyword in req_lower:
                boost += 15
        
        # Hardship-based matching (economically disadvantaged)
        hardship_keywords = ['poverty', 'low-income', 'disadvantaged', 'underserved', 'second-chance']
        if any(kw in profile.obstacles_overcome.lower() for kw in ['poor', 'poverty', 'homeless', 'foster']):
            if any(kw in req_lower for kw in hardship_keywords):
                boost += 20
        
        # Community ties (fraternal/religious)
        community_keywords = ['church', 'religious', 'fraternal', 'union', 'tribal', 'civic']
        for keyword in community_keywords:
            if keyword in profile.community_ties.lower() and keyword in req_lower:
                boost += 15
        
        # Rural location boost
        if profile.hidden_eligibility_factors.get('rural_status'):
            if 'rural' in req_lower:
                boost += 30
        
        # First-generation boost
        if 'first-generation' in profile.identity_factors:
            if 'first-generation' in req_lower or 'first gen' in req_lower:
                boost += 15
        
        return min(50, boost)  # Cap hidden boost at 50 points
    
    # -------------------------------------------------------------------------
    # LAYER 2: SUCCESS PROBABILITY
    # -------------------------------------------------------------------------
    
    def _score_success_probability(self, profile: UserProfile, source: FundingSource) -> float:
        """
        Estimate likelihood of winning based on competitive advantage.
        Uses CHIMERA pattern analysis logic.
        """
        score = 50.0  # Start at baseline
        
        # Base success rate from source
        if source.success_rate:
            score = source.success_rate * 100
        
        # Adjust based on competitive advantages
        num_advantages = len(profile.competitive_advantages)
        if num_advantages >= 3:
            score += 20
        elif num_advantages >= 2:
            score += 10
        
        # Story strength (unique angle)
        if profile.unique_story and len(profile.unique_story) > 100:
            score += 10
        
        # Experience match
        if profile.experience_years >= 5:
            score += 10
        elif profile.experience_years >= 10:
            score += 15
        
        # Education level (some grants prefer certain levels)
        ef = [str(f).lower() for f in (source.eligible_fields or [])]
        if 'education' in ef or 'research' in ef:
            if 'bachelor' in profile.education_level.lower() or 'master' in profile.education_level.lower():
                score += 10
        
        # Underrepresented status (improves chances for diversity-focused grants)
        if len(profile.identity_factors) >= 2:
            score += 15  # Multiple diversity factors = stronger application
        
        return min(100, score)
    
    # -------------------------------------------------------------------------
    # LAYER 3: EFFORT ASSESSMENT
    # -------------------------------------------------------------------------
    
    def _score_effort(self, profile: UserProfile, source: FundingSource) -> float:
        """
        Can they realistically complete the application?
        """
        score = 100.0
        
        # Application complexity vs. user capacity
        complexity_penalty = {
            'simple': 0,
            'moderate': 20,
            'complex': 40,
            'very_complex': 60
        }
        
        capacity_multiplier = {
            'A few hours per week': 2.0,
            'Very limited time': 3.0,
            '10-20 hours per week': 1.0,
            'Full-time (40+ hours)': 0.5
        }
        
        penalty = complexity_penalty.get(source.application_complexity, 20)
        multiplier = capacity_multiplier.get(profile.time_capacity, 1.0)
        
        score -= (penalty * multiplier)
        
        # Estimated hours to complete
        if source.estimated_hours:
            if source.estimated_hours > 40 and profile.time_capacity == 'Very limited time':
                score -= 30
            elif source.estimated_hours < 5:
                score += 10  # Quick win opportunity
        
        return max(0, min(100, score))
    
    # -------------------------------------------------------------------------
    # LAYER 4: TIMELINE VIABILITY
    # -------------------------------------------------------------------------
    
    def _score_timeline(self, profile: UserProfile, source: FundingSource) -> float:
        """
        Can they meet the deadline?
        """
        score = 100.0
        
        if not source.deadline:
            return 100  # Rolling deadline
        
        days_until_deadline = (source.deadline - datetime.now()).days
        
        # Urgency match
        urgency_thresholds = {
            'As soon as possible (emergency)': 30,
            'Within 3 months': 90,
            'Within 6 months': 180,
            'Within a year': 365,
            'No rush, just exploring': 9999
        }
        
        user_threshold = urgency_thresholds.get(profile.urgency, 180)
        
        if days_until_deadline < 0:
            return 0  # Missed deadline
        elif days_until_deadline < 30 and source.application_complexity in ['complex', 'very_complex']:
            score -= 50  # Not enough time for complex application
        elif days_until_deadline > user_threshold:
            score -= 20  # Too far out for their needs
        
        return max(0, score)
    
    # -------------------------------------------------------------------------
    # LAYER 5: STRATEGIC FIT
    # -------------------------------------------------------------------------
    
    def _score_fit(self, profile: UserProfile, source: FundingSource) -> float:
        """
        Is this the RIGHT funding for their vision?
        Uses semantic analysis similar to West Method compression.
        """
        score = 50.0  # Baseline
        
        # Project description keyword matching
        desc_lower = profile.project_description.lower()
        source_name_lower = source.source_name.lower()
        
        # Extract key terms from project description
        project_keywords = self._extract_keywords(desc_lower)
        source_keywords = self._extract_keywords(source_name_lower + " " + (source.requirements_text or ""))
        
        # Keyword overlap
        overlap = len(set(project_keywords) & set(source_keywords))
        score += min(30, overlap * 5)
        
        # Source type alignment with project stage
        stage_preferences = {
            "Just an idea I can't stop thinking about": ['grant', 'contest', 'microloan'],
            "I've been planning this for a while": ['grant', 'loan', 'contest'],
            "I've started but need help to grow": ['loan', 'grant', 'angel'],
            "I'm already doing this and want to expand": ['loan', 'grant', 'angel']
        }
        
        preferred_types = stage_preferences.get(profile.project_stage, [])
        if source.source_type in preferred_types:
            score += 15
        
        return min(100, score)
    
    # -------------------------------------------------------------------------
    # EXPLANATION GENERATION
    # -------------------------------------------------------------------------
    
    def _generate_match_reasons(self, profile: UserProfile, source: FundingSource, 
                                eligibility: float, success_prob: float) -> List[str]:
        """Generate human-readable match reasons"""
        reasons = []
        
        if eligibility >= 80:
            reasons.append(f"You meet all major eligibility requirements for {source.source_name}")
        
        if success_prob >= 70:
            reasons.append("You have strong competitive advantages for this opportunity")
        
        # Specific matches
        if 'woman' in profile.identity_factors and 'women' in source.requirements_text.lower():
            reasons.append("Women-owned business program match")
        
        if 'veteran' in profile.identity_factors and 'veteran' in source.requirements_text.lower():
            reasons.append("Veteran-specific funding opportunity")
        
        if profile.hidden_eligibility_factors.get('rural_status') and 'rural' in source.requirements_text.lower():
            reasons.append("Rural location qualifies you for this program")
        
        # Amount match
        user_min, user_max = profile.funding_needed
        if source.min_amount <= user_min <= source.max_amount:
            reasons.append(f"Funding amount ({source.min_amount:,.0f} - {source.max_amount:,.0f}) matches your needs")
        
        return reasons
    
    def _identify_eligibility_gaps(self, profile: UserProfile, source: FundingSource) -> List[str]:
        """Identify missing requirements"""
        gaps = []
        
        # Check requirements text for common gaps
        req = source.requirements_text.lower() if source.requirements_text else ""
        
        if 'business plan' in req and not any('plan' in advantage.lower() for advantage in profile.competitive_advantages):
            gaps.append("Business plan required - not mentioned in your profile")
        
        if 'financial statements' in req:
            gaps.append("Financial statements may be required")
        
        if 'letters of support' in req or 'recommendation' in req:
            gaps.append("Letters of support/recommendation needed")
        
        return gaps
    
    def _identify_competitive_advantages(self, profile: UserProfile, source: FundingSource) -> List[str]:
        """Identify why they're a strong candidate"""
        advantages = []
        
        # Use AI-extracted advantages
        advantages.extend(profile.competitive_advantages[:3])  # Top 3
        
        # Add identity-based advantages
        if len(profile.identity_factors) >= 2:
            advantages.append("Multiple diversity factors strengthen your application")
        
        if profile.obstacles_overcome and len(profile.obstacles_overcome) > 50:
            advantages.append("Compelling personal story of overcoming obstacles")
        
        if profile.experience_years >= 10:
            advantages.append(f"{profile.experience_years} years of experience in your field")
        
        return advantages[:5]  # Top 5
    
    # -------------------------------------------------------------------------
    # UTILITIES
    # -------------------------------------------------------------------------
    
    def _parse_json_list(self, val, all_marker: Optional[str] = None) -> List:
        """Parse JSON array from DB; support literal 'ALL' for eligibility."""
        if val is None or (isinstance(val, str) and val.strip() == ''):
            return []
        if isinstance(val, str) and all_marker and val.strip().upper() == 'ALL':
            return [all_marker]
        try:
            out = json.loads(val) if isinstance(val, str) else val
            return list(out) if out is not None else []
        except (json.JSONDecodeError, TypeError):
            return [val] if val else []

    def _get_active_sources(self) -> List[FundingSource]:
        """Retrieve active funding sources from database"""
        cursor = self.db.execute("""
            SELECT * FROM funding_sources 
            WHERE active = 1
            ORDER BY quality_score DESC
        """)
        
        sources = []
        for row in cursor:
            sources.append(FundingSource(
                source_id=row['source_id'],
                source_name=row['source_name'],
                source_type=row['source_type'],
                provider_name=row['provider_name'],
                provider_type=row['provider_type'],
                min_amount=row['min_amount'],
                max_amount=row['max_amount'],
                deadline=datetime.fromisoformat(row['application_deadline']) if row['application_deadline'] else None,
                deadline_type=row['deadline_type'],
                eligible_states=self._parse_json_list(row['eligible_states'], 'ALL'),
                eligible_project_types=self._parse_json_list(row['eligible_project_types']),
                eligible_fields=self._parse_json_list(row['eligible_fields'], 'ALL'),
                requirements_text=row['requirements_text'] or "",
                application_complexity=row['application_complexity'],
                estimated_hours=row['estimated_hours_to_complete'] or 0,
                success_rate=row['success_rate'] or 0.1,
                awards_last_year=row['number_awarded_last_year'] or 0,
                application_url=(row['application_url'] or row['source_url']) or None
            ))
        
        return sources
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in stopwords and len(w) > 3]


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    # Initialize engine
    engine = FundingMatchEngine("../database/funding_finder.db")
    
    # Example profile
    profile = UserProfile(
        user_id=1,
        profile_id=1,
        location={'city': 'Johnson City', 'state': 'TN', 'zip': '37601'},
        age=43,
        project_type='business',
        project_field='AI consulting',
        project_description='Building AI tools for underserved communities',
        project_stage="I've started but need help to grow",
        funding_needed=(10000, 50000),
        education_level='Some college',
        experience_years=2,
        licenses=[],
        income_range='Under $25K household income',
        credit_range='Under 580',
        identity_factors=['Woman', 'First-generation college student'],
        heritage='Appalachian',
        obstacles_overcome='Poverty, lack of formal education',
        community_ties='Rural community, church member',
        unique_story='Building AI tools that serve Appalachian communities',
        hidden_eligibility_factors={'rural_status': True},
        nuanced_qualifications={'technical_skills': 'self-taught', 'community_trust': 'high'},
        competitive_advantages=['Deep community knowledge', 'Unique market focus', 'Lived experience'],
        urgency='Within 6 months',
        time_capacity='10-20 hours per week'
    )
    
    # Get matches
    matches = engine.match(profile, max_results=10)
    
    # Display results
    for i, match in enumerate(matches, 1):
        print(f"\n{'='*60}")
        print(f"#{i}: {match.source.source_name}")
        print(f"Overall Score: {match.overall_score:.1f}/100")
        print(f"Provider: {match.source.provider_name}")
        print(f"Amount: ${match.source.min_amount:,.0f} - ${match.source.max_amount:,.0f}")
        print(f"\nScores:")
        print(f"  Eligibility: {match.eligibility_score:.1f}/100")
        print(f"  Success Probability: {match.success_probability:.1f}/100")
        print(f"  Fit: {match.fit_score:.1f}/100")
        print(f"\nWhy this matches:")
        for reason in match.match_reasons:
            print(f"  ✓ {reason}")
        if match.competitive_advantages:
            print(f"\nYour advantages:")
            for adv in match.competitive_advantages:
                print(f"  + {adv}")
        if match.eligibility_gaps:
            print(f"\nMissing requirements:")
            for gap in match.eligibility_gaps:
                print(f"  ⚠ {gap}")
