# Inspector Óptico FTTH 🤖🔍

Un sistema inteligente, autónomo y privado para el monitoreo, auditoría y análisis de redes de fibra óptica (FTTH) enfocado en operaciones de **mantenimiento preventivo**.

Este proyecto combina el análisis forense de trazas OTDR con la potencia de la Inteligencia Artificial Local (Ollama) para permitir a los ingenieros de planta externa interactuar con su red usando lenguaje natural a través de Telegram.

---

## 🌟 Características Principales

### 1. Ingesta Binaria Telcordia (SR-4731)
- Procesamiento directo de archivos `.sor` nativos de equipos OTDR (ej. FHO5000).
- Extracción de distancia, atenuación y clasificación de eventos (reflexiones, empalmes, splitters) mediante la librería `pyotdr`.
- Volcado automático de datos en una base de datos local SQLite (`ftth_mantenimiento.db`).

### 2. Soberanía Tecnológica y Razonamiento Local (Costo $0)
- Motor NLP impulsado por **Ollama**. 
- *Nota: El modelo de IA es a elección del usuario. Para efectos de las pruebas iniciales y validación de esta arquitectura, se utilizó el modelo ultraligero `qwen2.5-coder:1.5b`.*
- Privacidad total: los datos de la infraestructura de red no salen a APIs externas ni nubes públicas.
- Generación de consultas dinámicas (Text-to-SQL) para interrogar la base de datos en tiempo real.

### 3. Asistente O&M (Telegram Bot)
- **Comandos directos:** 
  - `/auditar` para buscar empalmes críticos (>0.5 dB) en todo un cable.
  - `/hilo [n]` para obtener una radiografía técnica instantánea de un hilo específico.
- **Lenguaje Natural:** Capacidad para procesar preguntas operativas como *"¿Cuántas trazas tenemos?"* o *"¿Cuál es la longitud del hilo 285?"*.
- **Visualización en Tiempo Real:** Generación y envío automático de gráficas de atenuación vs. distancia usando `matplotlib`.

### 4. Lógica de Mantenimiento Preventivo
- **Control de Presupuesto Óptico:** Cálculo automático de potencia estimada de llegada a CTO (asumiendo +3 dBm en cabecera).
- **Detección por Exclusión:** Identifica si un hilo consultado está en uso (activo) si no cuenta con una traza de mantenimiento preventivo registrada.

---

## 📂 Arquitectura del Proyecto

```text
C:\MLpractica3\
├── ai_engine.py           # Motor NLP local (Text-to-SQL + Interpretación) usando Ollama
├── ftth_mcp_server.py     # Backend Core / Servidor MCP (Lógica de diagnóstico de red)
├── telegram_bot.py        # Interfaz de usuario, enrutador de intenciones y envío de gráficas
├── import_otdr_traces.py  # Script batch para ingestar archivos .sor y poblar la DB
├── utils_plot.py          # Motor de renderizado (Matplotlib) para dibujar las trazas ópticas
├── ftth_mantenimiento.db  # Base de datos SQLite (Generada en ejecución)
├── TRAZAS/                # Directorio contenedor de los archivos .sor
└── venv/                  # Entorno virtual de Windows (Python)
```

---

## 🚀 Requisitos e Instalación

### Prerrequisitos
- **Python 3.10+** (Entorno nativo de Windows)
- **Ollama** instalado y ejecutándose localmente.

### 1. Configurar Entorno Virtual
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar Dependencias
Las principales librerías requeridas son:
```powershell
pip install pyotdr python-telegram-bot matplotlib requests mcp
```

### 3. Descargar Modelo LLM
Abre una terminal paralela y ejecuta el modelo ultraligero para programación:
```bash
ollama run qwen2.5-coder:1.5b
```

---

## 🛠️ Uso y Operación

### 1. Poblar la Base de Datos
Deposita tus archivos `.sor` en la carpeta `TRAZAS` (respetando la estructura de carpetas) y ejecuta el importador:
```powershell
.\venv\Scripts\python.exe import_otdr_traces.py
```

### 2. Iniciar el Bot de Telegram
Asegúrate de que tu `BOT_TOKEN` y `AUTHORIZED_CHAT_ID` estén configurados en `telegram_bot.py`.
```powershell
.\venv\Scripts\python.exe telegram_bot.py
```

### 3. Interactuar
Abre Telegram y envía un mensaje al bot. Puedes usar los comandos `/start` o hablarle de forma natural gracias al **Intent Routing** programado para ahorrar recursos computacionales.

---

## 🧠 Dataset de Entrenamiento Interno (Reglas O&M)

El modelo local ha sido condicionado mediante *Few-Shot Prompting* con las siguientes reglas de negocio del sector telecomunicaciones:
1. **Auditoría General:** Conteos de hilos y cables.
2. **Alertas Críticas:** Identificación de eventos (no splitters) con pérdida `> 0.5 dB`.
3. **Presupuesto Óptico:** Estimación de potencia asumiendo origen ODF en `+3 dBm`. Umbral de alerta en `-27 dBm`.
4. **Inventario:** Localización de splitters (1er y 2do nivel) por punto kilométrico.

---

## 🧪 Registro de Pruebas Generales (Test Suite)

Se ejecutó una batería de pruebas de razonamiento local para validar la integración entre Ollama, la base de datos y la intencionalidad O&M:

1. **Prueba de Auditoría (Resumen General)**
   - *Pregunta:* "¿Cuántas trazas tenemos cargadas?"
   - *Resultado Esperado:* Conteo único de `id_hilo`.
   - *Resultado Obtenido:* "He procesado 33 trazas en total. Todas pertenecen al cable 1." ✅

2. **Prueba de Alertas Críticas**
   - *Pregunta:* "¿Qué hilos tienen fallas críticas?"
   - *Resultado Esperado:* Filtro de atenuación > 0.5 dB.
   - *Resultado Obtenido:* "Encontré 2 empalmes críticos. El más grave está en el Hilo 65 a 4.9 km con una pérdida de 18.88 dB." ✅

3. **Prueba de Presupuesto Óptico**
   - *Pregunta:* "¿Cuál es el presupuesto óptico para el hilo 144?"
   - *Resultado Esperado:* Cálculo `+3 dBm - Sum(Atenuación)`.
   - *Resultado Obtenido:* "El hilo 144 tiene una pérdida total de 0.58 dB. Potencia llegada estimada: +2.41 dBm. Estado: Óptimo." ✅

4. **Prueba de Inventario (Localización de Splitters)**
   - *Pregunta:* "¿Dónde están los splitters del hilo 61?"
   - *Resultado Esperado:* Extracción de eventos clasificados como splitters.
   - *Resultado Obtenido:* "Para el hilo 61, el Splitter de 1er Nivel detectado a 3.12 km, y el de 2do Nivel a 4.9 km." ✅

---
*Desarrollado para la optimización de procesos O&M en redes FTTH.*
