import os
import pandas as pd
import numpy as np

# ── Carga de datos
ruta = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn-limpio.csv")
# ruta = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn.csv")
# ruta = os.path.join(os.path.dirname(__file__), "..", "..", "data", "02_Base_Customer-Churn.csv")
data = pd.read_csv(ruta, sep=",")

pesos = {
    "nulos": 0.3,
    "duplicados": 0.2,
    "inconsistencia": 0.3,
    "outliers": 0.2,
}

class Validador:
    # Constructor que recibe el dataset a validar
    def __init__(self, data):
        self.data = data

    def nulos(self, columna):
        cantidad_nulos = self.data[columna].isna().sum()
        return cantidad_nulos == 0   

    def duplicados(self, columna):
        return self.data[columna].is_unique  

    # atipicos
    def outliers(self, columna):
        numero = pd.to_numeric(self.data[columna], errors="coerce").dropna()
        if len(numero) == 0:
            return True   # si no hay datos, no evaluamos
        
        Q1 = numero.quantile(0.25)
        Q3 = numero.quantile(0.75)
        IQR = Q3 - Q1
        
        if IQR == 0:
            return True   # si no hay variabilidad, no consideramos outliers
        
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        return ((numero >= limite_inferior) & (numero <= limite_superior)).all() 

    # Incontistencias
    def inconsistencias(self, columna):
        numeric_cols = self.data[[columna]].select_dtypes(include=["number"])
        for col in numeric_cols.columns:
            if (numeric_cols[col] < 0).any():
                return True

        cat_cols = self.data.select_dtypes(include=["object", "string"])
        for col in cat_cols.columns:
            values = cat_cols[col].dropna().astype(str)
            normalized = values.str.strip().str.lower()
            # compara los datos sucios, con una limpieza rapida, si son iguales
            # no hay inconsistencias, pero si los valores son distintos es xq si hay 
            if len(values.unique()) != len(normalized.unique()):
                return True

        return False
    
    def calcular_score(self, checks):
        suma_puntos = 0.0
        suma_pesos = 0.0

        for check, resultado in checks.items():
            if check not in pesos:
                continue                            
            peso = pesos[check] 
            if resultado:
                suma_puntos += peso  
            else:
                suma_puntos += 0    
            suma_pesos += peso                      
        if suma_pesos == 0:
            return 1.0                             
        return suma_puntos / suma_pesos             

    # generar un reporte con los resultados
    def evaluar(self):
        reporte = {}
        for columna in self.data.columns:
            checks = {}
            numeric_cols = pd.api.types.is_numeric_dtype(self.data[columna])
            checks["nulos"] = self.nulos(columna)
            checks["outliers"] = self.outliers(columna) if numeric_cols else True
            
            if columna.lower().endswith("id"):
                checks["duplicados"] = self.duplicados(columna)
            else:
                checks["inconsistencia"] = self.inconsistencias(columna)
            if numeric_cols == "numerico":
                checks["outliers"] = self.outliers(columna)

            reporte[columna] = checks
        return reporte
    
    def imprimir(self, reporte):
        total = len(reporte)
        
        print("\n--------------------------------")
        print("Reporte de validación de datos\n")
        print(f"Total de columnas evaluadas: {len(reporte)}")
        print(f"Total de filas evaluadas: {len(self.data)}")
        print("--------------------------------")
        
        nulos = (sum(1 for c in reporte.values() if c.get("nulos")) / total) * 100
        duplicados = (sum(1 for c in reporte.values() if c.get("duplicados")) / total) * 100
        inconsistencias = (sum(1 for c in reporte.values() if c.get("inconsistencias")) / total) * 100
        outliers = (sum(1 for c in reporte.values() if c.get("outliers")) / total) * 100
        scores_cols = [self.calcular_score(c) for c in reporte.values()]
        score_general = round(np.mean(scores_cols) * 100, 2)
        
        print(f"Nulos               : {round(nulos, 1)}%")
        print(f"Duplicados          : {round(duplicados, 1)}%")
        print(f"Inconsistencia      : {round(inconsistencias, 1)}%")
        print(f"Outliers/Atipicos   : {round(outliers, 1)}%")
        print("--------------------------------")
        
        print(f"Score general del dataset: {score_general}%")
    
# ── Ejecución del script 
validador = Validador(data) 
validador.imprimir(validador.evaluar())
