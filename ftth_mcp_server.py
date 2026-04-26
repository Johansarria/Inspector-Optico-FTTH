import sqlite3
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Inicializar el servidor MCP
mcp = FastMCP("Inspector Optico FTTH MCP")

# Ruta a la base de datos SQLite (Ajusta esta ruta según la ubicación real de tu DB)
DB_PATH = "ftth_mantenimiento.db"

def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # Configurar para que las filas se comporten como diccionarios
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def consultar_ruta_hilo(id_cable: int, id_hilo: int) -> str:
    """
    Busca en la base de datos de mantenimiento preventivo y devuelve todos los eventos 
    ópticos (empalmes, splitters, fin de fibra) registrados por el OTDR para un cable e hilo específicos.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ajusta el nombre de la tabla ('eventos_otdr') y columnas a tu esquema real
        query = '''
            SELECT distancia_km, tipo_evento, atenuacion_db 
            FROM eventos_otdr 
            WHERE id_cable = ? AND id_hilo = ?
            ORDER BY distancia_km ASC
        '''
        cursor.execute(query, (id_cable, id_hilo))
        eventos = cursor.fetchall()
        conn.close()
        
        if not eventos:
            return f"El hilo {id_hilo} no se encuentra en los registros de mantenimiento preventivo. Esto indica que probablemente es un **hilo en uso** (activo)."
            
        resultado = f"Radiografía de la ruta - Cable {id_cable}, Hilo {id_hilo}:\n"
        for ev in eventos:
            resultado += f" - Distancia: {ev['distancia_km']} km | Evento: {ev['tipo_evento']} | Pérdida: {ev['atenuacion_db']} dB\n"
            
        return resultado
        
    except sqlite3.Error as e:
        return f"Error en base de datos al consultar la ruta: {e}"
    except Exception as e:
        return f"Error inesperado del sistema: {e}"

@mcp.tool()
def auditar_empalmes_criticos(limite_db: float, id_cable: Optional[int] = None) -> str:
    """
    Busca en todos los registros aquellos eventos de empalme o curvatura cuya 
    pérdida supere un umbral crítico de decibelios (dB), ignorando los splitters normales.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Excluimos los splitters para no generar falsos positivos (suelen tener > 10dB)
        if id_cable is not None:
            query = '''
                SELECT id_cable, id_hilo, distancia_km, tipo_evento, atenuacion_db 
                FROM eventos_otdr 
                WHERE atenuacion_db > ? 
                AND id_cable = ?
                AND LOWER(tipo_evento) NOT LIKE '%splitter%'
                ORDER BY atenuacion_db DESC
            '''
            cursor.execute(query, (limite_db, id_cable))
        else:
            query = '''
                SELECT id_cable, id_hilo, distancia_km, tipo_evento, atenuacion_db 
                FROM eventos_otdr 
                WHERE atenuacion_db > ? 
                AND LOWER(tipo_evento) NOT LIKE '%splitter%'
                ORDER BY atenuacion_db DESC
            '''
            cursor.execute(query, (limite_db,))
            
        eventos = cursor.fetchall()
        conn.close()
        
        if not eventos:
            return f"Auditoría limpia. No se encontraron empalmes ni curvaturas con pérdida mayor a {limite_db} dB."
            
        resultado = f"⚠️ ALERTA DE MANTENIMIENTO PREVENTIVO ⚠️\n"
        resultado += f"Se encontraron {len(eventos)} empalmes críticos superando el umbral de {limite_db} dB:\n"
        
        for ev in eventos:
            resultado += f" - Cable: {ev['id_cable']} | Hilo: {ev['id_hilo']} | Distancia: {ev['distancia_km']} km | Evento: {ev['tipo_evento']} | Pérdida: {ev['atenuacion_db']} dB\n"
            
        return resultado
        
    except sqlite3.Error as e:
        return f"Error en base de datos al realizar la auditoría: {e}"
    except Exception as e:
        return f"Error inesperado del sistema: {e}"

if __name__ == "__main__":
    # Inicia el servidor MCP a través de stdio (Standard Input/Output)
    mcp.run()
