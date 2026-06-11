from pipeline.ingesta_datos import ejecutar_ingesta
from pipeline.validador import Validador
from pipeline.limpieza_transformacion import ejecutar_transformacion
from models.train_model import entrenar_modelo
from models.test_model import testear_modelo
import pandas as pd
import os 

# ── Carga de datos para validación
ruta = os.path.join(os.path.dirname(__file__), "..", "data", "02_Base_Customer-Churn.csv")
df = pd.read_csv(ruta, sep=";")

validador = Validador(df) # Instancia del validador con el dataset cargado

def main():
    try:
        print("-"*100)
        print("Iniciando pipeline de datos...\n")
        ejecutar_ingesta()

        print("\nVerificando calidad de datos con el validador...")
        validador.imprimir(validador.evaluar())
        print("-"*100)
        print("Ejecutando limpieza y transformación...")
        ejecutar_transformacion()
        print("-"*100)
        print("\nPipeline de datos finalizado.")

        print("="*100)
        print("\nEjecutando entrenamiento del modelo...")
        entrenar_modelo()
        print("\nEntrenamiento del modelo finalizado.")
        
        print("="*100)
        print("\nEjecutando pruebas del modelo...")
        testear_modelo()
        print("\nPruebas del modelo finalizadas.")
        print("="*100)
        
    except RuntimeError as e:
        print(f"Error en el pipeline: {e}")


if __name__ == "__main__":
    main()