import pdfplumber

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text
result = extract_text_from_pdf("sample_resume_jordan_lee.pdf")
print(result)