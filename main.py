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
        docs = faiss_index.similarity_search(query)
        input_dict = {
            'input_documents': docs,
            'question': query
        }
        result = chain.invoke(input=input_dict)
        answers[query] = result['output_text']
        print(query + ": " + result['output_text'])  # Печатаем каждый вопрос и его ответ

    return answers

# def get_answers_from_ai(questions, model):
#     answers = {}
#     for question in questions:
#         messages = [
#             # System message может быть пустым, если не нужен контекст.
#             # {"role": "system", "content": ""},
#             {"role": "user", "content": question},
#         ]
#         response = model.invoke(messages)
#         answers[question] = response.content.strip()
#         print(response.content.strip())
#     print(answers)    
#     return answers

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
    questions = [
        "Какой размер шрифта следует использовать в этом документе?",
        "Какие отступы следует использовать в этом документе?",
    ]



    answers = get_document_answers(file_path, questions)
    print(answers)
    document_params = analyze_and_save_parameters(answers)
    print_document_params(document_params)

    # while True:
    #     user_input = input("Задайте вопрос или введите 'exit' для выхода: ")
    #     if user_input.lower() == 'exit':
    #         break

if __name__ == "__main__":
    main()

