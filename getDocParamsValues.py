# getDocParamsValues.py

import re

def extract_font_size(text):
    # Извлечь все числовые значения из текста
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return 12  # Возвращаем значение по умолчанию, если числа не найдены

    # Преобразовать найденные строки в целые числа
    numbers = [int(num) for num in numbers]

    # Вычислить среднее значение размеров шрифта
    number_average_font = sum(numbers) / len(numbers)

    # Проверяем, находится ли средний размер шрифта в приемлемых пределах
    if 8 <= number_average_font <= 16:
        return round(number_average_font)
    else:
        return 12  # Возвращаем значение по умолчанию, если среднее значение вне допустимого диапазона

def extract_indent_size(text):
    # Извлечь все числовые значения из текста, которые могут относиться к отступам
    numbers = re.findall(r'\d+', text)  # Находим все числовые значения
    if not numbers:
        return 1.25  # Возвращаем значение по умолчанию, если числа не найдены

    # Преобразовать найденные строки в целые числа
    numbers = [int(num) for num in numbers]

    # Вычислить среднее значение размеров отступов
    number_average = sum(numbers) / len(numbers)

    # Можете определить логические пределы для размеров отступов, например, между 0 и 55.87
    if 0 <= number_average <= 55.87:
        return round(number_average)
    else:
        return 1.25  # Возвращаем значение по умолчанию, если среднее значение вне допустимого диапазона


def analyze_and_save_parameters(answers):
    params = {}
    for question, answer in answers.items():
        if "шрифт" in question:
            params['font_size'] = extract_font_size(answer)
        elif "отступы" in question:
            params['indent_size'] = extract_indent_size(answer)
    return params
