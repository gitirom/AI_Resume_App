import re

def clean_text(text):
    text=re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    text = text.replace('\t', ' ')  # Replace tabs with space
    text = text.strip()  
    return text