import os  # Импорт модуля для работы с файлами
from datetime import datetime  # Импорт модуля для работы с датой и временем
import random  # Импорт модуля для генерации случайных чисел


def generate_unique_filename(path):
    base_path, ext = os.path.splitext(path)  # Разбиваем путь на базовую часть и расширение
    date_str = datetime.now().strftime("%d.%m.%Y")  # Формируем строку с датой в формате "дд.мм.гггг"
    random_number = random.randint(10, 99)  # Генерируем случайное число в диапазоне от 10 до 99
    modified_path = f"{base_path}_modified_{random_number}_{date_str}{ext}"  # Формируем уникальное имя файла

    while os.path.exists(modified_path):  # Если файл с таким именем уже существует
        random_number = random.randint(10, 99)  # Генерируем другое случайное число
        modified_path = f"{base_path}_modified_{random_number}_{date_str}{ext}"  # Формируем уникальное имя файла

    return modified_path  # Возвращаем уникальное имя файла

