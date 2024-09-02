from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import re

# Crear una nueva presentación
prs = Presentation()

# Función para añadir una diapositiva con múltiples párrafos y mayor estilización
def add_slide(prs, title, content, title_font_size=32, content_font_size=24):
    slide_layout = prs.slide_layouts[1]  # Diapositiva con título y contenido
    slide = prs.slides.add_slide(slide_layout)
    title_placeholder = slide.shapes.title
    content_placeholder = slide.placeholders[1]

    # Estilo para el título
    title_placeholder.text = title
    title_placeholder.text_frame.paragraphs[0].font.size = Pt(title_font_size)
    title_placeholder.text_frame.paragraphs[0].font.bold = True
    title_placeholder.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

    # Estilo para el contenido
    tf = content_placeholder.text_frame
    tf.clear()  # Limpiar cualquier contenido existente
    
    for paragraph_text in content:
        p = tf.add_paragraph()
        p.font.size = Pt(content_font_size)
        
        if paragraph_text.startswith("-"):
            p.level = 1  # Bullet point
            p.text = paragraph_text[1:].strip()
        elif re.match(r'^\d+\.', paragraph_text):
            p.level = 1  # Numbered list with indent
            p.text = paragraph_text.strip()
        else:
            p.level = 0  # Regular paragraph
            p.text = paragraph_text

# Leer el archivo de texto
with open('contenido.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Procesar el archivo de texto
title = None
subtitle = None
current_slide_title = None
current_slide_content = []

for line in lines:
    line = line.strip()
    
    if line.startswith("# Título:"):
        title = line.replace("# Título:", "").strip()
    elif line.startswith("# Subtítulo:"):
        subtitle = line.replace("# Subtítulo:", "").strip()
    elif line.startswith("# Autor:"):
        author = line.replace("# Autor:", "").strip()
    elif line.startswith("## "):  # Nueva diapositiva
        if current_slide_title:
            add_slide(prs, current_slide_title, current_slide_content)
        current_slide_title = line.replace("## ", "").strip()
        current_slide_content = []
    elif line:  # Parte del contenido de la diapositiva
        current_slide_content.append(line)

# Añadir la última diapositiva
if current_slide_title:
    add_slide(prs, current_slide_title, current_slide_content)

# Crear la diapositiva de título
slide_layout = prs.slide_layouts[0]  # Diapositiva de título
slide = prs.slides.add_slide(slide_layout)
title_placeholder = slide.shapes.title
subtitle_placeholder = slide.placeholders[1]

title_placeholder.text = title
title_placeholder.text_frame.paragraphs[0].font.size = Pt(44)
title_placeholder.text_frame.paragraphs[0].font.bold = True
title_placeholder.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

subtitle_placeholder.text = f"{subtitle}\n{author}"
subtitle_placeholder.text_frame.paragraphs[0].font.size = Pt(24)
subtitle_placeholder.text_frame.paragraphs[0].font.italic = True
subtitle_placeholder.text_frame.paragraphs[0].font.color.rgb = RGBColor(102, 102, 102)

# Mover la diapositiva de título al inicio
xml_slides = prs.slides._sldIdLst  
slides = list(xml_slides)
xml_slides.remove(slides[-1])  # Mover la diapositiva de título al inicio
xml_slides.insert(0, slides[-1])

# Guardar la presentación
prs.save('presentacion_generada.pptx')
