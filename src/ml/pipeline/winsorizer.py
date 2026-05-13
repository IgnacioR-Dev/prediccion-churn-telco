import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class Winsorizer(BaseEstimator, TransformerMixin):
    """
    winsorización de variables numéricas

    objetivo:
    - reducir impacto de outliers extremos
    - estabilizar distribuciones antes del escalado
    """

    def __init__(self, limits=(0.05, 0.05)):
        self.limits = limits

    def fit(self, X, y=None):
        """
        aprende los límites de recorte por columna
        """

        # detección de nombres de columnas
        if isinstance(X, pd.DataFrame):
            self.columns_ = X.columns
        else:
            self.columns_ = np.arange(X.shape[1])

        X = pd.DataFrame(X, columns=self.columns_)
        X = X.astype("float64")

        # almacenamiento de límites inferior y superior
        self.lower_limits_ = {}
        self.upper_limits_ = {}

        for col in self.columns_:

            self.lower_limits_[col] = X[col].quantile(self.limits[0])

            self.upper_limits_[col] = X[col].quantile(
                1 - self.limits[1]
            )

        return self

    def transform(self, X):
        """
        aplica recorte de valores extremos usando límites aprendidos
        """

        X = pd.DataFrame(X, columns=self.columns_)
        X = X.astype("float64")

        for col in self.columns_:

            X[col] = np.clip(
                X[col],
                self.lower_limits_[col],
                self.upper_limits_[col]
            )

        return X

    def get_feature_names_out(self, input_features=None):
        """
        retorna nombres de columnas de salida
        """

        if input_features is None:
            return np.array(self.columns_)

        return np.array(input_features)