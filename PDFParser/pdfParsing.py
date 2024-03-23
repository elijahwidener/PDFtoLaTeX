

import fitz

doc = fitz.open(r"C:/Users/elija/Downloads/Elijah Resume.pdf")

for page in doc:
    sections = []
    current_section = []

    text_blocks = page.get_text("blocks")
    for block in text_blocks:
        x0, y0, x1, y1 = block[:4]
        text = block[4]
        font = block[5]
        size = block[6]

        # Check if the current block is vertically separated from the previous block
        if current_section and y0 - current_section[-1][3] > 20:  # Adjust the threshold as needed
            # Start a new section
            sections.append(current_section)
            current_section = []

        current_section.append(block)

    # Add the last section
    if current_section:
        sections.append(current_section)

    for section in sections:
        print("Section:")
        for block in section:
            text = block[4]
            font = block[5]
            size = block[6]

            if size > 14:
                print("Heading:", text)
            elif ":" in text:
                key, value = text.split(":", 1)
                print(key.strip(), ":", value.strip())
            else:
                print("Text:", text)
        print("---")