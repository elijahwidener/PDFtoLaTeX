# File: pdf_parsing2.py
# Date: 2024-03-24
# Author: Elijah Widener Ferreira
#
# Brief: Second attempt at parsing using fitz starting from new
"""
We use fitz.open() to open the PDF file.
We extract the top section (name, contact, links) from the first block of text on the first page. We split the text by newline characters and assign the name, email, phone, and other links to the resume_data dictionary.
We iterate over the remaining blocks of text to extract sections and subsections.


Text Blocks
Text blocks are structured differently to provide detailed information about the text content, including its layout and styling:

    -type: Always 0 for text blocks.
    -bbox: The bounding box of the text block on the page.
    -number: The block count or number.
    -lines: A list of dictionaries, each representing a line of text within the block. Each line dictionary contains:
    -bbox: The bounding box of the line.
    -wmode: The writing mode, where 0 indicates horizontal and 1 indicates vertical.
    -dir: The writing direction, given as a unit vector (cosine, -sine) relative to the x-axis.
    -spans: A list of span dictionaries, with each span representing a segment of text that shares the same font properties. Each span dictionary includes:
        -bbox: The bounding box of the span.
        -origin: The origin point of the first character in the span.
        -font: The name of the font.
        -ascender and descender: Font metrics relative to a font size of 1, indicating the vertical space that the font occupies above and below the baseline, respectively.
        -size: The font size.
        -flags: An integer representing various font characteristics (italic, bold, etc.).
        -color: The text color, encoded in sRGB format.
        -text: The actual text content of the span.
        -chars: (Optional) A list of character dictionaries if the extraction mode provides it.
"""
import fitz
import re

'''
Parses the top section of a resume which is assumed to be the part with contact info, links, and other misc stuff
'''
def parse_top_section(page):
    top_section_data = {
        "name" : "",
        "contact": {},
        "links": []
    }

    text = page.get_text("blocks")
    top_section = text[0][4].split("\n")
    resume_data["name"] = top_section[0]

    # regex expressions
    phone_regex = re.compile(r"\+?\d{1,3}[-.\s]?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}")
    email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    for line in top_section[1:]:
        phone_match = phone_regex.search(line)
        email_match = email_regex.search(line)

        if email_match:
            top_section_data["contact"]["email"] = email_match.group()
        if phone_match:
            top_section_data["contact"]["phone"] = phone_match.group()
    
        links = page.get_links()
        for link in links:
            if link["uri"] and line.strip() in link["uri"]:
                top_section_data["links"].append({"text": line.strip(), "uri": link["uri"]})
    
    return top_section_data



'''
Analyzes a doc page to identify sections and subsections
'''
def parse_resume(file_path):
    doc = fitz.open(file_path)
    resume_data = {}
    page = doc[0]

    # Extract the top section (name, contact, links)
    resume_data["top_section"] = parse_top_section(page)


    # Extract sections and subsections
    resume_data["sections"] = {}
    text_blocks = page.get_text("dict")["blocks"]
    current_section = None
    current_subsection = None
    avg_font_size = sum(block["lines"][0]["spans"][0]["size"] for block in text_blocks) / len(text_blocks)


    for block in text_blocks:
        if block[0] == 0:  # Section heading
            current_section = block[4].strip()
            resume_data["sections"][current_section] = []
            current_subsection = None  # Reset current subsection when a new section starts
        elif block[0] > 0:  # Subsection or content
            if block[0] == 1:  # Subsection heading
                current_subsection = {"title": block[4].strip(), "content": []}
                resume_data["sections"][current_section].append(current_subsection)
            else:  # Content within a subsection
                content = block[4].strip()
                if content:
                    if current_subsection is None:
                        # Create a new subsection for the content if no subsection heading is found
                        current_subsection = {"title": "", "content": []}
                        resume_data["sections"][current_section].append(current_subsection)
                    current_subsection["content"].append(content)

    doc.close()
    return resume_data

# Usage example
file_path = "PDFtoLaTeX\PDFParser\Elijah Resume.pdf"
resume_data = parse_resume(file_path)
print(resume_data)
