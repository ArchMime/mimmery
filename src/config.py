# src/config.py
import os

# ==========================================
# RUTAS DEL ENTORNO LOCAL
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "memoria_qwen.db")

# ==========================================
# CONFIGURACIÓN DE OLLAMA (HARDWARE LOCAL)
# ==========================================
MODEL_OPTIONS = {
    "temperature": 0.2,   # Baja temperatura para respuestas técnicas precisas y deterministas
    "top_p": 0.7,
    "num_ctx": 4096       # Ventana fija controlada matemáticamente por el orquestador
}

# ==========================================
# LÍMITES ESTRICTOS DEL CONTEXTO LIVIANO
# ==========================================
LIMITE_N1 = 10  # Cantidad máxima de micro-commits históricos en el prompt
LIMITE_N2 = 2   # Cantidad máxima de resúmenes arquitectónicos previos
LIMITE_N3 = 3   # Cantidad máxima de Q&A saneados en la ventana activa

# ==========================================
# PROMPTS DEL SISTEMA Y DESTILACIÓN EN CASCADA
# ==========================================

SYSTEM_PROMPT_BASE = (
    "Eres un asistente de desarrollo de software altamente preciso.\n"
    "REGLA CRUCIAL DE IDENTIDAD: Tú eres el Asistente (IA) y el humano es el Usuario.\n"
    "A continuación tienes la memoria histórica de tus conversaciones pasadas.\n"
    "Usa esta información únicamente como antecedentes para responder con coherencia. "
    "No inventes datos que no estén explícitamente en el texto.\n"
)

# Paso 1 de Destilación: Chat Crudo (L4) -> Q&A Saneado (L3)
PROMPT_NIVEL3 = (
    "Analiza la conversación adjunta entre USER y ASSISTANT.\n"
    "Extrae EXCLUSIVAMENTE los bloques de preguntas/problemas técnicos y sus respectivas soluciones o códigos implementados.\n"
    "Elimina saludos, charlas casuales, explicaciones repetitivas y rodeos de cortesía.\n"
    "Devuelve únicamente pares limpios de Pregunta/Solución estructurados en formato Markdown.\n\n"
)

# Paso 2 de Destilación: Q&A Saneado (L3) -> Resumen Técnico (L2)
PROMPT_NIVEL2 = (
    "Analiza el registro de Q&A adjunto.\n"
    "Genera un resumen técnico riguroso de lo avanzado usando viñetas limpias.\n"
    "Estructura la respuesta utilizando únicamente estos tres ejes:\n"
    "- Decisiones de arquitectura tomadas por el usuario\n"
    "- Datos clave proporcionados (tecnologías, rutas de archivos, nombres)\n"
    "- Lógica discutida o pasos sugeridos\n"
    "PROHIBIDO: No agregues bloques de código, saludos, despedidas ni comentarios sobre ti mismo.\n\n"
)

# Paso 3 de Destilación: Resumen Técnico (L2) -> Micro-Commit (L1)
PROMPT_NIVEL1 = (
    "Analiza el resumen técnico adjunto.\n"
    "Escribe una sola frase de menos de 100 caracteres (estilo git commit) en modo imperativo "
    "que describa la acción o avance principal del proyecto.\n"
    "Sé directo y ultra sintético. Ejemplo: 'agrega persistencia sqlite y reestructura submódulo de config'\n\n"
)

# Agregar en src/config.py junto a los otros prompts

PROMPT_NIVEL3_TURNO = (
    "Analiza la siguiente interacción corta entre un USER y un ASSISTANT.\n"
    "Extrae el problema o pregunta técnica y la solución o comandos clave proporcionados.\n"
    "Si la interacción es solo charla casual, saludos o no contiene datos técnicos ni códigos, responde estrictamente con la palabra: OMITIR\n"
    "Si contiene datos técnicos, estructúralo exactamente así:\n"
    "Q: [Pregunta o problema breve]\nA: [Solución, comandos o lógica implementada]\n"
)
