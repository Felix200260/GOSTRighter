import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Доступ к API-ключу
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")

# Создание шаблона запроса
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
output_parser = StrOutputParser() # Класс для преобразования ответов модели в строки

chain = prompt | model | output_parser
# prompt - шаблон пользователя
# model - prompt передаётся в модель
# output_parser - ответ в строку
# chain - ответ(цепочка обработки)

# Выполнение запроса
try:
    result = chain.invoke({"topic": "машина"})
    print("Result:", result)
except Exception as e:
    print("An error occurred:", str(e))

