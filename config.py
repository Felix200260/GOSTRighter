import os
import getpass

# Устанавливаем значение API ключа
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key: ')

api_key = os.getenv("OPENAI_API_KEY")

# Конфигурация модели
model_config = {
    "model": "gpt-3.5-turbo",
    "api_key": api_key
}
