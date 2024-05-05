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
        {"text": "Какие шрифты рекомендуются для использования в этом документе?", "type": "font_recommendation"},
        # {"text": "Какие отступы следует использовать в этом документе?", "type": "indent_size"},
        # {"text": "Какой размер поля должен быть в документе слева?", "type": "margin_size", "side": "left"},
        # {"text": "Какой размер поля должен быть в документе справа?", "type": "margin_size", "side": "right"},
        # {"text": "Какой размер поля должен быть в документе снизу?", "type": "margin_size", "side": "bottom"},
        # {"text": "Какой размер поля должен быть в документе сверху?", "type": "margin_size", "side": "top"},
        # TODO: Нужно сделать доп функционал для источников другого типа (не только electronic): 
        # {"text": "Как следует оформлять ссылки на электронных ресурсов согласно ГОСТа? Приведи пример оформления", "type": "source", "subtype": "electronic", "keywords": keywords['electronic']}
    ]
    # TODO: Реализовать задавание вопросов по поводу рисунков
    return questions
    # TODO: Реализовать загрузку Word файлов
    # TODO: Узнать есть ли боблиотки, которые загружают разные расширения файлов и достают от туда текст
    # TODO: Реализовать поиск названия шрифта 'Times New Roman'
    # TODO: Реализовать 



def print_document_params(doc_params):
    print("---Параметры документа---")
    if 'font_size' in doc_params and doc_params['font_size'] is not None:
        print(f"Размер шрифта: {doc_params['font_size']}")
    else:
        print("Размер шрифта не указан.")

    if 'indent_size' in doc_params and doc_params['indent_size'] is not None:
        print(f"Размер отступа: {doc_params['indent_size']}")
    else:
        print("Размер отступа не указан.")

        # Печать размеров полей
    sides = ['left', 'right', 'top', 'bottom']
    for side in sides:
        key = f'margin_size_{side}'
        if key in doc_params and doc_params[key] is not None:
            print(f"Размер поля {side}: {doc_params[key]} мм")
        else:
            print(f"Размер поля {side} не указан.")

        # Вывод рекомендуемых шрифтов
    if 'recommended_fonts' in doc_params and doc_params['recommended_fonts']:
        print("Рекомендуемые шрифты:", ', '.join(doc_params['recommended_fonts']))
    else:
        print("Рекомендуемые шрифты не указаны.")

def main():
    model = ChatOpenAI(**model_config)
    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    questions = prepare_questions()
    answers = get_document_answers(file_path, questions)
    document_params = analyze_and_save_parameters(questions, answers)
    
    # Извлечение и сохранение рекомендуемых шрифтов
    recommended_fonts = extract_font_names(answers.get("Какие шрифты рекомендуются для использования в этом документе?", ""))
    document_params['recommended_fonts'] = recommended_fonts
    
    print_document_params(document_params)


if __name__ == "__main__":
    main()

