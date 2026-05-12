import os
import pandas as pd
import numpy as np
from db.conex import obtener_Conex


RUTA_CSV = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn.csv")
def ingestas():
    obtenerDato = obtener_Conex()
    try:
        print("Iniciando proceso de lectura de datos...")
        data = pd.read_csv(RUTA_CSV, sep=",")
        
        print("Iniciando proceso de Ingesta de datos...") 
        
        data.to_sql(name ="clientes_telecom", 
                    con = obtenerDato, 
                    if_exists = "append", 
                    index = False)
        
        print("Datos insertados correctamente en la base de datos.")
        print(f"Ingesta completada: {len(data)} registros cargados.")
        
    except Exception as e:
        print(f"Error al insertar datos en la base de datos: {e}")
        
    finally:
        print("Proceso de ingesta finalizado.")
        obtenerDato.dispose()
        
# ingestas()