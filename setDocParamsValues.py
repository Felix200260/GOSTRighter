from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

def set_doc_params_values(document, font_size, indent_size, line_spacing, font_name):
    style = document.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    font.italic = False

    print(f"Применен шрифт: {font.name}, размер шрифта: {font.size.pt}, курсив: {font.italic}")

    for paragraph in document.paragraphs:
        paragraph.style = style
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.left_indent = Cm(0)
        paragraph.paragraph_format.right_indent = Cm(0)
        paragraph.paragraph_format.first_line_indent = Cm(indent_size)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        paragraph.paragraph_format.line_spacing = line_spacing

        # print(f"Абзац: выравнивание по ширине, отступ первой строки: {paragraph.paragraph_format.first_line_indent.cm}cm, межстрочный интервал: {paragraph.paragraph_format.line_spacing}")

def apply_document_params(doc_path, params):
    doc = Document(doc_path)

    font_size = params.get('font_size', 12)
    indent_size = params.get('indent_size', 1.25)
    line_spacing = params.get('line_spacing', 1.5)  # Значение по умолчанию
    font_names = params.get('recommended_fonts', ['Times New Roman'])
    font_name = font_names[0] if font_names else 'Times New Roman'  # Убедитесь, что font_name это строка

    print(f"Получены такие параметры документа: шрифт {font_name}, размер шрифта {font_size}, отступ {indent_size}, межстрочный интервал {line_spacing}")

    set_doc_params_values(
        doc,
        font_size=font_size,
        indent_size=indent_size,
        line_spacing=line_spacing,
        font_name=font_name
    )

    modified_path = doc_path.replace('.docx', '_modified.docx')
    doc.save(modified_path)
    print(f"Документ сохранен как {modified_path}")

    return modified_path
