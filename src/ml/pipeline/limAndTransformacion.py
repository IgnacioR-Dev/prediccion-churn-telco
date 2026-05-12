import os
import pandas as pd
import numpy as np

from featureEngeneering import FeatureEngineering

# ── Carga de datos
ruta = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn.csv")
data = pd.read_csv(ruta, sep=",")

class DataCleaningPipeline:

    def __init__(self, data):
        self.steps = []
        self.data = data
        self.data.columns = self.data.columns.str.lower().str.strip()
    
    #agregar funcion/ agregar paso
    def add_step(self, name, function):
        """Add a cleaning step."""
        self.steps.append({'name': name, 'function': function})
        
    def execute(self,data):
        results = []
        current_df = data.copy()
        
        for step in self.steps:
            try:
                current_df = step['function'](current_df)
                results.append({
                    'step': step['name'],
                    'status': 'success',
                    'rows_affected': len(current_df)
                })
                print(f"Paso '{step['name']}' exitoso. Filas afectadas: {len(current_df)}")
                print("filas anteriores:", len(data), "filas actuales:", len(current_df))
                print("\n--------------------------------------------------------------")
            except Exception as e:
                results.append({
                    'step': step['name'],
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"Error en el paso '{step['name']}': {e}")
                break
                
        return current_df, results
    
    def remove_duplicados(self, data, customerID="customerid"):
        print("Eliminando Duplicados...")
        print("\n----------------------------------------------")
        return data.drop_duplicates(subset=[customerID])
    
    def remove_valor_faltante(self, data):
        # busca valores faltantes espacio blanco
        data = data.replace(r'^\s*$', np.nan, regex=True)
        missing_values = data.isnull().sum()
        # elimina fila con valores faltantes
        data = data.dropna()
        
        print("Eliminado {} valores faltantes".format(missing_values.sum()))
        return data
    
    def remove_inconsistente(self, data):
        text_cols = data.select_dtypes(include=["object", "string"])
        num_cols = data.select_dtypes(include=["number"]).columns
        
        for column in data.columns:
            if column in text_cols:
                data[column] = data[column].str.strip().str.lower()
                # print(f"Limpiando numeros en: {column}")
            if column in num_cols:
                data = data[(data[num_cols] >= 0).all(axis=1)]
                # print("Limpiando Inconsistencias de columnas numericas")
        return data
        
    # def remove_Outliers():
    #     pass
    
pipeline = DataCleaningPipeline(data)
fe = FeatureEngineering()


pipeline.add_step('remove_duplicados', pipeline.remove_duplicados)
pipeline.add_step('remove_valor_faltante', pipeline.remove_valor_faltante)
pipeline.add_step('remove_inconsistentes', pipeline.remove_inconsistente)
# pipeline.add_step('remove_Outliers', pipeline.remove_Outliers)
pipeline.add_step('ingenieria_caracteristicas', fe.transform)


cleaned_data, results = pipeline.execute(data)
cleaned_data.to_csv(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn-limpio.csv"), index=False)
data_limpia = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn-limpio.csv"))
