import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineering(BaseEstimator, TransformerMixin):
    """
    ingeniería de características para churn telco

    objetivo:
    - reducir redundancia semántica en servicios
    - generar variables agregadas
    - crear interacciones de negocio
    """

    def __init__(self, drop_originals=True):
        self.drop_originals = drop_originals

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        # normalización semántica de servicios
        columnas_servicios = [
            "OnlineSecurity",
            "TechSupport",
            "OnlineBackup",
            "DeviceProtection",
            "StreamingTV",
            "StreamingMovies"
        ]

        # unificación de categoría "no internet service" a "no"
        for col in columnas_servicios:

            if col in X.columns:

                X[col] = X[col].replace(
                    "No internet service",
                    "No"
                )

        # creación de variables agregadas
        servicios_proteccion = [
            "OnlineSecurity",
            "TechSupport",
            "OnlineBackup",
            "DeviceProtection"
        ]

        servicios_streaming = [
            "StreamingTV",
            "StreamingMovies"
        ]

        # conteo de servicios de protección activos
        cols_proteccion = [
            c for c in servicios_proteccion
            if c in X.columns
        ]

        if cols_proteccion:

            X["n_services_protection"] = (
                X[cols_proteccion]
                .eq("Yes")
                .sum(axis=1)
            )

        # conteo de servicios de streaming activos
        cols_streaming = [
            c for c in servicios_streaming
            if c in X.columns
        ]

        if cols_streaming:

            X["n_services_streaming"] = (
                X[cols_streaming]
                .eq("Yes")
                .sum(axis=1)
            )

        # feature de interacción (riesgo de churn)
        if all(col in X.columns for col in [
            "Contract",
            "PaymentMethod"
        ]):

            X["contract_payment_risk"] = (
                (X["Contract"] == "Month-to-month")
                &
                (X["PaymentMethod"] == "Electronic check")
            ).astype(int)

        # eliminación de variables redundantes
        if self.drop_originals:

            columnas_eliminar = (
                servicios_proteccion +
                servicios_streaming
            )

            columnas_eliminar = [
                c for c in columnas_eliminar
                if c in X.columns
            ]

            X = X.drop(columns=columnas_eliminar)

        return X