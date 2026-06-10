# src/model_client.py
import ollama
from src.config import MODEL_OPTIONS, SYSTEM_PROMPT_BASE, PROMPT_NIVEL1, PROMPT_NIVEL2

def listar_modelos_locales():
    try:
        respuesta = ollama.list()
        return [modelo['model'] for modelo in respuesta['models']]
    except Exception:
        return []

def consultar_modelo(modelo, mensaje_usuario, contexto, historial):
    # Combinamos las instrucciones del sistema con el contexto compilado de la DB
    prompt_sistema = f"{SYSTEM_PROMPT_BASE}\n{contexto}"
    
    messages = [
        {"role": "system", "content": prompt_sistema},
        *historial,
        {"role": "user", "content": mensaje_usuario}
    ]
    
    # Retornamos el objeto generador puro para el streaming en la CLI
    return ollama.chat(
        model=modelo,
        messages=messages,
        options=MODEL_OPTIONS,
        stream=True
    )

def autogenerar_memorias(modelo, historial_actual):
    # Serializamos la sesión actual a texto legible para los prompts de la IA
    texto_conversacion = ""
    for msg in historial_actual:
        texto_conversacion += f"{msg['role'].upper()}: {msg['content']}\n"
    
    # Generación de Nivel 1 (Commit)
    r1 = ollama.generate(model=modelo, prompt=f"{PROMPT_NIVEL1}{texto_conversacion}")
    commit = r1['response'].strip()
    
    # Generación de Nivel 2 (Resumen Técnico)
    r2 = ollama.generate(model=modelo, prompt=f"{PROMPT_NIVEL2}{texto_conversacion}")
    resumen = r2['response'].strip()
    
    return commit, resumen
