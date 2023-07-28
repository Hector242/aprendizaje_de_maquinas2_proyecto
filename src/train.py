"""
train.py

COMPLETAR DOCSTRING

DESCRIPCIÓN:
AUTOR:
FECHA:
"""

# Imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score
from sklearn import metrics
from sklearn.linear_model import LinearRegression
import pickle

class ModelTrainingPipeline(object):

    def __init__(self, input_path, model_path):
        self.input_path = input_path
        self.model_path = model_path

    def read_data(self) -> pd.DataFrame:
        """
        This function will read the training dataset
        
        :return pandas_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """
        pandas_df = pd.read_csv(self.input_path + '/train_final.csv')
        
        return pandas_df

    
    def model_training(self, df: pd.DataFrame) -> object:
        """
        This function will build & train the model

        :param df: training dataset
        :type df: pd.Dataframe

        :rparam model_trained: returns the model trained
        :rtype model_trained: object
        """
        df_train = df.copy()
        seed = 28
        model = LinearRegression()

        # split dataset in training & validation
        X = df_train.drop(columns='Item_Outlet_Sales') # Drop feature to predict
        x_train, _, y_train, _ = train_test_split(X,
                                                  df_train['Item_Outlet_Sales'],
                                                  test_size = 0.3,
                                                  random_state=seed)
        
        # model training
        model.fit(x_train,y_train)

        # return model trained
        model_trained = model
        return model_trained

    def model_dump(self, model_trained) -> None:
        """
        this function will save the model trained as a 
        pickle file
        
        :param model_trained: model trained
        :type model_trained: object
        """
        # file name & path
        model_pkl_file = self.model_path + '/model.pkl'
        
        # save in binary wb (write binary)
        with open(model_pkl_file, 'wb') as file:
            pickle.dump(model_trained, file)

        return None

    def run(self):
    
        df = self.read_data()
        model_trained = self.model_training(df)
        self.model_dump(model_trained)

if __name__ == "__main__":

    ModelTrainingPipeline(input_path = '../features',
                          model_path = '../model_trained').run()