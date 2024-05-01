# main.py

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from loader import load_and_split_documents
from getDocParamsValues import  analyze_and_save_parameters
from config import model_config
from langchain.chains.question_answering import load_qa_chain

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
        query_text = query["text"]  # Получаем текст вопроса из словаря
        docs = faiss_index.similarity_search(query_text)
        input_dict = {
            'input_documents': docs,
            'question': query_text  # Теперь передаем только текст вопроса
        }
        result = chain.invoke(input=input_dict)
        answers[query_text] = result['output_text']  # Используем текст вопроса в качестве ключа
        print(query_text + ": " + result['output_text'])

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

        # Печать размеров полей
    sides = ['left', 'right', 'top', 'bottom']
    for side in sides:
        key = f'margin_size_{side}'
        if key in doc_params and doc_params[key] is not None:
            print(f"Размер поля {side}: {doc_params[key]} мм")
        else:
            print(f"Размер поля {side} не указан.")



def main():
    model = ChatOpenAI(**model_config)

    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    questions = [
    # {"text": "Какой размер шрифта следует использовать в этом документе?", "type": "font_size"},
    # {"text": "Какие отступы следует использовать в этом документе?", "type": "indent_size"},
    {"text": "Какой размер поля должен быть в документе слева?", "type": "margin_size", "side": "left"},
    {"text": "Какой размер поля должен быть в документе справа?", "type": "margin_size", "side": "right"},
    {"text": "Какой размер поля должен быть в документе снизу?", "type": "margin_size", "side": "bottom"},
    {"text": "Какой размер поля должен быть в документе сверху?", "type": "margin_size", "side": "top"},
    ]

    answers = get_document_answers(file_path, questions) #получае словарь ответов
    # print(answers) 
    document_params = analyze_and_save_parameters(questions, answers)
    print_document_params(document_params)

if __name__ == "__main__":
    main()

