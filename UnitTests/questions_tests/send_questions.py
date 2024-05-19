import os
import json
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

# Устанавливаем значение API ключа
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = input('OpenAI API Key: ')

api_key = os.getenv("OPENAI_API_KEY")

# Конфигурация модели
model_config = {
    "model": "gpt-3.5-turbo",
    "api_key": api_key
}

def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_document_answers(texts, questions):
    # Инициализация необходимых компонентов для работы с моделями
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
        print(f'Вопрос: {query_text} \nОтвет: {answer}')
        print(f'======================================')

    return answers

def prepare_questions():
    keywords = {"electronic": ["электронный ресурс", "URL", "доступ", "доступно по", "дата обращения", "электронная копия", "веб-сайт", "портал", "база данных", "электронный адрес", "DOI"]}
    questions = [
        {"text": "Какой минимальный размер шрифта используется в этом документе?", "type": "font_size"},
        {"text": "Перечислите рекомендуемые шрифты для этого документа.", "type": "font_recommendation"},
        {"text": "Какой абзацный отступ следует использовать в этом документе?", "type": "indent_size"},
        {"text": "Какой размер поля должен быть в документе слева в миллиметрах?", "type": "margin_size", "side": "left"},
        {"text": "Какой размер поля должен быть в документе справа в миллиметрах?", "type": "margin_size", "side": "right"},
        {"text": "Какой размер поля должен быть в документе снизу в миллиметрах?", "type": "margin_size", "side": "bottom"},
        {"text": "Какой размер поля должен быть в документе сверху в миллиметрах?", "type": "margin_size", "side": "top"},
        {"text": "Как следует оформлять ссылки на электронных ресурсов согласно ГОСТа? Приведи пример оформления", "type": "source", "subtype": "electronic", "keywords": keywords['electronic']}
    ]
    return questions

def main():
    # Загрузить текст из файла
    text_path = r"C:\Users\felix\YandexDisk-korchevskyfelix\Programming\Programming\Python\GOSTRighter\UnitTests\loader_tests\PDFDocument.txt"
    document_text = load_text_file(text_path)
    
    # Разбиваем текст на страницы (если требуется)
    texts = [document_text]
    
    questions = prepare_questions()
    answers = get_document_answers(texts, questions)
    
    # Создаем директорию, если её нет
    output_dir = 'UnitTests/questions_tests'
    os.makedirs(output_dir, exist_ok=True)
    
    # Сохраняем ответы в JSON файл
    output_file = os.path.join(output_dir, 'answers.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
