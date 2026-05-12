import os
import pandas as pd
import numpy as np
from sklearn.base import TransformerMixin

ruta = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn.csv")
data = pd.read_csv(ruta, sep=",")

class CorrelationFilter(TransformerMixin):
    """
    Filtro de correlación

    Parámetros  
    elimina columnas innecesarias para el modelado, 
    
    eliminar CustomerID
    eliminar TotalCharges
    
    ----------
    BaseEstimator : Clase base para estimadores en scikit-learn.
    TransformerMixin : Clase base para transformadores en scikit-learn.

    Atributos
    ---------
    threshold : float
        Umbral de correlación
        
    """
    ruta = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Telco-Customer-Churn.csv")
    data = pd.read_csv(ruta, sep=",")

    def __init__(self, threshold=0.9):
        self.threshold = threshold

    def fit(self, X, y=None):
        self.feature_names_in_ = np.arange(X.shape[1])  # temporal
        df = data.DataFrame(X)

        corr = df.corr().abs()
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

        self.to_drop_ = [col for col in upper.columns if any(upper[col] > self.threshold)]
        self.features_ = [col for col in df.columns if col not in self.to_drop_]

        return self

    def transform(self, X):
        df = data.DataFrame(X)
        return df[self.features_].values

    def set_feature_names(self, names):
        self.feature_names_in_ = np.array(names)
        self.feature_names_out_ = self.feature_names_in_[self.features_]

    def get_feature_names_out(self, input_features=None):
        return self.feature_names_out_
    
    def delete():
        X = X.drop(columns=[])