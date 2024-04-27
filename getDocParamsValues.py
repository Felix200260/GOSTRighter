import re

def extract_font_size(text):
    match = re.search(r'размер шрифта (\d+)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def extract_indent_size(text):
    match = re.search(r'размер отступа (\d+)', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def get_document_parameters(docs):
    for doc in docs:
        font_size = extract_font_size(doc.page_content)
        indent_size = extract_indent_size(doc.page_content)
        if font_size and indent_size:
            return {
                'font_size': font_size,
                'indent_size': indent_size
            }
    return {
        'font_size': None,
        'indent_size': None
    }

def analyze_and_save_parameters(answers):
    params = {}
    for question, answer in answers.items():
        if "шрифт" in question:
            params['font_size'] = extract_font_size(answer)
        elif "отступы" in question:
            params['indent_size'] = extract_indent_size(answer)
    return params
