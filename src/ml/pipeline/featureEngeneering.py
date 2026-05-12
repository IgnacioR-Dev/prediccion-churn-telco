import pandas as pd
import numpy as np

class FeatureEngineering ():
    
    def __init__(self,
        PhoneService='phoneservice',
        MultipleLines='multiplelines',
        StreamingMovies='streamingmovies',
        StreamingTV='streamingtv',
        CustomerID='customerid',
        TotalCharges='totalcharges',
        drop_originals=True
    ):
        self.Phone = PhoneService
        self.Multiple = MultipleLines
        self.Movies = StreamingMovies
        self.TV = StreamingTV
        self.drop_originals = drop_originals
        self.id = CustomerID
        self.total = TotalCharges
        
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        X = X.copy()
        if self.Phone in X.columns and self.Multiple in X.columns:
            condiciones = [
                (X[self.Phone] == 'yes') & (X[self.Multiple] == 'yes'),
                (X[self.Phone] == 'yes') & (X[self.Multiple] == 'no'),
                (X[self.Phone] == 'no') & (X[self.Multiple] == 'no'),
                (X[self.Phone] == 'no') & (X[self.Multiple] == 'no phone service'),
            ]
            resultados = [
                'yes','yes','no','no'
            ]
            print('Creando columna de servicephone')
            X['servicephone'] = np.select(condiciones, resultados, default='no')
            
        if self.TV in X.columns and self.Movies in X.columns:
            condicione = [
                (X[self.TV] == 'yes') & (X[self.Movies] == 'yes'),
                (X[self.TV] == 'yes') & (X[self.Movies] == 'no'),
                (X[self.TV] == 'no') & (X[self.Movies] == 'no'),
                (X[self.TV] == 'no') & (X[self.Movies] == 'No internet service'),]
            resultadoStreaming = ['yes','yes','no','no']
            print('Creando columna de streaming')
            X['streaming'] = np.select(condicione, resultadoStreaming, default='no')
            
        if self.drop_originals:
            print('Eliminando columnas')
            X = X.drop(columns=[self.Phone, self.Multiple,
                                self.Movies, self.TV])
            X = X.drop(columns=[self.id, self.total])
        return X


