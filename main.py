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
            p.level = 1  
            p.text = paragraph_text[1:].strip()  
        
        
        elif re.match(r'^\d+\.', paragraph_text):
            p.level = 1  
            p.text = paragraph_text.strip()  
        
        else:
            p.level = 0  
            p.text = paragraph_text


# Diapositiva 1: Título
slide_layout = prs.slide_layouts[0]  # Diapositiva de título
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Seminario de Modelación de Transporte"
title.text_frame.paragraphs[0].font.size = Pt(44)
title.text_frame.paragraphs[0].font.bold = True
title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 51, 102)

subtitle.text = "Resumen de Aprendizajes\nRodrigo Vildosola"
subtitle.text_frame.paragraphs[0].font.size = Pt(24)
subtitle.text_frame.paragraphs[0].font.italic = True
subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(102, 102, 102)

# Diapositiva 2: Resumen de la Clase 2
add_slide(prs, "Clase 2: Estadística", 
          [
              "En esta clase, se exploraron conceptos clave de estadística aplicados a la modelación de transporte.",
              "Se enfocaron en:",
              "- Funciones de densidad de probabilidad",
              "- Tests de hipótesis"
          ],
          title_font_size=36, content_font_size=26)

# Diapositiva 3: Funciones de Densidad de Probabilidad
add_slide(prs, "Funciones de Densidad de Probabilidad", 
          [
              "Se analizaron las funciones de densidad de probabilidad (FDP) para describir cómo se distribuyen los valores de una variable aleatoria continua.",
              "Características principales:",
              "- No negativa: f(x) ≥ 0",
              "- Área bajo la curva = 1",
              "- Se utilizan para calcular probabilidades en intervalos específicos.",
              "Ejemplo: Distribución normal, utilizada para modelar la velocidad de vehículos en una carretera."
          ],
          title_font_size=36, content_font_size=24)

# Diapositiva 4: Tests de Hipótesis - Introducción
add_slide(prs, "Tests de Hipótesis: Introducción",
          [
              "Se definió un test de hipótesis como un procedimiento para decidir si aceptar o rechazar una suposición sobre una población basada en una muestra de datos.",
              "Se planteó una pregunta estadística sobre los datos, como si la media de una muestra difiere de un valor específico.",
              "Este proceso se basó en una distribución conocida bajo el supuesto de que la hipótesis nula es verdadera."
          ],
          title_font_size=36, content_font_size=24)

# Diapositiva 5: Tests de Hipótesis - Pasos
add_slide(prs, "Tests de Hipótesis: Pasos",
          [
              "Los pasos seguidos en un test de hipótesis fueron los siguientes:",
              "1. Plantear las hipótesis nula (H₀) y alternativa (H₁).",
              "2. Elegir un nivel de significancia (α).",
              "3. Calcular el estadístico de prueba.",
              "4. Determinar el p-valor.",
              "5. Tomar una decisión: Rechazar H₀ si el p-valor es menor que α.",
              "Ejemplo: Se comparó la media de las velocidades de vehículos en diferentes horas del día."
          ],
          title_font_size=36, content_font_size=24)

# Diapositiva 6: Tarea
add_slide(prs, "Tarea: Aplicación de Estadística",
          [
              "Se asignó la siguiente tarea:",
              "- Realizar un análisis utilizando una función de densidad para modelar los flujos de tráfico en una vía específica.",
              "- Aplicar un test de hipótesis para verificar si la media del flujo vehicular a distintas horas del día es significativamente diferente.",
              "Entrega: Se solicitó presentar los resultados en un informe detallado."
          ],
          title_font_size=36, content_font_size=24)

# Guardar la presentación
prs.save('presentacion_smt_clase2_rodrigo_vildosola.pptx')
