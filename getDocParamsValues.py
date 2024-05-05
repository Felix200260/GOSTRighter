import re
from icecream import ic

def extract_font_size(text):
    if not text:
        default_font_size = 12
        print("Пустой текст ответа: используем размер шрифта по умолчанию:", default_font_size)
        return default_font_size
    numbers = re.findall(r'\d+', text)
    if not numbers:
        print("Не найдены числовые значения: используем размер шрифта по умолчанию:", default_font_size)
        return default_font_size
    number_average_font = sum([int(num) for num in numbers]) / len(numbers)
    if 8 <= number_average_font <= 16:
        return round(number_average_font)
    print("Размер шрифта вне допустимого диапазона: используем значение по умолчанию", default_font_size)
    return default_font_size

def extract_indent_size(text):
    default_indent = 1.25
    if not text:
        print("Пустой текст ответа: используем отступ по умолчанию", default_indent)
        return default_indent
    numbers = re.findall(r'\d+', text)
    if not numbers:
        print("Не найдены числовые значения: используем отступ по умолчанию", default_indent)
        return default_indent
    number_average = sum([int(num) for num in numbers]) / len(numbers)
    return round(number_average) if 0 <= number_average <= 55.87 else default_indent

def extract_margin_size(text, side):
    default_margin = 20
    if not text:
        print(f"Нет информации для этой стороны {side}: используем значение по умолчанию", default_margin)
        return default_margin
    numbers = re.findall(r'\d+', text)
    if not numbers:
        print("Не найдены числовые значения для", side, ": используем значение по умолчанию", default_margin)
        return default_margin
    number_average = sum([int(num) for num in numbers]) / len(numbers)
    return round(number_average) if 10 <= number_average <= 50 else default_margin

def extract_font_names(answer):
    # Регулярное выражение для поиска шрифтов, например, Times New Roman, Arial
    font_names = re.findall(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', answer)
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
