#loader.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(pages) # чанки в виде массива (список объектов Document). Может ещё пригодиться
    documents = text_splitter.split_documents(pages) #нужно тк в main.py функция from_texts принимает строку, а у нас изначально чанки в виде массива (список объектов Document).
    # print(chunks)
    # type(chunks)
    # Извлекаем текст из каждого Document и возвращаем список строк
    return [doc.page_content for doc in documents]