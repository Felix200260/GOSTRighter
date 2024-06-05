from docx import Document
import re
from file_utils import generate_unique_filename
from datetime import datetime
from getAnswearAndGetLink import format_links_based_on_example, extract_links_from_document

def generation_format_question_for_ai(original_links, format_example):
    current_date = datetime.now().strftime('%d.%m.%Y')
    # Подготавливаем запросы один раз и передаем в функцию
    questions = [{"text": f"Отформатируй эту ссылку: {ref} по примеру: {format_example}"} for ref in original_links]
    answers = format_links_based_on_example(questions, original_links)  # Передаем уже подготовленные вопросы
    formatted_references = []
    for ref, answer in zip(original_links, answers.values()):
        formatted_reference = answer.replace("http://example.com/resource", ref)
        formatted_reference = re.sub(r'\(дата обращения \d{2}\.\d{2}\.\d{4}\)', f'(дата обращения {current_date})', formatted_reference)
        formatted_references.append(formatted_reference)
    
    return formatted_references

def process_document(doc_path, original_links, format_example):
    doc = Document(doc_path)
    formatted_links = generation_format_question_for_ai(original_links, format_example)
    for paragraph in doc.paragraphs:
        for original, formatted in zip(original_links, formatted_links):
            if original in paragraph.text:
                paragraph.text = paragraph.text.replace(original, formatted)
    new_doc_path = generate_unique_filename(doc_path)
    doc.save(new_doc_path)
    return new_doc_path
