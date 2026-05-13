import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class CorrelationFilter(BaseEstimator, TransformerMixin):
    """
    Elimina variables que entregan información redundante al modelo.

    Cuando dos variables están muy correlacionadas entre sí, incluir ambas
    no aporta información adicional. Este filtro identifica esos casos y
    conserva solo una de cada par, reduciendo ruido sin perder señal útil.

    Parámetros
    ----------
    threshold : float, default=0.9
        Nivel de correlación a partir del cual una variable se considera redundante.
    """

    def __init__(self, threshold=0.9):
        self.threshold = threshold

    # ── cálculo de matriz de correlación y selección de variables altamente correlacionadas
    def fit(self, X, y=None):
        """Identifica qué variables eliminar por ser demasiado similares entre sí."""

        df = pd.DataFrame(X)

        # matriz de correlación absoluta
        corr = df.corr().abs()

        # solo triángulo superior para evitar duplicados
        upper = corr.where(
            np.triu(np.ones(corr.shape), k=1).astype(bool)
        )

        # variables a eliminar por alta correlación
        self.to_drop_ = [
            col
            for col in upper.columns
            if any(upper[col] > self.threshold)
        ]

        # variables que se conservan en el dataset final
        self.features_ = [
            col
            for col in df.columns
            if col not in self.to_drop_
        ]

        return self

    # ── eliminación de variables correlacionadas
    def transform(self, X):
        """Elimina las variables redundantes identificadas en fit()."""

        df = pd.DataFrame(X)

        return df[self.features_].values

    # ── mapeo de nombres originales a nombres finales del pipeline
    def set_feature_names(self, names):
        """Asocia los nombres de columnas del preprocesador al filtro."""

        self.feature_names_out_ = np.array([
            names[i]
            for i in self.features_
        ])

    # ── retorno de nombres finales compatibles con sklearn
    def get_feature_names_out(self, input_features=None):
        """Retorna los nombres de las variables conservadas."""

        return self.feature_names_out_