
import os
import pandas as pd

from ml.pipeline.limAndTransformacion import DataCleaningPipeline
from ml.pipeline.ingesta import ingestas, ingesta_limpia

ruta = os.path.join(os.path.dirname(__file__), ".." ,"data", "Telco-Customer-Churn.csv")

def main():
    ingestas()   
    print("\n----------------------------------------------")
    
    data = pd.read_csv(ruta, sep=",")
    cleaner = DataCleaningPipeline()
    cleaner.llamado(data)
    
    ingesta_limpia()
    print("\n----------------------------------------------")
    
if __name__ == "__main__": 
    main()
