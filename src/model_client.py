# src/model_client.py
import ollama
from ollama import AsyncClient
from src.config import (
    MODEL_OPTIONS, 
    SYSTEM_PROMPT_BASE, 
    PROMPT_NIVEL1, 
    PROMPT_NIVEL2, 
    PROMPT_NIVEL3_TURNO
)

def listar_modelos_locales():
    try:
        respuesta = ollama.list()
        return [modelo['model'] for modelo in respuesta['models']]
    except Exception:
        return []

async def consultar_modelo_async(modelo, mensaje_usuario, contexto_historico, historial_l4_acotado):
    prompt_sistema = f"{SYSTEM_PROMPT_BASE}\n{contexto_historico}"
    messages = [
        {"role": "system", "content": prompt_sistema},
        *historial_l4_acotado,
        {"role": "user", "content": mensaje_usuario}
    ]
    client = AsyncClient()
    return await client.chat(model=modelo, messages=messages, options=MODEL_OPTIONS, stream=True)

async def destilar_turno_n3_async(modelo, pregunta_usuario, respuesta_asistente):
    """Destila un único turno en vivo. Devuelve una tupla (Q, A) o None si se debe omitir."""
    texto_turno = f"USER: {pregunta_usuario}\nASSISTANT: {respuesta_asistente}\n"
    client = AsyncClient()
    
    r3 = await client.generate(model=modelo, prompt=f"{PROMPT_NIVEL3_TURNO}\n{texto_turno}")
    respuesta = r3['response'].strip()
    
    if respuesta.upper() == "OMITIR" or "Q:" not in respuesta:
        return None
        
    try:
        # Parseo seguro del formato estándar Q: / A:
        partes = respuesta.split("A:")
        preg = partes[0].replace("Q:", "").strip()
        resp = partes[1].strip()
        return preg, resp
    except Exception:
        return None

async def destilar_cascada_final_async(modelo, texto_todos_los_qna):
    """Genera L2 y L1 basándose en el consolidado limpio de la sesión (sin procesar chat crudo)."""
    client = AsyncClient()
    
    # Paso 1: Generar Resumen Técnico L2 basado en los Q&A limpios de la sesión
    r2 = await client.generate(
        model=modelo, 
        prompt=f"{PROMPT_NIVEL2}CONSOLIDADO DE INTERACCIONES SANEADAS:\n{texto_todos_los_qna}"
    )
    resumen_tecnico = r2['response'].strip()
    
    # Paso 2: Generar Micro-Commit L1 basado en el resumen de nivel 2
    r1 = await client.generate(
        model=modelo, 
        prompt=f"{PROMPT_NIVEL1}RESUMEN TÉCNICO:\n{resumen_tecnico}"
    )
    commit_linea = r1['response'].strip()
    
    return commit_linea, resumen_tecnico
