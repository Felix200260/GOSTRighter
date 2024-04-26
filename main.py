import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter



# Доступ к API-ключу
# Запрос API ключа если он не задан в окружении
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key: ')

api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")

# Создание шаблона запроса
prompt = ChatPromptTemplate.from_template("Ответь на вопрос: {question}")
output_parser = StrOutputParser() # Класс для преобразования ответов модели в строки

chain = prompt | model | output_parser
# prompt - шаблон пользователя
# model - prompt передаётся в модель
# output_parser - ответ в строку
# chain - ответ(цепочка обработки)

# loader = PyPDFLoader("C:/Users/felix/YandexDisk-korchevskyfelix\Programming/Programming/Python/GOSTRighter/pdf")
loader = PyPDFLoader(r"C:/Users/felix/YandexDisk-korchevskyfelix\Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf")
pages = loader.load_and_split()
# print(pages[0])

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=500,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

# Разделяем текст документа на чанки
chunks = text_splitter.split_documents(pages)
print(f'Колличество чанков: {len(chunks)}')

# faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())

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







