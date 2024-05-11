from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

from file_utils import generate_unique_filename  # Импорт функции из file_utils.py

def set_doc_params_values(document, font_size, indent_size, line_spacing, font_name, margin_left, margin_right, margin_top, margin_bottom):
    style = document.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    font.italic = False

    print(f"Применен шрифт: {font.name}, размер шрифта: {font.size.pt}, курсив: {font.italic}")

    # Установка размеров полей документа
    section = document.sections[0]  # Берем первую секцию документа
    section.left_margin = Cm(margin_left)
    section.right_margin = Cm(margin_right)
    section.top_margin = Cm(margin_top)
    section.bottom_margin = Cm(margin_bottom)

    for paragraph in document.paragraphs:
        paragraph.style = style
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.left_indent = Cm(indent_size)
        paragraph.paragraph_format.right_indent = Cm(0)
        paragraph.paragraph_format.first_line_indent = Cm(indent_size)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        paragraph.paragraph_format.line_spacing = line_spacing

def apply_document_params(doc_path, params):
    doc = Document(doc_path)

    font_size = params.get('font_size', 12)
    indent_size = params.get('indent_size', 1.25)
    line_spacing = params.get('line_spacing', 1.5)  # Значение по умолчанию
    font_names = params.get('recommended_fonts', ['Times New Roman'])
    font_name = font_names[0] if font_names else 'Times New Roman'  # убеждаемся, что font_name это строка

    margin_left = params.get('margin_size_left', 3.0)  # значение по умолчанию для левого поля в см
    margin_right = params.get('margin_size_right', 1.5)  # значение по умолчанию для правого поля в см
    margin_top = params.get('margin_size_top', 2.0)  # значение по умолчанию для верхнего поля в см
    margin_bottom = params.get('margin_size_bottom', 2.0)  # значение по умолчанию для нижнего поля в см

    print(f"Получены такие параметры документа: шрифт {font_name}, размер шрифта {font_size}, отступ {indent_size}, межстрочный интервал {line_spacing}")
    print(f"Размер поля left: {margin_left} см")
    print(f"Размер поля right: {margin_right} см")
    print(f"Размер поля top: {margin_top} см")
    print(f"Размер поля bottom: {margin_bottom} см")

    set_doc_params_values(
        doc,
        font_size=font_size,
        indent_size=indent_size,
        line_spacing=line_spacing,
        font_name=font_name,
        margin_left=margin_left,
        margin_right=margin_right,
        margin_top=margin_top,
        margin_bottom=margin_bottom
    )

    modified_path = generate_unique_filename(doc_path)  # Используем нашу функцию для генерации уникального имени файла
    doc.save(modified_path)
    print(f"Документ сохранен как {modified_path}")

    return modified_path

