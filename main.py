# main.py
from src.database import inicializar_db, obtener_proyectos_unicos, cargar_contexto_dinamico, guardar_sesion
from src.model_client import listar_modelos_locales, consultar_modelo, autogenerar_memorias
from src.config import LIMITE_N2_DEFECTO, LIMITE_N3_DEFECTO

def solicitar_limite(tipo_nivel, defecto):
    entrada = input(f"Cantidad de registros para {tipo_nivel} [Por defecto {defecto}]: ").strip()
    return int(entrada) if entrada.isdigit() else defecto

def main():
    inicializar_db()
    print("=== INTERFAZ DE MEMORIA PERSISTENTE MODULAR ===")
    
    # 1. SELECCIÓN DE MODELO
    modelos = listar_modelos_locales()
    if not modelos:
        print("\n[!] Error: No se detectó Ollama ejecutándose o no tienes modelos instalados.")
        return
        
    print("\nModelos disponibles:")
    for i, model in enumerate(modelos, start=1):
        print(f" [{i}] {model}")
    sel_m = input("\nSelecciona el número del modelo: ").strip()
    modelo_activo = modelos[int(sel_m) - 1] if (sel_m.isdigit() and 1 <= int(sel_m) <= len(modelos)) else modelos[0]
    print(f"> Modelo activo: '{modelo_activo.upper()}'")

    # 2. SELECCIÓN DE PROYECTO
    proyectos = obtener_proyectos_unicos()
    print("\nProyectos activos en base de datos:")
    print(" [0] GLOBAL (Cargar historial general de todo el sistema)")
    for i, proj in enumerate(proyectos, start=1):
        print(f" [{i}] {proj}")
        
    seleccion = input("\nSelecciona un número o escribe uno NUEVO: ").strip()
    if seleccion == "0" or seleccion.lower() == "global":
        proyecto_activo = "global"
    elif seleccion.isdigit() and 1 <= int(seleccion) <= len(proyectos):
        proyecto_activo = proyectos[int(seleccion) - 1]
    else:
        proyecto_activo = seleccion if seleccion else "general"
    print(f"> Proyecto asignado: '{proyecto_activo.upper()}'")

    # 3. CONFIGURACIÓN DINÁMICA DE CONTEXTO
    print("\n--- Ajustes de Ventana de Contexto ---")
    limite_n2 = solicitar_limite("Nivel 2 (Resúmenes Técnicos)", LIMITE_N2_DEFECTO)
    limite_n3 = solicitar_limite("Nivel 3 (Conversación Cruda)", LIMITE_N3_DEFECTO)
    
    print("\nCompilando memoria histórica...")
    contexto_previo = cargar_contexto_dinamico(proyecto_activo, limite_n2, limite_n3)
    
    # 4. BUCLE DE CONVERSACIÓN (STREAMING CORREGIDO)
    historial_sesion = []
    print(f"\n¡Entorno listo! Escribe 'salir' para finalizar.\n")
    
    while True:
        usuario = input("Tú: ").strip()
        if not usuario:
            continue
        if usuario.lower() == "salir":
            break
            
        historial_sesion.append({"role": "user", "content": usuario})
        
        print(f"\n{modelo_activo}: ", end="", flush=True)
        respuesta_completa = ""
        
        # Consumo correcto del generador fragmento por fragmento
        stream = consultar_modelo(modelo_activo, usuario, contexto_previo, historial_sesion[:-1])
        for chunk in stream:
            texto_fragmento = chunk['message']['content']
            print(texto_fragmento, end="", flush=True)
            respuesta_completa += texto_fragmento
        print("\n")
        
        historial_sesion.append({"role": "assistant", "content": respuesta_completa})

    # 5. VENTANA DE APROBACIÓN HUMANA
    if historial_sesion:
        print("\n" + "="*50)
        print("PROCESANDO CIERRE: Generando propuestas de memoria...")
        commit_propuesto, resumen_propuesto = autogenerar_memorias(modelo_activo, historial_sesion)
        
        while True:
            print("\n=== REVISIÓN DE MEMORIA ANTES DE GUARDAR ===")
            print(f"[PROYECTO]: {proyecto_activo}")
            print(f"[NIVEL 1 - COMMIT]: {commit_propuesto}")
            print(f"\n[NIVEL 2 - RESUMEN TÉCNICO]:\n{resumen_propuesto}")
            print("="*50)
            print("\nOpciones: [1] Guardar | [2] Editar Commit | [3] Editar Resumen | [4] Cambiar Proyecto | [5] Descartar")
            
            opc = input("Selecciona una opción: ").strip()
            if opc == "1":
                guardar_sesion(proyecto_activo, commit_propuesto, resumen_propuesto, historial_sesion)
                print("\n¡Registro inyectado con éxito en SQLite!")
                break
            elif opc == "2":
                commit_propuesto = input("\nNuevo Git Commit:\n> ").strip()
            elif opc == "3":
                print("\nNuevo Resumen (Presiona Enter y luego Ctrl+D o Ctrl+Z para terminar):")
                lineas = []
                while True:
                    try:
                        lineas.append(input())
                    except EOFError:
                        break
                resumen_propuesto = "\n".join(lineas).strip()
            elif opc == "4":
                proyecto_activo = input("\nNuevo nombre de proyecto:\n> ").strip()
            elif opc == "5":
                print("\nSesión cerrada sin guardar cambios.")
                break

if __name__ == "__main__":
    main()
