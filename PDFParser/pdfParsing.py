import fitz  # PyMuPDF

doc = fitz.open(r"C:/Users/elija/Downloads/Elijah Resume.pdf")

def is_heading(block, average_font_size):
    x0, y0, x1, y1, text, font, size = block
    # Adjust conditions based on font size, potential bold style, and common headings
    return size > average_font_size or any(keyword in text.lower() for keyword in ["education", "skills", "experience"])

def parse_resume_sections(doc):
    for page in doc:
        sections = []
        current_section = []
        text_blocks = page.get_text("blocks")
        
        # Calculate average font size for heuristic
        average_font_size = sum(block[6] for block in text_blocks) / len(text_blocks)
        
        for block in text_blocks:
            if is_heading(block, average_font_size):
                if current_section:
                    sections.append(current_section)
                    current_section = []
            current_section.append(block)
        
        if current_section:
            sections.append(current_section)
        
        # Process sections...
        for section in sections:
            # Example processing
            print("Section:")
            for block in section:
                print(block[4])  # Just printing the text for simplicity
            print("---")


parse_resume_sections(doc)