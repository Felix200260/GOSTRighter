# main.py

from datetime import datetime
import os
import re
import sys
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from loader.loader_document import load_and_split_documents
from getDocParamsValues import analyze_and_save_parameters
from config import model_config
from langchain.chains.question_answering import load_qa_chain

from loader.loader_keywords import load_keywords

from icecream import ic
from docx import Document

from setDocParamsValues.setDocParamsValues import apply_document_params
from reference_formatter import process_document
from getAnswearAndGetLink import get_document_answers_from_pdf, extract_links_from_document
from pprint import pprint

def prepare_questions():
    keywords = load_keywords()  # Загрузка ключевых слов для каждого типа источника
    questions = [
        {"text": "Какой минимальный размер шрифта используется в этом документе?", "type": "font_size"},
        {"text": "Перечислите рекомендуемые шрифты для этого документа.", "type": "font_recommendation"},
        {"text": "Какой абзацный отступ следует использовать в этом документе?", "type": "indent_size"},
        {"text": "Какой размер поля должен быть в документе слева в миллиметрах?", "type": "margin_size", "side": "left"},
        {"text": "Какой размер поля должен быть в документе справа в миллиметрах?", "type": "margin_size", "side": "right"},
        {"text": "Какой размер поля должен быть в документе снизу в миллиметрах?", "type": "margin_size", "side": "bottom"},
        {"text": "Какой размер поля должен быть в документе сверху в миллиметрах?", "type": "margin_size", "side": "top"},
        {"text": "Как следует оформлять ссылки на электронных ресурсов согласно ГОСТа? Приведи пример оформления", "type": "source", "subtype": "electronic", "keywords": keywords['electronic']}
    ]
    return questions




def print_document_params(doc_params):
    print("---Параметры документа---")
    print(f"Размер шрифта: {doc_params.get('font_size', 'не указан')}")
    print(f"Размер отступа: {doc_params.get('indent_size', 'не указан')}")

    # Печать размеров полей
    for side in ['left', 'right', 'top', 'bottom']:
        key = f"margin_size_{side}"
        print(f"Размер поля {side}: {doc_params.get(key, 'не указан')} мм")

    # Вывод рекомендуемых шрифтов
    print("Рекомендуемые шрифты:", ', '.join(doc_params.get('recommended_fonts', ['не указаны'])))


    
    # временная функция 
# Функция для открытия документа, перемещена на глобальный уровень
def open_document(file_path):
    os.startfile(file_path)

def print_subheader(subheader, details=None):
    """ Печатает подзаголовок внутри раздела и дополнительные детали если они есть """
    print("\n" + "-" * 30)
    print(f"{subheader}")
    if details:
        pprint(details, width=80, compact=True)
    print("-" * 30)

def print_header(header):
    """ Печатает заголовок раздела """
    print("\n" + "=" * 50)
    print(f"{header}")
    print("=" * 50)

def print_subheader(subheader, details=None):
    """ Печатает подзаголовок внутри раздела и дополнительные детали, если они есть, с использованием pprint """
    print("\n" + "-" * 30)
    print(f"{subheader}")
    if details:
        pprint(details)  # details - список словарей с деталями indent - отступ, width - ширина
    print("-" * 30)
# indent=4, width=80

def generation_format_question_for_ai(original_links, format_example):
    # Подготовка вопросов для ИИ
    current_date = datetime.now().strftime('%d.%m.%Y')
    questions = [{"text": f"Отформатируй эту ссылку: {ref} по примеру: {format_example}"} for ref in original_links]
    answers = get_document_answers("", questions)  # Путь файла не важен здесь

    # Обрабатываем полученные ответы, чтобы они соответствовали нашему формату
    formatted_references = []
    for ref, answer in zip(original_links, answers.values()):
        formatted_reference = answer.replace("http://example.com/resource", ref)
        formatted_reference = re.sub(r'\(дата обращения \d{2}\.\d{2}\.\д{4}\)', f'(дата обращения {current_date})', formatted_reference)
        formatted_references.append(formatted_reference)
    
    return formatted_references


def main():
    print_header("Запуск программы")
    
    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    doc_name = os.path.basename(file_path)
    print_subheader("Загрузка документа", details=f"Анализируемый документ: {doc_name}")

    questions = prepare_questions()
    question_details = [{"text": q["text"], "type": q["type"]} for q in questions]
    print_subheader("Получение вопросов", details=question_details)

    print_subheader("Получение ответов на вопросы")
    answers = get_document_answers_from_pdf(file_path, questions)

    print_subheader("Анализ ответов и сохранение параметров")
    document_params = analyze_and_save_parameters(questions, answers)
    print_document_params(document_params)

    # doc_path = 'C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/tests/word/testFileWord.docx'
    doc_path = 'C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/tests/test_setDocParamsValues/test_wordFiles/testFileWord.docx'
    doc = Document(doc_path)

    # skdnksafnbkfaenbknknkbnksa
    original_links = extract_links_from_document(doc)
    print(f"Найдено ссылок: {len(original_links)}")

    reference_format_example = answers.get("Как следует оформлять ссылки на электронных ресурсов согласно ГОСТа? Приведи пример оформления")
    formatted_doc_path = process_document(doc_path, original_links, reference_format_example)

    print_subheader("Применение параметров к документу", details=f"Документ для изменений: {formatted_doc_path}")
    final_doc_path = apply_document_params(formatted_doc_path, document_params)
    print(f"Документ окончательно обработан и сохранен как {final_doc_path}")

    print_subheader("Сохранение измененного документа")
    open_document(final_doc_path)
    modified_doc_name = os.path.basename(final_doc_path)
    print(f"Документ сохранен как {modified_doc_name}")

if __name__ == "__main__":
    main()
