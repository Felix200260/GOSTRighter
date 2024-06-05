from datetime import datetime
import re
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from loader.loader_document import load_and_split_documents

from openai import OpenAI
from config import model_config

from langchain.chains.question_answering import load_qa_chain

client = OpenAI(api_key=model_config["api_key"])

def get_document_answers_from_pdf(file_path, questions):
    texts = load_and_split_documents(file_path)
    if not texts:
        print("В документе не найдено данных.")
        return {}
    
    embeddings = OpenAIEmbeddings()
    faiss_index = FAISS.from_texts(texts, embeddings)
    chain = load_qa_chain(ChatOpenAI(**model_config), chain_type="stuff")
    answers = {}

    for query in questions:
        query_text = query["text"]
        keywords = query.get("keywords", [])
        if keywords:
            query_text += ". Ключевые слова: " + ", ".join(keywords)
        docs = faiss_index.similarity_search(query_text)
        input_dict = {
            'input_documents': docs,
            'question': query_text
        }
        result = chain.invoke(input=input_dict)
        answer = result['output_text']
        answers[query["text"]] = answer
        print(f'Вопрос: {query["text"]} \nОтвет: {answer}')
        print(f'======================================')

    return answers


def format_links_based_on_example(questions, original_links):
    # questions = [{"text": f"Отформатируй эту ссылку: {link} по примеру: {format_example}"} for link in original_links]
    current_date = datetime.now().strftime('%d.%m.%Y')
    # В этой функции нет необходимости загружать документ, используем плейсхолдер
    # embeddings = OpenAIEmbeddings()
    # faiss_index = FAISS.from_texts([''], embeddings)
    chain = load_qa_chain(ChatOpenAI(**model_config), chain_type="stuff")
    answers = {}
    
    # Проходим по всем вопросам, с которыми работаем
    for query in questions:
        # Извлекаем текст вопроса
        query_text = query["text"]
        # Вызываем модель и получаем ответ
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": query_text}],
            model=model_config["model"]
        )
        answer = response.choices[0].message.content  # Получаем текст ответа        # Сохраняем ответ в словаре
        answers[query_text] = answer
        print(f'======================================')
        # Выводим запрос и ответ в консоль
        print(f'Запрос: {query_text} \nОтформатированная ссылка: {answer}')
        # Выводим разделитель
        print(f'======================================')

    formatted_references = []
    for ref, answer in zip(original_links, [answers[q["text"]] for q in questions]):
        formatted_reference = answer.replace("http://example.com/resource", ref)
        formatted_reference = re.sub(r'\(дата обращения \d{2}\.\d{2}\.\d{4}\)', f'(дата обращения {current_date})', formatted_reference)
        formatted_references.append(formatted_reference)

    return formatted_references


def extract_links_from_document(doc):
    links = []
    for paragraph in doc.paragraphs:
        for match in re.finditer(r'http[s]?://\S+', paragraph.text):
            links.append(match.group())
    return links
