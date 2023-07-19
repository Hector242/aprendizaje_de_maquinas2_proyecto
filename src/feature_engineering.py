"""
feature_engineering.py

COMPLETAR DOCSTRING

DESCRIPTIÓN: feature engineering.py it's for preprocess the data for ML usage 
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
        DOCSTRING

        In this function load & build the dataset

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
        DOCSTRING
        
        This function preprosses the raw dataframe and return another 
        dataframe with the data transformed 

        :param df: Dataframe to be transform
        :type df: Dataframe

        :return df_transformed: Dataframe transformed
        :rtype: Dataframe 
        """
        
        # FEATURES ENGINEERING: Calculing how old is the shop (current year - Establishment_Year)
        df['Outlet_Establishment_Year'] = 2020 - df['Outlet_Establishment_Year']

        # Cleaning: Unifying labels for 'Item_Fat_Content'
        df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({'low fat':  'Low Fat', 
                                                                 'LF': 'Low Fat', 
                                                                 'reg': 'Regular'})

        # cleaning: Imputing missing data for Item_Weight with the mode.
        item_list = list(df[df['Item_Weight'].isnull()]['Item_Identifier'].unique())
        for item in item_list:
            mode = (df[df['Item_Identifier'] == item][['Item_Weight']]).mode().iloc[0,0] 
            df.loc[df['Item_Identifier'] == item, 'Item_Weight'] = mode 
        
        # Cleaning: Imputing missing data for Outlet_Size with the value = "small"
        outlet_list = list(df[df['Outlet_Size'].isnull()]['Outlet_Identifier'].unique())
        for outlet in outlet_list:
            df.loc[df['Outlet_Identifier'] == outlet, 'Outlet_Size'] =  'Small'

        # FEATURES ENGINEERING: setting new categorie for 'Item_Fat_Content'
        product_list = ['Household', 'Health and Hygiene', 'Hard Drinks',
                        'Hard Drinks', 'Soft Drinks', 'Fruits and Vegetables']
        for product in product_list:
            df.loc[df['Item_Type'] == product_list[product], 'Item_Fat_Content'] = 'NA'


        df_transformed = None
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