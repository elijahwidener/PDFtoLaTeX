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
            -bit 0: superscripted (2^0) – not a font property, detected by MuPDF code.
            -bit 1: italic (2^1)
            -bit 2: serifed (2^2)
            -bit 3: monospaced (2^3)
            -bit 4: bold (2^4)
        -color: The text color, encoded in sRGB format.
        -text: The actual text content of the span.
        -chars: (Optional) A list of character dictionaries if the extraction mode provides it.



resume_data structure
│
├── top_section
│   ├── name
│   ├── contact
│   └── links
│       ├── [0]
│       │   ├── text
│       │   └── uri
│       ├── [1]
│       │   ├── text
│       │   └── uri
│       ├── [2]
│       │   ├── text
│       │   └── uri
│       ├── [3]
│       │   ├── text
│       │   └── uri
│       └── [4]
│           ├── text
│           └── uri
│
└── sections
    ├── Default
    │   ├── [0]
    │   │   ├── text
    │   │   ├── font (if different from regular)
    │   │   ├── size
    │   │   ├── color
    │   │   └── flags
    │   ├── [1]
    │   │   ├── text
    │   │   ├── font (if different from regular)
    │   │   ├── size
    │   │   ├── color
    │   │   └── flags
    │   ├── ...
    │   └── [60]
    │       ├── text
    │       ├── font (if different from regular)
    │       ├── size
    │       ├── color
    │       └── flags
    ├── education
    │   └── [0]
    │       ├── text
    │       ├── font (if different from regular)
    │       ├── size
    │       ├── color
    │       └── flags
    ├── skills
    │   └── [0]
    │       ├── text
    │       ├── font (if different from regular)
    │       ├── size
    │       ├── color
    │       └── flags
    ├── languages
    │   └── [0]
    │       ├── text
    │       ├── font (if different from regular)
    │       ├── size
    │       ├── color
    │       └── flags
    ├── experience
    │   └── [0]
    │       ├── text
    │       ├── font (if different from regular)
    │       ├── size
    │       ├── color
    │       └── flags
    └── projects
        └── [0]
            ├── text
            ├── font (if different from regular)
            ├── size
            ├── color
            └── flags
"""
import fitz
import re
from resume_patterns import patterns  # Importing the patterns


def get_average_font_size(blocks):
    """Calculates the average font size across all text blocks."""
    total_size = sum(span["size"] for block in blocks for line in block["lines"] for span in line["spans"])
    total_spans = sum(len(line["spans"]) for block in blocks for line in block["lines"])
    return total_size / total_spans if total_spans else 0


def is_section_heading(line, avg_font_size):
    """Determines if a block is likely a section heading."""
    # Simplified logic: A heading might be identified by larger font size in its first line
    # More complex logic might consider bold text, position, etc.
    pattern_match = ""
    font_size = line["spans"][0]["size"]
    for key, pattern in patterns.items():
        if pattern.search(line["spans"][0]["text"]):
            pattern_match = key
            break

    if pattern_match or font_size > avg_font_size:
        return pattern_match
    else:
        return None


"""
Parses the top section of a resume which is assumed to be the part with contact info, links, and other misc stuff
"""
def parse_top_section(page):
    top_section_data = {
        "name" : "",
        "contact": {},
        "links": []
    }

    text = page.get_text("blocks")
    top_section = text[0][4].split("\n")
    top_section_data["name"] = top_section[0]  # Use top_section_data instead of resume_data

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



"""
Analyzes a doc page to identify sections and subsections
"""
def parse_resume(file_path):
    doc = fitz.open(file_path)
    resume_data = {}
    page = doc[0]

    # Extract the top section (name, contact, links)
    resume_data["top_section"] = parse_top_section(page)


    # Extract sections and subsections
    resume_data["sections"] = {}
    text_blocks = page.get_text("dict")["blocks"]
    avg_font_size = get_average_font_size(text_blocks)
    current_section = None
    normal_font = None
    

    # Regex to be used to identify when a date is present 
    date_regex = re.compile(r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(?:19|20)\d{2})\s*(?:-|to)\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(?:19|20)\d{2}|\bPresent\b)", re.IGNORECASE)


    for block in text_blocks:
        if 'lines' not in block:  # Skip non-text blocks
            continue

        #identify a section such as education or experience
        

        for line in block["lines"]:
            line_text = ""  # Variable to store the text of the entire line
            for span in line["spans"]:
                text = span["text"].strip()
                line_text += text + " "  # Append the text of each span to the line_text variable

                if normal_font is None:
                    normal_font = span["font"]

                span_data = {
                    "text": text,
                    "size": span["size"],
                    "color": span["color"],
                    "flags": span["flags"]
                }
                if span["font"] != normal_font:
                    span_data["font"] = span["font"]  # Include font only if it's different from the normal font

                new_current_section = is_section_heading(line, avg_font_size)    
                if new_current_section is not None and new_current_section is not current_section:  
                    current_section = new_current_section
                    resume_data["sections"][current_section] = []
                    current_subsection = None # Reset subsection for a new section found
                    # Note: This allows for immediate following text to be processed without skipping
                    # Note: We want to check if were at a new section for every line in case the block contains two sections


                # Check for dates within the text, indicating a subsection
                date_match = date_regex.search(text)
                if date_match and current_section is not None:
                    # New subsection identified by a date
                    current_subsection = {"date": date_match.group(), "content": []}
                    resume_data["sections"][current_section].append(current_subsection)
                if current_subsection is not None:
                    # Append content to the current subsection
                        current_subsection["content"].append(span_data)
                elif current_section is not None:
                    # Append content to the current section if not in a subsection
                        resume_data["sections"][current_section].append(span_data)
                # Additional logic here for handling text that doesn't fit as a subsection or section content
                    
                line_data = {
                    "text": line_text.strip(),  # Store the entire line text
                    "size": line["spans"][0]["size"],  # Use the size of the first span as the line size
                    "color": line["spans"][0]["color"],  # Use the color of the first span as the line color
                    "flags": line["spans"][0]["flags"]  # Use the flags of the first span as the line flags
                }
                if current_subsection is not None:
                    current_subsection["content"].append(line_data)
                elif current_section is not None:
                    resume_data["sections"][current_section].append(line_data)

    doc.close()
    return resume_data

def print_sections(data, indent=""):
    for key, value in data.items():
        if key == "sections":
            for section, section_data in value.items():
                print(f"{indent}{section}")
                print_subsections(section_data, indent + "  ")
        elif isinstance(value, dict):
            print_sections(value, indent + "  ")

def print_subsections(section_data, indent=""):
    for item in section_data:
        if isinstance(item, dict) and "date" in item:
            print(f"{indent}{item['date']}")
            print_subsections(item["content"], indent + "  ")
        else:
            print(f"{indent}{item['text']}")

# Usage example
file_path = "PDFtoLaTeX\PDFParser\Elijah Resume.pdf"
resume_data = parse_resume(file_path)
print_sections(resume_data)
