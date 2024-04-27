import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from loader import load_and_split_documents
from getDocParamsValues import get_document_parameters, analyze_and_save_parameters
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
        # Вместо response.choices[0].text используйте response.content
        # Предполагаем, что в response будет только один ответ от AI.
        # answers[question] = response.content.strip()
        print(response)
    return answers


def main():
    model = ChatOpenAI(**model_config)

    file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    chunks = load_and_split_documents(file_path)
    print(f'Количество чанков: {len(chunks)}')

    faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings(api_key=model_config["api_key"]))

    questions = [
        "Какого размера шрифт следует использовать в этом документе?",
        "Какие отступы следует использовать в этом документе?"
    ]

    # Получение ответов от нейронной сети
    answers = get_answers_from_ai(questions, model)

    # Анализ полученных ответов и сохранение параметров документа
    document_params = analyze_and_save_parameters(answers)
    print("---Параметры документа---")
    if 'font_size' in document_params:
        print(f"Размер шрифта: {document_params['font_size']}")
    else:
        print("Размер шрифта не указан.")

    if 'indent_size' in document_params:
        print(f"Размер отступа: {document_params['indent_size']}")
    else:
        print("Размер отступа не указан.")

    while True:
        user_input = input("Задайте вопрос или введите 'exit' для выхода: ")
        if user_input.lower() == 'exit':
            break
        
        # Поиск в документе с помощью векторного индекса
        docs = faiss_index.similarity_search(user_input, k=1)
        if docs:
            # Получаем параметры документа
            doc_params = get_document_parameters(docs)
            print("---Параметры документа---")
            print(f"Размер шрифта: {doc_params['font_size']}")
            print(f"Размер отступа: {doc_params['indent_size']}")
            # Здесь вы можете использовать полученные параметры для дальнейшей обработки
        else:
            print("Информация по вашему запросу в документе не найдена.")

if __name__ == "__main__":
    main()
