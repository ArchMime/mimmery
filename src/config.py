# src/config.py
import os

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "memoria_qwen.db")

# Configuración de Ollama para hardware de bajos recursos
MODEL_OPTIONS = {
    "temperature": 0.2,
    "top_p": 0.7,
    "num_ctx": 4096  # Ajustado a 4k para el modelo 0.5B para máxima fluidez
}

# Límites de contexto por defecto para el modelo 0.5B
LIMITE_N2_DEFECTO = 10
LIMITE_N3_DEFECTO = 3

"""
# Prompts de comportamiento y resumen
SYSTEM_PROMPT_BASE = (
    "Eres un asistente de desarrollo de software altamente preciso.\n"
    "Apóyate en la memoria del entorno provista abajo para mantener la continuidad.\n"
)

PROMPT_NIVEL1 = (
    "Resume la siguiente conversación en una sola frase técnica de menos de 150 caracteres. "
    "Usa un estilo imperativo y directo, idéntico a un commit de git (ej: 'agrega conexion sqlite y refactoriza cliente'):\n\n"
)

PROMPT_NIVEL2 = (
    "Genera un resumen técnico detallado de la sesión. Incluye puntos clave, decisiones tomadas, "
    "tecnologías discutidas y fragmentos de código esenciales implementados:\n\n"
)
"""
# src/config.py (Reemplaza los prompts antiguos)

SYSTEM_PROMPT_BASE = (
    "Eres un asistente de desarrollo de software altamente preciso.\n"
    "REGLA CRUCIAL DE IDENTIDAD: Tú eres el Asistente (IA) y el humano con el que hablas es el Usuario.\n"
    "A continuación tienes la memoria histórica de tus conversaciones pasadas con este usuario.\n"
    "Usa esta información únicamente como antecedentes para responder al usuario con coherencia. "
    "No inventes datos que no estén explícitamente en el texto.\n"
)

PROMPT_NIVEL1 = (
    "Analiza la conversación adjunta entre USER y ASSISTANT.\n"
    "Escribe una sola frase de menos de 150 caracteres (estilo git commit) que describa la acción principal del usuario.\n"
    "SÉ DIRECTO. Ejemplo: 'usuario indica su nombre Mimo y define pruebas de contexto'\n\n"
)

PROMPT_NIVEL2 = (
    "Genera un resumen técnico riguroso de la conversación adjunta.\n"
    "Usa viñetas limpias. Estructura únicamente:\n"
    "- Decisiones tomadas por el usuario\n"
    "- Datos clave proporcionados (nombres, rutas, tecnologías)\n"
    "- Logica discutida o pasos sugeridos por el usuario\n"
    "No agreges códigos\n"
    "PROHIBIDO: No agregues saludos, despedidas ni comentarios sobre ti mismo.\n\n"
)
