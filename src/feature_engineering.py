"""
feature_engineering.py

COMPLETAR DOCSTRING

DESCRIPTIÓN: In this code feature engineering for the dataset It's been done 
AUTOR: Hector Sanchez
FECHA:-
"""

# Imports
import pandas as pd
import numpy as np

class FeatureEngineeringPipeline(object):

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING 
        In this function we read the whole dataset
        :return pandas_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """
            
        # Reading Test and Train datasets
        data_train = pd.read_csv(f'{self.input_path}/Train_BigMart.csv')
        data_test = pd.read_csv(f'{self.input_path}/Test_BigMart.csv')

        # label both df to merge them and be able to split them
        data_train['Set'] = 'train'
        data_test['Set'] = 'test'
        
        # Mergin both df in one
        pandas_df = pd.concat([data_train, data_test], ignore_index=True, sort=False)
        return pandas_df

    
    def data_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        COMPLETAR DOCSTRING
        
        """
        
        # FE: Calculing how old is the shop (current year - Establishment_Year)
        df['Outlet_Establishment_Year'] = 2020 - df['Outlet_Establishment_Year']

        # Cleaning: Unifying labels for 'Item_Fat_Content'
        df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({'low fat':  'Low Fat', 
                                                                     'LF': 'Low Fat', 
                                                                     'reg': 'Regular'})

        # cleaning: Imputing with similar values.
        item_list = list(df[df['Item_Weight'].isnull()]['Item_Identifier'].unique()) # making a list
        for item in item_list:
            mode = (df[df['Item_Identifier'] == item][['Item_Weight']]).mode().iloc[0,0] # taking the mode
            df.loc[df['Item_Identifier'] == item, 'Item_Weight'] = mode # Imputing with the mode
        
        
        return df_transformed

    def write_prepared_data(self, transformed_dataframe: pd.DataFrame) -> None:
        """
        COMPLETAR DOCSTRING
        
        """
        
        # COMPLETAR CON CÓDIGO
        
        return None

    def run(self):
    
        df = self.read_data()
        df_transformed = self.data_transformation(df)
        self.write_prepared_data(df_transformed)

  
if __name__ == "__main__":
    FeatureEngineeringPipeline(input_path = '../data',
                               output_path = '../outputs/').run()