```text
            --     -                     
           -x.      -    -              
          -x##       -####-            
          *###x-      -*####xx*       
         -x######-       *##.____       
         *########.              
         x# *#######*     -x##x   
    .#################*- .#########x    
     -*#############*######*x#####*     
       -*###########x  *x* -####.       
        -############x.    x###x        
         x###x-x######*-   -x##*        
         *##x  -*####x       x#.        
         -##-     -##-       .#         
          *#-       *        ##         
          -x-         ...####x          
            -      .########x-          
                  -########x-           
                   x#####x.             
                    -**.-   
         
              ARCHMIME
         SOFTWARE + GAMES

=======================================

Para el portafolio de [@ArchMime](https://github.com/ArchMime/)
```


# mimmery - Local SLM Hierarchical Memory Interface

Una arquitectura ligera de Persistencia de Memoria Jerárquica (RAG Nativo) diseñada para Modelos de Lenguaje Pequeños (SLMs) locales. Este proyecto optimiza la inyección de contexto histórico operando bajo restricciones estrictas de hardware (CPU de 4 hilos, 8 GB de RAM y sin GPU dedicada).

## 🚀 El Problema Técnico y la Solución

Los modelos de lenguaje locales sufren de "amnesia" entre ejecuciones independientes. Al inyectar historiales de chat masivos para resolver esto, el costo computacional de la ventana de atención crece de forma **cuadrática** (O(N²)), saturando la CPU y forzando el uso de *Swap* en equipos de bajos recursos.

Este proyecto resuelve el problema implementando un **sistema RAG jerárquico de tres niveles** sobre SQLite, actuando como un filtro inteligente que inyecta únicamente los fragmentos de memoria críticos:

1. **Nivel 1 (Índice - Git Commit):** Una frase técnica imperativa (<150 caracteres) que mapea cronológicamente todas las sesiones pasadas.
2. **Nivel 2 (Resumen Técnico):** Viñetas estructuradas con decisiones y datos clave generados automáticamente al cerrar la sesión.
3. **Nivel 3 (Historial Crudo):** Los últimos mensajes de la conversación activa decodificados desde JSON.

## 🛠️ Arquitectura del Proyecto

El software aplica estrictamente el principio de **Responsabilidad Única** modularizando la lógica en el directorio `src/`:

```text
.
├── main.py                # Interfaz de línea de comandos (CLI) y orquestación.
├── requirements.txt       # Dependencias congeladas del entorno.
├── LICENSE                # Licencia GNU GPLv3.
└── src/
    ├── __init__.py        # Inicializador del paquete modular.
    ├── config.py          # Centralización de hiperparámetros de Ollama y prompts.
    ├── database.py        # Ciclo de vida de SQLite y compilación del contexto.
    └── model_client.py    # Abstracción del cliente de Ollama y generadores de streaming.
```

## ⚡ Características Principales

- **Streaming de Tokens Corregido:** Consumo dinámico de respuestas fragmento a fragmento para evitar congelamientos de interfaz en CPU.
- **Ventana de Contexto Configurable:** Permite definir en tiempo real cuántos registros del Nivel 2 y 3 inyectar al prompt del sistema.
- **Aprobación Humana en Bucle (HITL):** Menú interactivo antes del guardado físico para auditar, editar o descartar los resúmenes generados por la IA.
- **Agnóstico al Modelo:** Compatible nativamente con cualquier SLM cuantizado en formato GGUF a través de Ollama (`llama3.2:1b`, `gemma3:1b`, etc.).

## 📦 Instalación y Uso

1. Clonar el repositorio y activar el entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Asegurarse de tener Ollama corriendo y el modelo deseado instalado:
   ```bash
   ollama run gemma3:1b
   ```
4. Ejecutar la interfaz:
   ```bash
   python main.py
   ```

## 📄 Licencia

Este proyecto está bajo la Licencia GNU GPLv3 - ver el archivo [LICENSE](LICENSE) para más detalles.
