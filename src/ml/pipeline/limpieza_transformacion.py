import os
import re
import pandas as pd

from db.conexion import obtener_motor

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    StandardScaler,
    OneHotEncoder
)
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from .feature_engineering import FeatureEngineering
from .filtro_correlacion import CorrelationFilter
from .winsorizer import Winsorizer


# normalización de los nombres de las columnas que se generanpara ml y base de datos
def clean_names(cols):
    return [
        re.sub(r"[^0-9a-zA-Z]+", "_", col).strip("_").lower()
        for col in cols
    ]


def tratar_duplicados(X: pd.DataFrame, drop=True):
    return X.drop_duplicates() if drop else X


# pipeline de transformación de datos
def ejecutar_transformacion(exportar_csv=True, exportar_bd=True):
    """
    Ejecuta el pipeline completo de limpieza y transformación del dataset de churn.

    Carga los datos crudos, aplica ingeniería de características, preprocesamiento
    por tipo de variable y filtro de colinealidad. Permite exportar el resultado
    a CSV y persistirlo en base de datos.

    Parámetros
    ----------
    exportar_csv : bool, default=True
        Si es True, guarda el dataset transformado en data/data_limpia.csv.
    exportar_bd : bool, default=True
        Si es True, inserta el dataset transformado en la tabla datos_limpios.
    """

    # conexión a base de datos
    motor = obtener_motor()

    # carga de dataset
    ruta_data = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
        "02_Base_Customer-Churn.csv"
    )
    
    data = pd.read_csv(ruta_data, sep=";")

    #para eliminar los duplicados pero solo tomando encuenta la columna Id para realizarlo 
    data = data.drop_duplicates(subset=["customerID"], keep="last")

    # separación de variable objetivo
    target = "Churn"
    X = data.drop(columns=[target], errors="ignore")
    y = data[target]

    # definición de variables por tipo
    num_cols = ["tenure", "MonthlyCharges"]

    disc_cols = [
        "n_services_protection",
        "n_services_streaming"
    ]

    bin_cols = [
        "SeniorCitizen",
        "contract_payment_risk"
    ]

    cat_cols = [
        "Contract",
        "InternetService",
        "PaymentMethod",
        "PaperlessBilling",
        "Partner",
        "Dependents"
    ]

    # feature engineering del dominio
    fe = FeatureEngineering()

    # preprocesamiento por tipo de variable
    preprocessor = ColumnTransformer([

        # variables numéricas: outliers + imputación + escalado
        (
            "num",
            Pipeline([
                ("winsorizer", Winsorizer()),
                ("imputer", SimpleImputer(strategy="mean")),
                ("scaler", StandardScaler())
            ]),
            num_cols
        ),

        # variables discretas: imputación básica
        (
            "disc",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent"))
            ]),
            disc_cols
        ),

        # variables binarias: sin transformación
        (
            "bin",
            "passthrough",
            bin_cols
        ),

        # variables categóricas: imputación + one hot encoding
        (
            "cat",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                    sparse_output=False
                ))
            ]),
            cat_cols
        )
    ])

    # pipeline completo de preparación
    pipeline_preparacion = Pipeline([
        ("duplicados", FunctionTransformer(lambda x: x.drop_duplicates())),
        ("feature_engineering", fe),
        ("preprocesador", preprocessor),
        ("colinealidad", CorrelationFilter(threshold=0.9))
    ])

    # ajuste del pipeline
    pipeline_preparacion.fit(X)

    # obtención de nombres de features
    feature_names = (
        pipeline_preparacion
        .named_steps["preprocesador"]
        .get_feature_names_out()
    )

    pipeline_preparacion.named_steps[
        "colinealidad"
    ].set_feature_names(feature_names)

    # transformación del dataset
    X_transformada = pipeline_preparacion.transform(X)

    cols_finales = (
        pipeline_preparacion
        .named_steps["colinealidad"]
        .get_feature_names_out()
    )

    cols_finales = list(clean_names(cols_finales))

    # reconstrucción del dataset final
    data_transformada = pd.DataFrame(
        X_transformada,
        columns=cols_finales
    )

    # para eliminar las columnas duplicadas que puedan surgir del preprocesamiento, 
    # asegurando que cada columna sea única en el dataset final.
    data_transformada = data_transformada.loc[:, ~data_transformada.columns.duplicated()]

    # agregado de variable objetivo
    data_transformada["churn"] = y.values

    # persistencia en csv
    if exportar_csv:

        ruta_salida = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "data",
            "data_limpia.csv"
        )

        data_transformada.round(4).to_csv(
            ruta_salida,
            index=False,
            sep=";",
            decimal=","
        )

    print("\nDataset limpio exportado correctamente.")

    # persistencia en base de datos
    if exportar_bd:

        print("Haciendo la inserción en la base de datos...")

        data_transformada.round(4).to_sql(
            name="datos_limpios",
            con=motor,
            if_exists="append",
            index=False,
            chunksize=1000,
            method="multi"
        )

        print("Datos insertados correctamente en la tabla 'datos_limpios'.\n")

    # resumen final
    print("-"*55)
    print("Limpieza y transformación completadas correctamente.")
    print(f"Dimensión final: {data_transformada.shape}")
    print(f"Features finales: {len(cols_finales)}")
    print("-"*55)

    print("\nListado de features:")

    for col in cols_finales:
        print(f"- {col}")

    return data_transformada, y, pipeline_preparacion