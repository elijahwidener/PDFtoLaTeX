# File: pdfParsing.py
# Date: 2024-03-23
# Author: Elijah Widener Ferreira
#
# Brief: General parsing algorithm for pdf resumes

import fitz  # PyMuPDF
import re
from resume_patterns import patterns  # Importing the patterns

# Fitz parses the pdf into blocks following this form:
    #block[x0][y0][x1][y1][text][font][size]
# we will leverage this to identify sections of a resume, their subsections, and their contents.


doc = fitz.open(r"PDFtoLaTeX\PDFParser\Elijah Resume.pdf")

def detect_section(block, average_font_size):
    x0, y0, x1, y1, text, font, size = block
    # Broaden the keyword list to cover more section possibilities
    
    # Check size and see if text matches any keyword or part of a keyword.
    is_larger_font = size > average_font_size
    section_title = "TBD"
    matches_pattern = False

    for key, pattern in patterns.items():
        if pattern.search(text):
            section_title = key 
            matches_pattern = True
            break
    # Optional: Add more sophisticated logic to identify bold or italic text if possible
    # This could involve checking the font variable or using font_styles if you've defined it to map styles
    return (is_larger_font or matches_pattern, section_title)


def parse_resume_sections(doc):
    sections = {}
    current_section_title = "Initial"  # Start with a default section
    sections[current_section_title] = []  # Initialize the first section to accumulate blocks

    
    for page in doc:
        text_blocks = page.get_text("blocks")

        # Calculate average font size for heuristic
        average_font_size = sum(block[6] for block in text_blocks) / len(text_blocks)
        
        for block in text_blocks:
            is_section, section_title = detect_section(block, average_font_size)
            if is_section and section_title:
                # If this block marks the beginning of a new section, add the previous section's content
                # Then start a new section with this block's text as the first entry
                if current_section_title != section_title:  # New section
                    current_section_title = section_title
                    sections[current_section_title] = []
            sections[current_section_title].append(block[4])
                    

        
        # Process sections...
        for section_title, text in sections.items():
            print(f"Section: {section_title}")
            for block_text in text:
                print(block_text)  # Print accumulated text for each section
            print("---")

def parse_sub_sections(section):
    for block in section:
        pass


parse_resume_sections(doc)
