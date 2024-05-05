from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

def set_doc_params_values(document, font_size=12, first_line_indent=1.25, line_spacing=1.5, font_name='Times New Roman'):
    style = document.styles['Normal']
    font = style.font
    font.name = font_name
    font.size = Pt(font_size)
    font.italic = False

    for paragraph in document.paragraphs:
        paragraph.style = style
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph.paragraph_format.left_indent = Cm(0)
        paragraph.paragraph_format.right_indent = Cm(0)
        paragraph.paragraph_format.first_line_indent = Cm(first_line_indent)
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        paragraph.paragraph_format.line_spacing = line_spacing

def apply_document_params(doc_path, params):
    doc = Document(doc_path)
    set_doc_params_values(
        doc,
        font_size=params.get('font_size', 12),
        first_line_indent=params.get('indent_size', 1.25),
        line_spacing=1.5,
        font_name=params.get('recommended_fonts', ['Times New Roman'])[0]
    )
    # Сохраняем измененный документ
    modified_path = doc_path.replace('.docx', '_modified.docx')
    doc.save(modified_path)
    return modified_path
