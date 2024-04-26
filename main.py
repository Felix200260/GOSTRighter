import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

#мои библиотеки
from loader import load_and_split_documents



# Доступ к API-ключу
# Запрос API ключа если он не задан в окружении
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key: ')

api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")


# Импортируем chunks из loader.py
file_path = r"C:/Users/felix/YandexDisk-korchevskyfelix\Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
chunks = load_and_split_documents(file_path)
print(f'Количество чанков: {len(chunks)}')


# Создаем индекс для частей документа
faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings(api_key=api_key))

while True:
    user_input = input("Задайте вопрос или введите 'exit' для выхода: ")
    if user_input.lower() == 'exit':
        break
    
    # Поиск в документе с помощью векторного индекса
    docs = faiss_index.similarity_search(user_input, k=1)  # k=1 возвращает наиболее релевантный фрагмент
    if docs:
        print("---Ответ из документа:", '\n', docs[0].page_content[:300])  # Выводит первые 300 символов наиболее релевантного ответа
    else:
        print("Информация по вашему запросу в документе не найдена.")

