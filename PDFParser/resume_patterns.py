# File: sectionPatterns.py
# Date: 2024-03-23
# Author: Elijah Widener Ferreira
#
# Brief: Patterns for detection resume sections

import re


patterns = {
    "education": re.compile(r"education\s*", re.IGNORECASE),
    "skills": re.compile(r"skills\s*", re.IGNORECASE),
    "experience": re.compile(r"(professional\s*experience|experience)\s*", re.IGNORECASE),
    "projects": re.compile(r"projects\s*", re.IGNORECASE),
    "awards": re.compile(r"awards\s*", re.IGNORECASE),
    "certifications": re.compile(r"certifications\s*", re.IGNORECASE),
    "publications": re.compile(r"publications\s*", re.IGNORECASE),
    "volunteer_work": re.compile(r"(volunteer\s*work|volunteering)\s*", re.IGNORECASE),
    "languages": re.compile(r"languages\s*", re.IGNORECASE),
    "interests": re.compile(r"interests\s*", re.IGNORECASE),
    "references": re.compile(r"references\s*", re.IGNORECASE),
    "achievements": re.compile(r"achievements\s*", re.IGNORECASE),
    "professional_summary": re.compile(r"(professional\s*summary|summary)\s*", re.IGNORECASE),
    "objective": re.compile(r"objective\s*", re.IGNORECASE),
    "courses": re.compile(r"courses\s*", re.IGNORECASE),
    "work_history": re.compile(r"(work\s*history|employment\s*history)\s*", re.IGNORECASE),
    "personal_information": re.compile(r"(personal\s*information|contact\s*information)\s*", re.IGNORECASE),
    "technical_skills": re.compile(r"technical\s*skills\s*", re.IGNORECASE),
    "soft_skills": re.compile(r"soft\s*skills\s*", re.IGNORECASE),
}