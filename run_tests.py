import asyncio
from ai_engine import ask_ai

async def run_documentation_tests():
    print("--- INICIANDO PRUEBAS DE SISTEMA ---")
    
    test_questions = [
        "¿Cuántas trazas hay cargadas en total?",
        "¿Qué hilos tienen fallas críticas?",
        "¿Cuál es el presupuesto óptico para el hilo 65?",
        "¿Dónde están los splitters del hilo 144?"
    ]
    
    results = []
    for q in test_questions:
        print(f"Pregunta: {q}")
        response = await ask_ai(q)
        results.append(f"**Pregunta:** {q}\n**Respuesta:** {response}\n")
        print(f"Respuesta obtenida.\n")
        
    with open("pruebas_sistema.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    
    print("--- PRUEBAS COMPLETADAS Y GUARDADAS EN pruebas_sistema.txt ---")

if __name__ == "__main__":
    asyncio.run(run_documentation_tests())
