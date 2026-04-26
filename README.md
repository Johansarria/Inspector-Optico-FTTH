# FiberMind Analytics 🤖📊

Un sistema inteligente, autónomo y privado diseñado para transformar datos crudos de hardware en diagnósticos accionables utilizando **Modelos de Lenguaje Locales (LLMs)**. 

Este proyecto implementa una arquitectura **Text-to-SQL** y análisis de datos en lenguaje natural para optimizar las operaciones de mantenimiento preventivo (O&M). Aunque el MVP actual está especializado en el análisis forense de redes de fibra óptica (FTTH) mediante trazas OTDR, la arquitectura modular es extrapolable a cualquier sector que requiera detección de anomalías y auditoría de infraestructura crítica.

---

## 🌟 Características Principales

### 1. Motor Analítico Asistido por LLM (Soberanía de Datos)
- **Razonamiento Local (Costo $0):** Impulsado por **Ollama** ejecutando modelos ultraligeros optimizados para código (ej. `qwen2.5-coder:1.5b` o `llama3`), garantizando que los datos de infraestructura corporativa nunca salgan hacia APIs de terceros.
- **Text-to-SQL Dinámico:** Capacidad del agente para interpretar intenciones operativas complejas en lenguaje natural y transformarlas en consultas SQL precisas en tiempo real.
- **Análisis de Fallas (Fault Analysis):** El LLM no solo extrae datos, sino que cruza atenuaciones y distancias para diagnosticar la viabilidad del enlace.

### 2. Pipeline ETL para Datos Binarios Industriales
- **Extracción y Transformación:** Lectura directo y decodificación de archivos binarios cerrados (Estándar Telcordia SR-4731 / `.sor`) generados por equipos de hardware.
- **Clasificación Heurística:** Algoritmos en Python que procesan matrices de datos (distancia, reflectancia, atenuación) para identificar e indexar eventos físicos (empalmes, anomalías, splitters).
- **Carga Estructurada:** Volcado automático en una base de datos relacional local (`SQLite`) optimizada para consultas analíticas rápidas.

### 3. Interfaz Agéntica Multicanal (Telegram MVP)
- **Democratización de los Datos:** Permite a ingenieros y técnicos de campo interactuar con la base de datos de infraestructura directamente desde sus teléfonos sin necesidad de saber SQL.
- **Enrutamiento de Intenciones (Intent Routing):** Sistema híbrido que responde instantáneamente a consultas recurrentes (ahorrando poder computacional) y deriva al LLM las preguntas analíticas complejas.
- **Generación Gráfica Automatizada:** Renderizado on-the-fly de reportes visuales y gráficas de dispersión (atenuación vs. distancia) utilizando `matplotlib`.

---

## 📂 Arquitectura del Sistema

```text
C:\MLpractica3\
├── ai_engine.py           # Core Analítico: LLM Local (Text-to-SQL + Razonamiento) vía Ollama
├── ftth_mcp_server.py     # Backend de Diagnóstico: Reglas de negocio y heurística de red
├── telegram_bot.py        # Interfaz Agéntica: Procesamiento de lenguaje natural y enrutador
├── import_otdr_traces.py  # Pipeline ETL: Ingesta de binarios .sor hacia base de datos relacional
├── setup_ftth_db.py       # Migraciones y setup de la base de datos (Inventario y Óptica)
├── run_tests.py           # Scripts de validación y benchmarking del sistema
├── utils_plot.py          # Motor de renderizado de datos (Matplotlib)
├── ftth_glossary.md       # Glosario técnico y nomenclatura O&M (CA, CTO, Mufa, etc.)
├── .env.example           # Plantilla de variables de entorno (Credenciales de Telegram)
├── .gitignore             # Configuración de exclusión para proteger archivos binarios y bases de datos
├── ftth_mantenimiento.db  # Data Warehouse local (SQLite)
├── TRAZAS/                # Data Lake: Almacenamiento de archivos binarios raw (.sor)
├── PLANOS/                # Archivos GIS/CAD de red local (Ignorados en GitHub por seguridad)
└── venv/                  # Entorno virtual de dependencias
```

---

## 🚀 Requisitos e Instalación

### Prerrequisitos
- Python 3.10+
- Ollama instalado y ejecutándose localmente como motor de IA.

### 1. Despliegue del Entorno
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install pyotdr python-telegram-bot matplotlib requests mcp python-dotenv
```

### 2. Inicialización del Modelo LLM Local
Descarga y levanta el modelo analítico en segundo plano:
```bash
ollama run qwen2.5-coder:1.5b
```

### 3. Ejecución del Pipeline ETL y Agente
1. Deposita los archivos binarios raw en la carpeta `TRAZAS/`.
2. Ejecuta el motor de ingesta para construir el Data Warehouse: `python import_otdr_traces.py`
3. Inicializa la interfaz conversacional: `python telegram_bot.py`

---

## 🧠 Capacidades Analíticas y Casos de Uso (Benchmark)
El agente ha sido validado bajo escenarios reales de Operaciones y Mantenimiento, demostrando las siguientes capacidades de interpretación:

**Auditoría de Inventario y Volumetría**
- **Prompt:** "¿Cuántas trazas tenemos cargadas?"
- **Respuesta de la IA:** "He procesado 33 registros en total, pertenecientes a la troncal principal (Cable 1)." ✅

**Detección Predictiva de Anomalías Críticas**
- **Prompt:** "¿Qué hilos del CA01 tienen fallas críticas (>0.5 dB)?"
- **Respuesta de la IA:** "Se detectaron 10 hilos con fallas críticas en el Cable 1 (ej. hilos 124, 126, 132, 65, 68). Requieren inspección operativa." ✅

**Localización Geográfica (Planos AutoCAD)**
- **Prompt:** "¿Dónde está el Empalme Norte 01?"
- **Respuesta de la IA:** "📍 Elemento 'EMPALME NORTE 01' localizado en Plano: SECTOR_FICTICIO_ZONA_A. Coordenadas: X: 1024.5, Y: -512.8." ✅

**Cálculo de Presupuesto y Diagnóstico de Viabilidad**
- **Prompt:** "¿Cómo llega el hilo 144 a la CTO?"
- **Respuesta de la IA:** "Pérdida acumulada: 0.58 dB. Proyectando una inyección de +3 dBm, la potencia de llegada estimada es +2.41 dBm. Estado operativo: Óptimo." ✅

---

## 🛠️ Estado del Proyecto y Roadmap (Naturaleza MVP)

**FiberMind Analytics** se encuentra actualmente en fase de **Producto Mínimo Viable (MVP)**. Como herramienta de ingeniería asistida por IA, su efectividad operativa está sujeta a las siguientes consideraciones:

1.  **Dependencia de Datos:** El razonamiento del agente es tan preciso como la calidad de las bases de datos relacionales provistas. La alimentación constante del *Data Warehouse* (SQLite) es esencial para la integridad de los diagnósticos.
2.  **Integración de Planos (CAD):** En esta fase, la dimensión espacial utiliza un modelo de indexación heurística sobre archivos `.dwg`. Para despliegues de producción masiva, se recomienda la transición a formatos abiertos (`.dxf`) o la integración directa con **APIs de terceros (ej. Autodesk Forge/APS)** para una extracción ETL automatizada y en tiempo real.
3.  **Escalabilidad del Modelo:** Aunque el MVP utiliza modelos ligeros locales para garantizar soberanía, la arquitectura es compatible con LLMs de mayor escala según los requisitos de latencia y complejidad del proyecto.

---
*Proyecto diseñado y desarrollado por **Johan Sarria** para la optimización de procesos O&M en redes FTTH.*
