import sqlite3
import requests
import json
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Forzar salida en UTF-8 para evitar errores de encoding en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuración Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5-coder:1.5b"
DB_PATH = "ftth_mantenimiento.db"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

SCHEMA_INFO = """
Base de datos: ftth_mantenimiento.db

TABLAS:
1. eventos_otdr:
   - id (INTEGER), id_cable (INTEGER), id_hilo (INTEGER), distancia_km (REAL), 
     tipo_evento (TEXT) (ej: 'reflection', 'splitter'), atenuacion_db (REAL)
2. inventario_geografico:
   - id (INTEGER), nombre_elemento (TEXT) (ej: 'EMPALME 3'), plano (TEXT), x (REAL), y (REAL)

METADATOS FIBERMIND:
- Nombre: FiberMind Analytics (O&M AI Agent)
- Modelo: Ollama / qwen2.5-coder
- Contexto Óptico: Cabecera C++ (+3 a +5 dBm). Doble cascada splitters 1x8 (10.5 dB cada uno).
- Presupuesto Objetivo: -18 dBm a -22 dBm en CTO.
- Umbral Crítico: Empalme > 0.5 dB.
"""

SYSTEM_PROMPT = f"""
{SCHEMA_INFO}

Eres "FiberMind Analytics", un Agente de IA especializado en infraestructura FTTH. 
Tu propósito es servir de puente entre datos OTDR, planos AutoCAD y el personal operativo.

REGLAS DE RAZONAMIENTO:
1. Análisis de Fallas: Si detectas pérdida alta, calcula impacto en potencia (Potencia = 3 - Suma pérdidas).
2. Búsqueda Geográfica: Si preguntan por ubicación, usa SQL para buscar en 'inventario_geografico' y devuelve X, Y.
3. Tono: Profesional, técnico y conciso. Usa términos: Mufa, Sangría, CTO, Empalme.
4. NUNCA inventes coordenadas ni atenuaciones.

TAREA: Traduce la pregunta del usuario a SQL de SQLite. 
REGLA ESTRICTA: Responde SOLO con el código SQL crudo, sin marcas markdown, ni explicaciones.
"""

def is_greeting(text):
    text = text.lower().strip()
    greetings = ["hola", "buenos dias", "buenas", "hey", "hola bot", "saludos", "que tal", "quien eres"]
    return any(g in text for g in greetings) and len(text) < 15

def query_database(sql):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return results, column_names
    except Exception as e:
        return str(e), None

async def ask_ai(question):
    # Filtro de saludos (Costo $0 local)
    if is_greeting(question):
        return "¡Hola! 👋 Soy FiberMind Analytics, tu Agente IA local (Ollama). Estoy listo para analizar la red de Chiminangos sin límites de cuota. ¿Qué consulta técnica tienes?"

    # 1. Generar SQL con Ollama
    prompt_sql = f"{SYSTEM_PROMPT}\nPregunta: {question}"
    
    try:
        print(f"🧠 Generando SQL con Ollama para: {question}...")
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt_sql,
            "stream": False,
            "options": {"temperature": 0.0}
        }, timeout=60) # Aumentar timeout a 60 segundos
        sql = response.json()['response'].strip()
        # Limpieza básica
        sql = sql.replace("```sql", "").replace("```", "").strip()
        
        if not sql.lower().startswith("select"):
             return sql # Si no es SQL, es una respuesta directa de la IA

        print(f"⚙️ SQL Generado: {sql}")
        results, columns = query_database(sql)
        print(f"📊 Resultados DB: {results}")
        
        if isinstance(results, str):
            return f"Error en SQL local: {results}"

        # 2. Interpretar resultados con Ollama
        print("✍️ Interpretando resultados con Ollama...")
        prompt_interpret = f"""
        Pregunta: {question}
        SQL: {sql}
        Resultados: {results} (Columnas: {columns})
        Tarea: Explica estos resultados de forma amigable y técnica para un ingeniero de fibra óptica en español.
        """
        
        response_final = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt_interpret,
            "stream": False,
            "options": {"temperature": 0.5}
        }, timeout=60)
        final_answer = response_final.json()['response'].strip()
        print("✅ Respuesta final generada.")
        return final_answer

    except requests.exceptions.ConnectionError:
        return "❌ Error: Ollama no está respondiendo. Asegúrate de haber ejecutado 'ollama run qwen2.5-coder:1.5b' en tu terminal."
    except Exception as e:
        return f"❌ Error inesperado en motor local: {e}"

if __name__ == "__main__":
    import asyncio
    async def test():
        print(await ask_ai("cuantos hilos hay?"))
    asyncio.run(test())
