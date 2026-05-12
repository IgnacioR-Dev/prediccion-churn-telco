
from pipeline.ingesta import ingestas
from pipeline.limAndTransformacion import DataCleaningPipeline
from pipeline.featureEngeneering import FeatureEngineering

def main():
    print("Proceso de ingesta completado.")
    ingestas()
    
    pipeline = DataCleaningPipeline()
    fe = FeatureEngineering()
    pipeline.add_step('remove_duplicados', pipeline.remove_duplicados)
    pipeline.add_step('remove_valor_faltante', pipeline.remove_valor_faltante)
    pipeline.add_step('remove_inconsistentes', pipeline.remove_inconsistente)
    pipeline.add_step('ingenieria_caracteristicas', fe.transform)



if __name__ == "__main__": 
    main()
