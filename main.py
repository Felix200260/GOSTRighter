import os
import getpass
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.document_loaders import PyPDFLoader

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Доступ к API-ключу
# Запрос API ключа если он не задан в окружении
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key: ')

api_key = os.getenv("OPENAI_API_KEY")
# api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")

# Создание шаблона запроса
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
output_parser = StrOutputParser() # Класс для преобразования ответов модели в строки

chain = prompt | model | output_parser
# prompt - шаблон пользователя
# model - prompt передаётся в модель
# output_parser - ответ в строку
# chain - ответ(цепочка обработки)

# ---------------------------Код проверки работы модели------------------------------------
# Выполнение запроса
# try:
#     result = chain.invoke({"topic": "машина"})
#     print("Result:", result)
# except Exception as e:
#     print("An error occurred:", str(e))
# ---------------------------Код проверки работы модели------------------------------------
# loader = PyPDFLoader("C:/Users/felix/YandexDisk-korchevskyfelix\Programming/Programming/Python/GOSTRighter/pdf")
loader = PyPDFLoader(r"C:/Users/felix/YandexDisk-korchevskyfelix\Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf")
pages = loader.load_and_split()
# print(pages[0])


faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
docs = faiss_index.similarity_search("Какой шрифт следует использовать?", k=2)
for doc in docs:
    print(str(doc.metadata["page"]) + ":", doc.page_content[:300])


