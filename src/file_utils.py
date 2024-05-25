import os  # Импорт модуля для работы с файлами
from datetime import datetime  # Импорт модуля для работы с датой и временем

def generate_unique_filename(path):
    base_path, ext = os.path.splitext(path)  # Разбиваем путь на базовую часть и расширение
    timestamp = datetime.now().strftime("%H-%M-%S_%d.%m.%Y")  # Формируем строку с временем и датой в формате "чч-мм-сс_дд.мм.гггг"
    modified_path = f"{base_path}_modified_{timestamp}{ext}"  # Формируем уникальное имя файла с временной меткой

    while os.path.exists(modified_path):  # Если файл с таким именем уже существует
        timestamp = datetime.now().strftime("%H-%M-%S_%d.%m.%Y")  # Обновляем временную метку
        modified_path = f"{base_path}_modified_{timestamp}{ext}"  # Формируем новое уникальное имя файла

    return modified_path  # Возвращаем уникальное имя файла
