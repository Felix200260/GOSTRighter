import re
from icecream import ic

def extract_font_size(text):
    if not text:
        raise ValueError("Пустой текст ответа не может быть обработан")
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return 12
    numbers = [int(num) for num in numbers]
    number_average_font = sum(numbers) / len(numbers)
    return round(number_average_font) if 8 <= number_average_font <= 16 else 12

def extract_indent_size(text):
    if not text:
        raise ValueError("Пустой текст ответа не может быть обработан")
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return 1.25
    numbers = [int(num) for num in numbers]
    number_average = sum(numbers) / len(numbers)
    return round(number_average) if 0 <= number_average <= 55.87 else 1.25

def extract_margin_size(text, side):
    ic(text)
    if not text:
        print(f"Нет информации для этой стороны: {side}")
        print(f"Установлено значение по умолчанию: {20}")
        return 20  # Возвращает значение по умолчанию, если нет данных для обработки
    numbers = re.findall(r'\d+', text)
    if not numbers:
        return 20
    numbers = [int(num) for num in numbers]
    number_average = sum(numbers) / len(numbers)
    return round(number_average) if 10 <= number_average <= 50 else 20


def extract_font_names(answer):
    # Регулярное выражение для поиска шрифтов, пример: Times New Roman, Arial и т.д.
    font_names = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', answer)
    return font_names


def analyze_and_save_parameters(questions, answers):
    print("Answers dictionary:", answers)
    params = {}
    for question_info in questions:
        question_text = question_info["text"]
        question_type = question_info["type"]
        answer = answers.get(question_text, "")  # Используйте текст вопроса как ключ для получения ответа
        if question_type == "font_size":
            params['font_size'] = extract_font_size(answer)
        elif question_type == "font_recommendation":
            # Извлекаем и сохраняем рекомендуемые шрифты
            params['recommended_fonts'] = extract_font_names(answer)
        elif question_type == "margin_size":
            params[f"margin_size_{question_info['side']}"] = extract_margin_size(answer, question_info["side"])
    return params
