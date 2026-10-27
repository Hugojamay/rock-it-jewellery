# ==========================================
# CONFIGURACIÓN DEL CLIENTE (¡Cambiar por cada venta!)
# ==========================================

# Nombre del negocio o cliente
CLIENT_NAME = "Joyería Fina Rock it Jewellry"

# Giro o Nicho del cliente
NICHE_NAME = "Joyería de Lujo y Regalos Exclusivos"

# ¿Qué busca exactamente su cliente ideal?
TARGET_DESCRIPTION = "personas que buscan anillos de compromiso, joyas de oro, plata o regalos especiales para bodas, aniversarios o graduaciones."

# Palabras clave y consultas web automáticas que rastreará el agente
SEARCH_QUERIES = [
    "busco anillo de compromiso oro 14k",
    "recomienden joyería fina para regalo de aniversario",
    "donde comprar cadenas de plata o esclavas",
    "busco sortija de matrimonio diseño exclusivo"
]

# Prompt dinámico comercial para la IA adaptado a este negocio
def get_evaluator_prompt(post_text: str) -> str:
    return f"""
    Analiza la siguiente publicación de redes sociales para determinar si es un cliente potencial (prospecto válido) que desea comprar productos del giro: {NICHE_NAME}. 
    El perfil ideal busca activamente: {TARGET_DESCRIPTION}. 
    Descarta spam, memes, noticias o temas ajenos.

    Publicación: "{post_text}"

    Responde estrictamente en formato JSON con la siguiente estructura exacta:
    {{
        "is_valid_prospect": true o false,
        "problem_detected": "breve descripción de lo que el cliente desea comprar o regalar, o null si no aplica",
        "urgency": "Alta", "Media" o "Baja",
        "suggested_message": "Un mensaje amable, empático y profesional de parte de {CLIENT_NAME} sugiriendo su catálogo de piezas exclusivas, o null si no aplica",
        "reasoning": "Breve explicación de por qué es o no es un prospecto válido"
    }}
    """