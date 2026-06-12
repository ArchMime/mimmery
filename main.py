# main.py
import asyncio
import sys
from src.database import (
    inicializar_db, 
    obtener_proyectos_unicos, 
    obtener_o_crear_sesion, 
    cargar_contexto_base_ordenado, 
    guardar_mensaje_en_vivo,
    finalizar_y_consolidar_sesion
)
# CAMBIO AQUÍ: Reemplazar 'destilar_memorias_async' por 'destilar_cascada_final_async' y añadir 'destilar_turno_n3_async'
from src.model_client import (
    listar_modelos_locales, 
    consultar_modelo_async, 
    destilar_cascada_final_async,
    destilar_turno_n3_async
)

async def main():
    # Inicialización relacional de la BD
    inicializar_db()
    print("=== ORQUESTADOR DE MEMORIA JERÁRQUICA (MOTOR CENTRAL) ===")
    
    # 1. SELECCIÓN ASÍNCRONA DE MODELO LOCAL
    modelos = listar_modelos_locales()
    if not modelos:
        print("\n[!] Error: No se detectó Ollama en ejecución o no hay modelos instalados.")
        return
        
    print("\nModelos detectados:")
    for i, model in enumerate(modelos, start=1):
        print(f" [{i}] {model}")
    sel_m = input("\nSelecciona el índice del modelo: ").strip()
    modelo_activo = modelos[int(sel_m) - 1] if (sel_m.isdigit() and 1 <= int(sel_m) <= len(modelos)) else modelos[0]
    print(f"> Modelo asignado: '{modelo_activo.upper()}'")

    # 2. SELECCIÓN DE PROYECTO
    proyectos = obtener_proyectos_unicos()
    print("\nProyectos registrados en el sistema:")
    print(" [0] GLOBAL (Antecedentes generales de todo el entorno)")
    for i, proj in enumerate(proyectos, start=1):
        print(f" [{i}] {proj}")
        
    seleccion = input("\nSelecciona un número o ingresa uno NUEVO: ").strip()
    if seleccion == "0" or seleccion.lower() == "global":
        proyecto_activo = "global"
    elif seleccion.isdigit() and 1 <= int(seleccion) <= len(proyectos):
        proyecto_activo = proyectos[int(seleccion) - 1]
    else:
        proyecto_activo = seleccion if seleccion else "general"
    print(f"> Ámbito activo: '{proyecto_activo.upper()}'")

    # 3. CONTROL DE RESILIENCIA (Chequeo de Estado Abierto)
    print("\nVerificando integridad del entorno...")
    sesion_id, fue_restaurada = obtener_o_crear_sesion(proyecto_activo)
    
    if fue_restaurada:
        print(f"⚠️ [AVISO]: Se detectó una sesión previa abierta de forma forzada para el proyecto '{proyecto_activo}'.")
        print("Restaurando el historial del chat en vivo de manera automática...")
    else:
        print(f"✔️ Nueva sesión relacional inicializada con ID: {sesion_id}")

    print("\nCompilando prompt maestro optimizado...")
    # main.py (Sección del bucle modificada)
# Reemplaza desde el "while True:" en tu main.py actual

    tareas_fondo = set() # Contenedor para evitar que el recolector de basura elimine las tareas en ejecución

    print(f"\n¡Entorno listo! Escribe 'salir' para cerrar la sesión y consolidar.")
    print(f"Escribe ':abort' para cerrar de forma forzada simulando un apagón.\n")
    
    while True:
        contexto_base, historial_l4_acotado = cargar_contexto_base_ordenado(proyecto_activo, sesion_id)
        
        usuario = input("Tú: ").strip()
        if not usuario:
            continue
        if usuario.lower() == "salir":
            break
        if usuario == ":abort":
            print("\n[!] Abortando programa. El estado permanece a salvo en SQLite.")
            sys.exit(0)
            
        guardar_mensaje_en_vivo(sesion_id, "user", usuario)
        
        print(f"\n{modelo_activo}: ", end="", flush=True)
        respuesta_completa = ""
        
        stream = await consultar_modelo_async(modelo_activo, usuario, contexto_base, historial_l4_acotado)
        async for chunk in stream:
            texto_fragmento = chunk['message']['content']
            print(texto_fragmento, end="", flush=True)
            respuesta_completa += texto_fragmento
        print("\n")
        
        guardar_mensaje_en_vivo(sesion_id, "assistant", respuesta_completa)

        # ----------------------------------------------------------------------
        # GATILLO EN CALIENTE: Destilación asíncrona del Nivel 3 en segundo plano
        # ----------------------------------------------------------------------
        async def proceso_fondo_n3(u, r, s_id):
            resultado = await destilar_turno_n3_async(modelo_activo, u, r)
            if resultado:
                preg_saneada, resp_saneada = resultado
                # Inyección quirúrgica inmediata en la tabla relacional de Nivel 3
                with conectar_temporal_para_main() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO nivel3_qna (sesion_id, pregunta, respuesta, timestamp)
                        VALUES (?, ?, ?, DATETIME('now'))
                    """, (s_id, preg_saneada, resp_saneada))
                    conn.commit()

        # Lanzamos la tarea de fondo de forma no bloqueante
        tarea = asyncio.create_task(proceso_fondo_n3(usuario, respuesta_completa, sesion_id))
        tareas_fondo.add(tarea)
        tarea.add_done_callback(tareas_fondo.discard)

    # 5. VENTANA DE CONSOLIDACIÓN RÁPIDA (Al escribir 'salir')
    print("\n" + "="*60)
    print("PROCESANDO ENTORNO: Finalizando tareas en segundo plano y consolidando...")
    
    # Aseguramos que todas las micro-destilaciones pendientes terminen antes de cerrar
    if tareas_fondo:
        await asyncio.gather(*tareas_fondo)

    # Recuperamos todos los Q&A guardados limpiamente durante el día para compilar L2 y L1
    with conectar_temporal_para_main() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT pregunta, respuesta FROM nivel3_qna WHERE sesion_id = ? ORDER BY id ASC", (sesion_id,))
        filas_qna = cursor.fetchall()
        
    if filas_qna:
        texto_qna_consolidado = "\n".join([f"Q: {f[0]}\nA: {f[1]}\n---" for f in filas_qna])
        
        # Generación veloz de L2 y L1 (El modelo solo lee un par de líneas limpias)
        commit_propuesto, resumen_propuesto = await destilar_cascada_final_async(modelo_activo, texto_qna_consolidado)
        
        while True:
            print("\n=== AUDITORÍA DE MEMORIA OPTIMIZADA EN CALIENTE ===")
            print(f"[PROYECTO]: {proyecto_activo.upper()}")
            print(f"[NIVEL 1 - COMMIT PROPUESTO]: {commit_propuesto}")
            print(f"\n[NIVEL 2 - RESUMEN ARQUITECTÓNICO]:\n{resumen_propuesto}")
            print(f"[NIVEL 3]: {len(filas_qna)} bloques Q&A guardados en vivo con éxito.")
            print("="*60)
            
            opc = input("\nOpciones: [1] Aprobar y Guardar | [2] Modificar Commit | [3] Descartar\nSelecciona: ").strip()
            if opc == "1":
                finalizar_y_consolidar_sesion(sesion_id, commit_propuesto, resumen_propuesto)
                print("\n✔️ ¡Éxito! Estructura relacional consolidada velozmente.")
                break
            elif opc == "2":
                commit_propuesto = input("\nNuevo Commit:\n> ").strip()
            elif opc == "3":
                print("\nCambios descartados.")
                break
    else:
        print("\nNo se registraron interacciones técnicas relevantes en esta sesión. Cerrando de forma limpia.")


def conectar_temporal_para_main():
    """Función de soporte interna exclusiva para la lectura final del chat en main."""
    import sqlite3
    from src.config import DB_PATH
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    # Arrancamos el bucle de eventos asíncronos nativo de Python
    asyncio.run(main())
