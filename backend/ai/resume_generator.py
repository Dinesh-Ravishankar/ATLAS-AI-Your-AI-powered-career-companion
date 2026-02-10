"""
Resume/Atlas Card PDF Export
Generates professional PDF resumes from user profiles
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from typing import Dict, List
from datetime import datetime


class ResumeGenerator:
    """Generate professional PDF resumes from Atlas Card data"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=6,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=6,
            spaceBefore=12,
            borderColor=colors.HexColor('#1e3a8a'),
            borderWidth=0,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#374151')
        ))
    
    def generate_resume(self, user_data: Dict, profile_data: Dict, skills: List[Dict], projects: List[Dict]) -> BytesIO:
        """
        Generate PDF resume from user profile data
        
        Args:
            user_data: User account info (name, email)
            profile_data: Profile details (bio, education, etc.)
            skills: List of user skills
            projects: List of user projects
        
        Returns:
            BytesIO object containing PDF data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build document
        story = []
        
        # Header - Name
        name = user_data.get('full_name', 'Your Name')
        story.append(Paragraph(name, self.styles['CustomTitle']))
        story.append(Spacer(1, 6))
        
        # Contact Information
        contact_parts = []
        if user_data.get('email'):
            contact_parts.append(user_data['email'])
        if profile_data.get('phone'):
            contact_parts.append(profile_data['phone'])
        if profile_data.get('location'):
            contact_parts.append(profile_data['location'])
        
        if contact_parts:
            contact_text = " | ".join(contact_parts)
            story.append(Paragraph(contact_text, self.styles['ContactInfo']))
        
        # Links
        link_parts = []
        if profile_data.get('linkedin_url'):
            link_parts.append(f"<link href='{profile_data['linkedin_url']}'>LinkedIn</link>")
        if profile_data.get('github_url'):
            link_parts.append(f"<link href='{profile_data['github_url']}'>GitHub</link>")
        if profile_data.get('portfolio_url'):
            link_parts.append(f"<link href='{profile_data['portfolio_url']}'>Portfolio</link>")
        
        if link_parts:
            links_text = " | ".join(link_parts)
            story.append(Paragraph(links_text, self.styles['ContactInfo']))
        
        story.append(Spacer(1, 12))
        
        # Professional Summary / Bio
        if profile_data.get('bio'):
            story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['CustomHeading']))
            story.append(Paragraph(profile_data['bio'], self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Education
        if profile_data.get('university') or profile_data.get('education'):
            story.append(Paragraph("EDUCATION", self.styles['CustomHeading']))
            
            if profile_data.get('university'):
                edu_text = f"<b>{profile_data['university']}</b>"
                if profile_data.get('major'):
                    edu_text += f" - {profile_data['major']}"
                if profile_data.get('graduation_year'):
                    edu_text += f" (Expected {profile_data['graduation_year']})"
                if profile_data.get('gpa'):
                    edu_text += f" | GPA: {profile_data['gpa']}"
                story.append(Paragraph(edu_text, self.styles['Normal']))
            
            # Additional education entries
            if profile_data.get('education'):
                for edu in profile_data['education']:
                    edu_text = f"<b>{edu.get('institution', '')}</b>"
                    if edu.get('degree'):
                        edu_text += f" - {edu['degree']}"
                    if edu.get('year'):
                        edu_text += f" ({edu['year']})"
                    story.append(Paragraph(edu_text, self.styles['Normal']))
                    story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 12))
        
        # Skills
        if skills:
            story.append(Paragraph("SKILLS", self.styles['CustomHeading']))
            
            # Group skills by category
            skills_by_category = {}
            for skill in skills:
                category = skill.get('category', 'Other')
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill.get('name', skill))
            
            for category, skill_list in skills_by_category.items():
                skills_text = f"<b>{category.title()}:</b> {', '.join(skill_list)}"
                story.append(Paragraph(skills_text, self.styles['Normal']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 12))
        
        # Projects
        if projects:
            story.append(Paragraph("PROJECTS", self.styles['CustomHeading']))
            
            for project in projects[:5]:  # Limit to 5 projects
                # Project title
                project_title = f"<b>{project.get('title', 'Untitled Project')}</b>"
                if project.get('github_url'):
                    project_title += f" | <link href='{project['github_url']}'>GitHub</link>"
                if project.get('live_url'):
                    project_title += f" | <link href='{project['live_url']}'>Live Demo</link>"
                
                story.append(Paragraph(project_title, self.styles['Normal']))
                
                # Project description
                if project.get('description'):
                    story.append(Paragraph(project['description'], self.styles['Normal']))
                
                # Tech stack
                if project.get('tech_stack'):
                    tech_text = f"<i>Technologies: {', '.join(project['tech_stack'])}</i>"
                    story.append(Paragraph(tech_text, self.styles['Normal']))
                
                story.append(Spacer(1, 10))
        
        # Target Roles / Career Interests
        if profile_data.get('target_roles'):
            story.append(Paragraph("CAREER INTERESTS", self.styles['CustomHeading']))
            roles_text = ", ".join(profile_data['target_roles'])
            story.append(Paragraph(roles_text, self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Footer - Generated by Atlas AI
        story.append(Spacer(1, 24))
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        footer_text = f"Generated by Atlas AI on {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer


# Global instance
generator = ResumeGenerator()


def export_resume_pdf(user_data: Dict, profile_data: Dict, skills: List, projects: List) -> BytesIO:
    """Main function to export resume as PDF"""
    return generator.generate_resume(user_data, profile_data, skills, projects)
