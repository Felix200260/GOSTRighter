#loader.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger
from pprint import pformat, pprint

def load_and_split_documents(pdf_path):
    loader = PyPDFLoader(pdf_path)
    logger.info('Текст из документа {}', loader)
    pages = loader.load_and_split()

    # =========================================logging==========================================
    formatted_pages = [f"Page {i}:\n{pformat(page.page_content)}\nMetadata: {pformat(page.metadata)}" for i, page in enumerate(pages)]
    logger.info('Полученные страницы:\n{}', "\n\n".join(formatted_pages))
    # =========================================logging==========================================

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(pages) 

    # =========================================logging==========================================
    formatted_chunks = [f"Chunk {i}:\n{pformat(chunk.page_content)}\nMetadata: {pformat(chunk.metadata)}" for i, chunk in enumerate(chunks)]
    logger.info('Полученные чанки:\n{}', "\n\n".join(formatted_chunks))  # Записываем все formatted_chunks в лог-файл
    # =========================================logging==========================================

    result = [doc.page_content for doc in chunks]

    # =========================================logging==========================================
    logger.info('Содержимое переменной result:\n{}', pformat(result))
    # =========================================logging==========================================
    
    return result 

if __name__ == "__main__":
    logger.add("file_{time}.log", format="{time} {level} {message}", level="INFO")
    # todo вспомнить устройтсов конструкции if __name__ == "__main__":
    pdf_path = r"C:/Users/felix/YandexDisk-korchevskyfelix/Programming/Programming/Python/GOSTRighter/pdf/7.32-2017.pdf"
    load_and_split_documents(pdf_path)

