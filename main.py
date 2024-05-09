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

from setDocParamsValues import apply_document_params


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
        print(query_text + ": " + answer)

    return answers


def prepare_questions():
    keywords = load_keywords()  # Загрузка ключевых слов для каждого типа источника
    questions = [
        # {"text": "Какой размер шрифта следует использовать в этом документе?", "type": "font_size"},
        # {"text": "Какие шрифты рекомендуются для использования в этом документе?", "type": "font_recommendation"},
        # {"text": "Какие отступы следует использовать в этом документе?", "type": "indent_size"},
        {"text": "Какой размер поля должен быть в документе слева?", "type": "margin_size", "side": "left"},
        {"text": "Какой размер поля должен быть в документе справа?", "type": "margin_size", "side": "right"},
        {"text": "Какой размер поля должен быть в документе снизу?", "type": "margin_size", "side": "bottom"},
        {"text": "Какой размер поля должен быть в документе сверху?", "type": "margin_size", "side": "top"},
        # TODO: Нужно сделать доп функционал для источников другого типа (не только electronic): 
        # {"text": "Как следует оформлять ссылки на электронных ресурсов согласно ГОСТа? Приведи пример оформления", "type": "source", "subtype": "electronic", "keywords": keywords['electronic']}
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

def main():
    model = ChatOpenAI(**model_config)
    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    questions = prepare_questions()
    answers = get_document_answers(file_path, questions)
    document_params = analyze_and_save_parameters(questions, answers) # пример получаемых данных {'font_size': 12, 'first_line_indent': 1.25, 'line_spacing': 1.5, 'font_name': 'Times New Roman'} 
    print_document_params(document_params)
    
    # Путь к документу Word, который нужно изменить
    doc_path = 'C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/tests/word/testFileWord.docx'
    modified_doc_path = apply_document_params(doc_path, document_params) # передаём: {'font_size': 12, 'first_line_indent': 1.25, 'line_spacing': 1.5, 'font_name': 'Times New Roman'}
    
    # Открыть модифицированный документ
    open_document(modified_doc_path)

if __name__ == "__main__":
    main()
