import pandas as pd
import pickle
import os
import pathlib

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier

from pipeline.filtro_correlacion import CorrelationFilter

#manejar conjuntos de datos con desequilibrios imblearn
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

def entrenar_modelo():
    # Crear carpeta de resultados
    rutaresults = os.path.join(os.path.dirname(__file__),"..","results")
    os.makedirs(rutaresults, exist_ok=True)

    # -------------------------------------------------
    # Cargar datos
    # -------------------------------------------------
    rutadata = os.path.join(os.path.dirname(__file__),"..","..","data","data_limpia.csv")
    data = pd.read_csv(rutadata, sep=";")


    # Variable objetivo
    target = "churn"
    
    X = data.drop(columns=[target])
    data[target] = data[target].map({"Yes": 1, "No": 0})
    y = data[target]
    

    # Revisa la distribución de la variable objetivo
    # En este caso se obtiene un gráfico de torta
    data[target].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                    labels=['No Churn', 'Churn'],
                                    figsize=(6, 6))
    plt.title("Distribución de variable objetivo", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(rutaresults, "distribucion_clases.png"), dpi=300, bbox_inches="tight")
    plt.close()
    
    # print(f" RUTA REAL DE RESULTS EN DOCKER: {pathlib.Path(rutaresults).resolve()}")
    # print(f" RUTA REAL DE DATA EN DOCKER: {pathlib.Path(rutadata).resolve()}")
    
    # -------------------------------------------------
    # Variables categóricas y numéricas
    # -------------------------------------------------
    categorical_features = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric_features = X.select_dtypes(exclude=["object"]).columns.tolist()

    # -------------------------------------------------
    # Preprocesamiento
    # -------------------------------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features
            )
        ],
        remainder="passthrough"
    )

    # -------------------------------------------------
    # Modelo
    # -------------------------------------------------
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=29,
        n_jobs=-1,
        class_weight="balanced"
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    # -------------------------------------------------
    # Split
    # -------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=29,
        stratify=y
    )

    # -------------------------------------------------
    # Entrenamiento
    # -------------------------------------------------
    pipeline.fit(X_train, y_train)

    # -------------------------------------------------
    # Guardar modelo
    # -------------------------------------------------
    rutamodels= os.path.join(os.path.dirname(__file__),"..","models")
    with open(os.path.join(rutamodels, "modelo_churn.pkl"), "wb") as f:
        pickle.dump(pipeline, f)
        print("Modelo guardado como modelo_churn.pkl")
    # print(f"RUTA REAL DE MODELS EN DOCKER: {pathlib.Path(rutamodels).resolve()}")
    
    # -------------------------------------------------
    # Guardar X_test e y_test
    # -------------------------------------------------
    rutadata = os.path.join(os.path.dirname(__file__),"..","..","data")
    X_test.to_csv(os.path.join(rutadata, "X_test.csv"), index=False)
    y_test.to_csv(os.path.join(rutadata, "y_test.csv"), index=False)

    print("Entrenamiento finalizado ...")