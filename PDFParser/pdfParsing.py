import fitz

doc = fitz.open("C:/Users/elija/Downloads/Elijah Resume.pdf")

for page in doc:
    text_blocks = page.get_text("blocks")
    for block in text_blocks:
        # coordinates
        x0, y0, x1, y1 = block[:4]

        
        raw_text = block[4]
        font_type = block[5]
        font_size = block[6]
        
        if font_size > 14:
            print("Heading:", text)
        elif ":" in raw_text:
            key, value = raw_text.split(":", 1)
            print(key.strip(), ":", value.strip())
        else:
            print("Text:", raw_text)
