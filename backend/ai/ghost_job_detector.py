"""
Ghost Job Detector & Scam Shield
Analyzes job postings for red flags and provides trust scores
"""

import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class GhostJobDetector:
    """Detects fake job postings and scams using rule-based analysis"""
    
    # Red flag patterns
    SUSPICIOUS_SALARY_PATTERN = r'\$\d{3,}k|100k+|200k+|hiring immediately'
    VAGUE_WORDS = ['flexible', 'easy money', 'work from home entrepreneur', 'unlimited earning']
    SCAM_INDICATORS = ['send money', 'pay upfront', 'wire transfer', 'western union', 'gift card']
    URGENCY_WORDS = ['urgent', 'immediate hire', 'start today', 'limited spots']
    
    def analyze_job_posting(self, job_data: Dict) -> Dict:
        """
        Analyze a job posting and return trust score + red flags
        
        Args:
            job_data: Dictionary containing job posting details
            {
                "title": str,
                "description": str,
                "salary": str (optional),
                "company": str,
                "company_verified": bool,
                "post_date": str (optional),
                "url": str (optional),
                "application_method": str (optional)
            }
        
        Returns:
            {
                "trust_score": int (0-100),
                "risk_level": str ("Safe", "Caution", "High Risk"),
                "red_flags": List[str],
                "recommendations": List[str]
            }
        """
        red_flags = []
        trust_score = 100
        recommendations = []
        
        title = job_data.get("title", "").lower()
        description = job_data.get("description", "").lower()
        salary = job_data.get("salary", "").lower()
        company = job_data.get("company", "")
        company_verified = job_data.get("company_verified", False)
        
        # Check 1: Unrealistic salary
        if self._check_unrealistic_salary(salary, description):
            red_flags.append("Unrealistic or suspiciously high salary mentioned")
            trust_score -= 30
            recommendations.append("Research typical salaries for this role on Glassdoor")
        
        # Check 2: Vague or minimal description
        if len(description) < 100:
            red_flags.append("Job description is too vague or minimal")
            trust_score -= 20
            recommendations.append("Ask for detailed job responsibilities during interview")
        
        # Check 3: Company verification
        if not company_verified:
            red_flags.append("Company is not verified on this platform")
            trust_score -= 25
            recommendations.append("Search company on LinkedIn and verify their website")
        
        # Check 4: Scam language
        scam_count = self._check_scam_language(description, title)
        if scam_count > 0:
            red_flags.append(f"Contains {scam_count} potential scam indicators")
            trust_score -= (scam_count * 15)
            recommendations.append("NEVER send money or personal financial info during application")
        
        # Check 5: High pressure tactics
        if self._check_urgency_tactics(description, title):
            red_flags.append("Uses high-pressure or urgency tactics")
            trust_score -= 15
            recommendations.append("Legitimate companies rarely rush hiring decisions")
        
        # Check 6: Missing contact information
        if not self._has_proper_contact(description, company):
            red_flags.append("Missing proper company contact information")
            trust_score -= 10
            recommendations.append("Verify company email domain matches their website")
        
        # Check 7: Entry-level with excessive experience requirements
        if self._check_experience_inflation(title, description):
            red_flags.append("Entry-level position requiring excessive experience")
            trust_score -= 10
            recommendations.append("This might be a 'ghost job' - apply but keep searching")
        
        # Check 8: Too good to be true perks
        if self._check_unrealistic_perks(description):
            red_flags.append("Promises unusually generous perks or benefits")
            trust_score -= 15
            recommendations.append("If it sounds too good to be true, it probably is")
        
        # Ensure trust score doesn't go below 0
        trust_score = max(0, trust_score)
        
        # Determine risk level
        if trust_score >= 80:
            risk_level = "Safe"
        elif trust_score >= 50:
            risk_level = "Caution"
        else:
            risk_level = "High Risk"
        
        # Add positive indicators if score is high
        if trust_score >= 80:
            recommendations.append("✓ This posting appears legitimate - proceed with confidence")
        
        return {
            "trust_score": trust_score,
            "risk_level": risk_level,
            "red_flags": red_flags,
            "recommendations": recommendations,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _check_unrealistic_salary(self, salary: str, description: str) -> bool:
        """Check for unrealistic salary claims"""
        combined = f"{salary} {description}"
        return bool(re.search(self.SUSPICIOUS_SALARY_PATTERN, combined, re.IGNORECASE))
    
    def _check_scam_language(self, description: str, title: str) -> int:
        """Count scam indicators in text"""
        combined = f"{description} {title}".lower()
        count = 0
        for indicator in self.SCAM_INDICATORS:
            if indicator in combined:
                count += 1
        return count
    
    def _check_urgency_tactics(self, description: str, title: str) -> bool:
        """Check for high-pressure urgency tactics"""
        combined = f"{description} {title}".lower()
        return any(word in combined for word in self.URGENCY_WORDS)
    
    def _has_proper_contact(self, description: str, company: str) -> bool:
        """Check if posting has proper contact information"""
        # Look for email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        has_email = bool(re.search(email_pattern, description))
        has_company = bool(company and len(company) > 2)
        return has_email or has_company
    
    def _check_experience_inflation(self, title: str, description: str) -> bool:
        """Check for entry-level jobs requiring too much experience"""
        is_entry_level = any(term in title.lower() for term in ['entry', 'junior', 'associate', 'intern'])
        if not is_entry_level:
            return False
        
        # Look for excessive experience requirements
        experience_patterns = [r'5\+?\s*years', r'7\+?\s*years', r'10\+?\s*years']
        for pattern in experience_patterns:
            if re.search(pattern, description, re.IGNORECASE):
                return True
        return False
    
    def _check_unrealistic_perks(self, description: str) -> bool:
        """Check for too-good-to-be-true perks"""
        unrealistic_perks = [
            'unlimited vacation',
            'work 2 hours',
            'no experience required',
            'make $10000',
            'passive income',
            'get rich'
        ]
        desc_lower = description.lower()
        return any(perk in desc_lower for perk in unrealistic_perks)
    
    def batch_analyze(self, job_listings: List[Dict]) -> List[Dict]:
        """Analyze multiple job postings at once"""
        results = []
        for job in job_listings:
            analysis = self.analyze_job_posting(job)
            analysis['job_title'] = job.get('title', 'Unknown')
            analysis['company'] = job.get('company', 'Unknown')
            results.append(analysis)
        
        return sorted(results, key=lambda x: x['trust_score'], reverse=True)


# Global instance
detector = GhostJobDetector()


def verify_job_posting(job_data: Dict) -> Dict:
    """Main function to verify a job posting"""
    return detector.analyze_job_posting(job_data)


def analyze_multiple_jobs(job_listings: List[Dict]) -> List[Dict]:
    """Analyze multiple job postings"""
    return detector.batch_analyze(job_listings)
