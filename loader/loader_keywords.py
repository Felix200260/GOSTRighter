import os

# Путь к папке с файлами ключевых слов
KEYWORD_FOLDER = 'source'

def read_keywords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        keywords = file.read().splitlines()
    return keywords

def load_keywords():
    keyword_files = {
        'articles': os.path.join(KEYWORD_FOLDER, 'articles_in_journals_and_collections_key_word.txt'), # Ключ: articles, Значение: source\articles_in_journals_and_collections_key_word.txt
        'books': os.path.join(KEYWORD_FOLDER, 'books_and_monographs.txt'),
        'conferences': os.path.join(KEYWORD_FOLDER, 'conference_materials_and_abstracts.txt'),
        'electronic': os.path.join(KEYWORD_FOLDER, 'electronic_resources.txt'),
        'miscellaneous': os.path.join(KEYWORD_FOLDER, 'miscellaneous.txt'),
        'regulatory': os.path.join(KEYWORD_FOLDER, 'regulatory_documents.txt')
    }
    
    keywords = {}
    for key, path in keyword_files.items():
        print(path)
        keywords[key] = read_keywords(path)
    print(keywords)
    return keywords
