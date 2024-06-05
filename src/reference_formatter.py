from docx import Document
import re
from file_utils import generate_unique_filename
from datetime import datetime
from getAnswearAndGetLink import format_links_based_on_example, extract_links_from_document

def generation_format_question_for_ai(original_links, format_example):
    # current_date = datetime.now().strftime('%d.%м.%Y')
    questions = [{"text": f"Отформатируй эту ссылку: {ref} по примеру: {format_example}"} for ref in original_links]
    answers = format_links_based_on_example(questions, original_links)  # Передаем уже подготовленные вопросы
    
    return answers

def link_formatting(doc_path, original_links, format_example, temp_doc_path):
    doc = Document(doc_path)
    answers = generation_format_question_for_ai(original_links, format_example)  # Получаем отформатированные ссылки

    for paragraph in doc.paragraphs:
        for original, formatted in zip(original_links, answers):
            if original in paragraph.text:
                paragraph.text = paragraph.text.replace(original, formatted)
    
    doc.save(temp_doc_path)
