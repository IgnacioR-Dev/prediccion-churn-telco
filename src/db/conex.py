from sqlalchemy import create_engine

engine = None
def obtener_Conex():
    global engine
    if engine is None:
        try:
            print("Creando conexión a la base de datos...")
            engine = create_engine("postgresql+psycopg2://Admin:Admin@database:5432/ia_data") 
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
    return engine

# obtener_datos()
# Test-NetConnection -ComputerName localhost -Port 5432  