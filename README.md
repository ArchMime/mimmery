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

Una arquitectura ligera de Persistencia de Memoria Jerárquica diseñada para Modelos de Lenguaje Pequeños (SLMs) locales. Este proyecto optimiza la inyección de contexto histórico operando bajo restricciones estrictas de hardware (CPU de 4 hilos, 8 GB de RAM y sin GPU dedicada).

## 🚀 El Problema Técnico y la Solución

Los modelos de lenguaje locales sufren de "amnesia" entre ejecuciones independientes. Al inyectar historiales de chat masivos para resolver esto, el costo computacional de la ventana de atención crece de forma cuadrática (O(N²)), saturando la CPU y forzando el uso de Swap en equipos de bajos recursos.

Este proyecto resuelve el problema implementando un sistema relacional jerárquico de cuatro niveles sobre SQLite, actuando como un filtro inteligente que mantiene un consumo de tokens planísimo y controlado matemáticamente:

1. Nivel 1 (Índice - Git Commit): Una frase técnica imperativa (<100 caracteres) que indexa cronológicamente las sesiones pasadas.
2. Nivel 2 (Resumen Técnico): Viñetas estructurales densas con decisiones de arquitectura y datos clave.
3. Nivel 3 (Diccionario Q&A Saneado): Bloques limpios de Pregunta/Solución de código extraídos en tiempo real.
4. Nivel 4 (Chat Crudo): Ventana deslizante efímera limitada estrictamente a las últimas interacciones vivas en la terminal.

## 🛠️ Arquitectura del Proyecto

El software aplica estrictamente el principio de **Responsabilidad Única** modularizando la lógica en el directorio `src/`:

```text
.
├── main.py                # Bucle de interacción CLI y orquestación asíncrona.
├── auditar_db.py          # Script de diagnóstico e integridad relacional.
├── requirements.txt       # Dependencias congeladas del entorno.
├── LICENSE                # Licencia GNU GPLv3.
└── src/
    ├── __init__.py        # Inicializador del paquete.
    ├── config.py          # Hiperparámetros de Ollama, límites de nivel y prompts.
    ├── model_client.py    # Cliente AsyncClient de Ollama y tubería de destilación.
    └── database/          # Submódulo relacional normalizado
        ├── __init__.py    # Fachada única de la API de datos.
        ├── connection.py  # Conexión física a SQLite y DDL de tablas.
        ├── messages.py    # Persistencia inmediata del chat en vivo (Nivel 4).
        ├── queries.py     # Consultas quirúrgicas y compilación del Prompt Maestro.
        └── sessions.py    # Ciclo de vida y resiliencia de jornadas de trabajo.

```

## ⚡ Características Principales

- Destilación Asíncrona en Caliente: El Nivel 3 (Q&A) se procesa en segundo plano mediante asyncio.create_task inmediatamente después de cada mensaje, eliminando la sobrecarga computacional al cerrar la sesión.
- Resiliencia y Blindaje de Datos: El chat se guarda mensaje a mensaje. Si ocurre un apagón, el sistema detecta la sesión colgada y la restaura automáticamente al reiniciar.
- Eterno Retorno del Prompt Maestro: Compilación compacta oculta (~1,400 tokens fijos) relanzada en cada interacción para guiar la atención del modelo sin saturar su memoria.
- Agnóstico al Modelo: Optimizado para el comportamiento y atención de SLMs cuantizados (llama3.2:1b, gemma3:1b, qwen2.5-coder, etc.).

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
