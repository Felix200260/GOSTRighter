import re
from datetime import datetime
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
import os
import subprocess
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from config import model_config

def get_document_answers(questions):
    embeddings = OpenAIEmbeddings()
    texts = [q["text"] for q in questions]
    faiss_index = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(ChatOpenAI(**model_config), chain_type="stuff")
    answers = {}

    for query in questions:
        query_text = query["text"]
        docs = faiss_index.similarity_search(query_text)
        input_dict = {
            'input_documents': docs,
            'question': query_text
        }
        result = chain.invoke(input=input_dict)
        answer = result['output_text']
        answers[query_text] = answer
        print(f'Вопрос: {query_text} \nОтвет: {answer}')
        print(f'======================================')

    return answers

def format_references_with_ai(original_links, format_example):
    # Подготовка вопросов для ИИ
    current_date = datetime.now().strftime('%d.%m.%Y')
    questions = [{"text": f"Отформатируй эту ссылку: {ref} по примеру: {format_example}"} for ref in original_links]
    answers = get_document_answers(questions)

    # Обрабатываем полученные ответы, чтобы они соответствовали нашему формату
    formatted_references = []
    for ref, answer in zip(original_links, answers.values()):
        formatted_reference = answer.replace("http://example.com/resource", ref)
        formatted_reference = re.sub(r'\(дата обращения \d{2}\.\d{2}\.\d{4}\)', f'(дата обращения {current_date})', formatted_reference)
        formatted_references.append(formatted_reference)
    
    return formatted_references

def extract_links_from_document(doc):
    links = []
    for paragraph in doc.paragraphs:
        for match in re.finditer(r'http[s]?://\S+', paragraph.text):
            links.append(match.group())
    return links

def apply_formatted_references(doc, original_links, formatted_links):
    for paragraph in doc.paragraphs:
        for original, formatted in zip(original_links, formatted_links):
            if original in paragraph.text:
                paragraph.text = paragraph.text.replace(original, formatted)

def highlight_text(paragraph, text_to_highlight):
    run = paragraph.add_run()
    run.text = text_to_highlight
    run.font.highlight_color = WD_COLOR_INDEX.YELLOW  # Желтый маркер

def process_document(input_file, output_file, format_example):
    doc = Document(input_file)
    original_links = extract_links_from_document(doc)
    formatted_links = format_references_with_ai(original_links, format_example)
    apply_formatted_references(doc, original_links, formatted_links)
    
    for paragraph in doc.paragraphs:
        for link in formatted_links:
            if link in paragraph.text:
                paragraph.clear()
                highlight_text(paragraph, link)
    
    try:
        doc.save(output_file)
        print(f"Документ '{output_file}' успешно сохранен.")
    except PermissionError:
        temp_output_file = 'temp_' + output_file
        doc.save(temp_output_file)
        print(f"Не удалось сохранить документ как '{output_file}'. Файл открыт в другой программе. Сохранено как '{temp_output_file}'.")

def open_documents(input_file, output_file):
    try:
        if os.name == 'nt':  # Для Windows
            os.startfile(input_file)
            os.startfile(output_file)
        elif os.name == 'posix':  # Для macOS и Linux
            subprocess.call(('open', input_file))
            subprocess.call(('open', output_file))
    except Exception as e:
        print(f"Не удалось открыть документы: {e}")

def main():
    input_file = 'test_editing_link.docx'
    output_file = 'test_editing_link_edited.docx'
    
    # Пример форматирования ссылок
    format_example = """
    1 Статистические показатели российского книгоиздания в 2006 г.: цифры и рейтинги [Электронный ресурс]. —
    2006. — URL: http://bookhamber.ru/stat_2006.htm (дата обращения 12.03.2009).
    """

    #     2 Прогноз научно-технологического развития Российской Федерации на период до 2030 года. — URL: http://
    # government.ru/media/files/41d4b737638891da2184/pdf (дата обращения 15.11.2016).
    # 3 Web of Science. — URL: http://apps.webofknowledge.com/ (дата обращения 15.11.2016).
    
    process_document(input_file, output_file, format_example)
    open_documents(input_file, output_file)

if __name__ == "__main__":
    main()
