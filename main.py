# main.py

import os
import sys
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from loader.loader_document import load_and_split_documents
from getDocParamsValues import  analyze_and_save_parameters, extract_font_names
from config import model_config
from langchain.chains.question_answering import load_qa_chain

from loader.loader_keywords import load_keywords

from icecream import ic
from docx import Document

from setDocParamsValues.setDocParamsValues import apply_document_params

import pprint


def get_document_answers(file_path, questions):
    texts = load_and_split_documents(file_path)
    if not texts:
        print("В документе не найдено данных.")
        return {}
    
    embeddings = OpenAIEmbeddings()
    faiss_index = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(ChatOpenAI(**model_config), chain_type="stuff") 
    answers = {}

    for query in questions:
        query_text = query["text"]
        if "keywords" in query:
            query_text += ". Ключевые слова: " + ", ".join(query["keywords"])
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
        # TODO: Нужно сделать доп функционал для источников другого типа (не только electronic): 
        {"text": "Как следует оформлять ссылки на электронных ресурсов согласно ГОСТа? Приведи пример оформления", "type": "source", "subtype": "electronic", "keywords": keywords['electronic']}
    ]
    # TODO: Реализовать задавание вопросов по поводу рисунков
    return questions
    # TODO: Реализовать загрузку Word файлов
    # TODO: Узнать есть ли боблиотки, которые загружают разные расширения файлов и достают от туда текст
    # TODO: Реализовать 



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
        pprint.pprint(details, width=80, compact=True)  # Используем pprint для красивого вывода
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
        pprint.pprint(details)  # details - список словарей с деталями indent - отступ, width - ширина
    print("-" * 30)
# indent=4, width=80

def main():
    print_header("Запуск программы")
    
    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    file_name = os.path.basename(file_path)
    print_subheader("Загрузка документа", details=f"Анализируемый документ: {file_name}")

    questions = prepare_questions()
    question_details = [{"text": q["text"], "type": q["type"]} for q in questions]
    print_subheader("Получение вопросов", details=question_details)

    print_subheader("Получение ответов на вопросы")
    answers = get_document_answers(file_path, questions)

    print_subheader("Анализ ответов и сохранение параметров")
    document_params = analyze_and_save_parameters(questions, answers)
    print_document_params(document_params)

    doc_path = 'C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/tests/word/testFileWord.docx'
    doc_name = os.path.basename(doc_path)
    print_subheader("Применение параметров к документу", details=f"Документ для изменений: {doc_name}")
    modified_doc_path = apply_document_params(doc_path, document_params)

    print_subheader("Сохранение измененного документа")
    open_document(modified_doc_path)
    modified_doc_name = os.path.basename(modified_doc_path)
    print(f"Документ сохранен как {modified_doc_name}")

if __name__ == "__main__":
    main()
