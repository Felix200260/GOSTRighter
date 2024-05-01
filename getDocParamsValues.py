# getDocParamsValues.py

import re

def extract_font_size(text):
    if not text:
        raise ValueError("Пустой текст ответа не может быть обработан")
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
    if not text:
        raise ValueError("Пустой текст ответа не может быть обработан")
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

def extract_margin_size(text, side):
    if not text:
        raise ValueError("Пустой текст ответа не может быть обработан")

    # Извлекаем числовые значения, которые могут относиться к размерам полей
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return 20  # Возвращаем значение по умолчанию, если числа не найдены

    # Преобразование найденных строк в целые числа
    numbers = [int(num) for num in numbers]

    # Вычисление среднего значения размеров полей
    number_average = sum(numbers) / len(numbers)

    # Проверка на приемлемый диапазон значений полей
    if 10 <= number_average <= 50:  # Предполагаем диапазон от 10 мм до 50 мм для полей
        return round(number_average)
    else:
        return 20  # Возвращаем значение по умолчанию, если среднее значение вне допустимого диапазона

def handle_font_size(question, answer):
    return extract_font_size(answer)

def handle_indent_size(question, answer):
    return extract_indent_size(answer)

def handle_margin_size(question, answer, side):
    return extract_margin_size(answer, side)

def process_question(question_info, answer):
    if question_info["type"] == "font_size":
        return handle_font_size(question_info["text"], answer)
    elif question_info["type"] == "indent_size":
        return handle_indent_size(question_info["text"], answer)
    elif question_info["type"] == "margin_size":
        return handle_margin_size(question_info["text"], answer, question_info["side"])
    else:
        print(f"Неизвестный тип вопроса: {question_info['type']}")


def analyze_and_save_parameters(questions, answers):
    params = {}
    for question_info in questions:
        question_text = question_info["text"]
        question_type = question_info["type"]
        answer = answers.get(question_text, "")

        if question_type == "font_size":
            params['font_size'] = handle_font_size(question_text, answer)
        elif question_type == "indent_size":
            params['indent_size'] = handle_indent_size(question_text, answer)
        elif question_type == "margin_size":
            side = question_info["side"]
            params[f"margin_size_{side}"] = handle_margin_size(question_text, answer, side)

    return params
