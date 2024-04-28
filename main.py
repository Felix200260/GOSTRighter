# main.py

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from loader import load_and_split_documents
from getDocParamsValues import  analyze_and_save_parameters
from config import model_config

def get_answers_from_ai(questions, model):
    answers = {}
    for question in questions:
        messages = [
            # System message может быть пустым, если не нужен контекст.
            # {"role": "system", "content": ""},
            {"role": "user", "content": question},
        ]
        response = model.invoke(messages)
        answers[question] = response.content.strip()
        print(response.content.strip())
    print(answers)    
    return answers

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



def main():
    model = ChatOpenAI(**model_config)

    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    try:
        chunks = load_and_split_documents(file_path)
        if not chunks:
            print("Документ не содержит данных.")
            return
        print(f'Количество чанков: {len(chunks)}')

        faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings(api_key=model_config["api_key"]))
    except Exception as e:
        print(f"Ошибка при загрузке или индексации документа: {e}")
        return

    questions = [
        "Какого размера шрифт следует использовать в этом документе?",
        "Какие отступы следует использовать в этом документе?"
    ]

    answers = get_answers_from_ai(questions, model)
    document_params = analyze_and_save_parameters(answers)
    print_document_params(document_params)

    # while True:
    #     user_input = input("Задайте вопрос или введите 'exit' для выхода: ")
    #     if user_input.lower() == 'exit':
    #         break

if __name__ == "__main__":
    main()

