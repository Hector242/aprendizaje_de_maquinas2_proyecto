"""
feature_engineering.py

DESCRIPTIÓN: feature engineering.py it's for preprocess the data for ML usage 
AUTOR: Hector Sanchez
FECHA:09/08/2023
"""

# Imports
import logging
import sys
import pandas as pd
import numpy as np
import argparse

# avoiding traceback
sys.excepthook = lambda exctype,exc,traceback : print("{}: {}".format(exctype.__name__,exc))

# adding logging
logging.basicConfig(
    filename='../logs/featureEng.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# allowing and taking arguments with --json-path
parser = argparse.ArgumentParser(description="Json from user")
parser.add_argument("--json-path", type=str, help="Path to Json file")
args = parser.parse_args()

class FeatureEngineeringPipeline(object):

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self) -> pd.DataFrame:
        """
        In this function load & build the dataset

        :return pandas_df: The desired DataLake table as a DataFrame
        :rtype: pd.DataFrame
        """
        logging.info("INIT: load train and test datasets")
        # chooce between --json-path provided or not
        if args.json_path:
            json_path = args.json_path
            logging.info(f"Received JSON path: {json_path}")
            try:
                # Load json-data for inference
                pandas_df = pd.read_json(json_path, orient='index').T
                logging.info("dataset from json loaded")
            except ValueError as ve:
                logging.error(f"FAILED: ValueError occurred during prediction: {ve}")
            except Exception as e:
                logging.error(f"FAILED: An unexpected error occurred during prediction: {e}")
        else:
            try:
                # Reading Test and Train datasets
                data_train = pd.read_csv(self.input_path + '/Train_BigMart.csv')
                logging.info("SUCCESS: training data was loaded successfully")

                data_test = pd.read_csv(self.input_path + '/Test_BigMart.csv')
                logging.info("SUCCESS: test data was loaded successfully")

            except FileNotFoundError:
                print("file or directory not found. Please double check the path and names")
                logging.error("FAILED: file or directory not found")

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
        :type df: pd.DataFrame

        :return df_transformed: Dataframe transformed
        :rtype: pd.DataFrame 
        """
        logging.info("INIT: data transformation")
        # FEATURES ENGINEERING: Calculing how old is the shop(current year-Establishment_Year)
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
        for product in range(len(product_list)):
            df.loc[df['Item_Type'] == product_list[product], 'Item_Fat_Content'] = 'NA'

        # FEATURES ENGINEERING: building categories for 'Item_Type'
        dict_Item_Type = {'Others': 'Non perishable', 'Health and Hygiene': 'Non perishable', 
                          'Household': 'Non perishable', 'Seafood': 'Meats', 'Meat': 'Meats',
                          'Baking Goods': 'Processed Foods', 'Frozen Foods': 'Processed Foods', 
                          'Canned': 'Processed Foods', 'Snack Foods': 'Processed Foods',
                          'Breads': 'Starchy Foods', 'Breakfast': 'Starchy Foods',
                          'Soft Drinks': 'Drinks', 'Hard Drinks': 'Drinks', 'Dairy': 'Drinks'}
        
        df['Item_Type'] = df['Item_Type'].replace(dict_Item_Type)
        

        # FEATURES ENGINEERING: adding new categorie to 'Item_Fat_Content'
        df.loc[df['Item_Type'] == 'Non perishable', 'Item_Fat_Content'] = 'NA'

        # FEATURES ENGINEERING: encoding prices levels in 'Item_MRP'
        if 'Item_MRP' in df.columns and pd.api.types.is_numeric_dtype(df['Item_MRP']):
            df['Item_MRP'] = pd.qcut(df['Item_MRP'], 4, labels = [1, 2, 3, 4])

        # FEATURES ENGINEERING: encoding ordinal variable
        dataframe = df.drop(columns=['Item_Type', 'Item_Fat_Content']).copy()

        dict_outlet_size = {'High': 2, 'Medium': 1, 'Small': 0}
        dict_location_type = {'Tier 1': 2, 'Tier 2': 1, 'Tier 3': 0}

        dataframe['Outlet_Size'] = dataframe['Outlet_Size'].replace(dict_outlet_size)
        dataframe['Outlet_Location_Type'] = dataframe['Outlet_Location_Type'].replace(dict_location_type)

        # FEATURES ENGINEERING: encoding nominal variable
        dataframe = pd.get_dummies(dataframe, columns=['Outlet_Type'])

        df_transformed = dataframe.copy()
        logging.info("SUCCESS: data was successfully transformed")

        return df_transformed

    def write_prepared_data(self, transformed_dataframe: pd.DataFrame) -> None:
        """
        This fuction will split the data in test & train and the will save it in
        .csv files.

        :param transformed_dataframe: dataframe transformed
        :type transformed_dataframe: pd.DataFrame
        """
        logging.info("INIT: saving train & test data")
        # Drop non informative features
        dataset = transformed_dataframe.drop(columns=['Item_Identifier', 'Outlet_Identifier'])
        # chooce between --json-path provided or not
        if args.json_path:
            json_path = args.json_path
            logging.info(f"Received JSON path: {json_path}")
            dataset.to_csv(self.output_path + '/custom_data.csv', index=False)
            logging.info("SUCCESS: custom data was saved successfully")
        else:
            # split train & test
            df_train = dataset.loc[dataset['Set'] == 'train']
            df_test = dataset.loc[dataset['Set'] == 'test']

            df_train_copy = df_train.copy()
            df_test_copy = df_test.copy()

            # drop features without data
            df_train_copy.drop(['Set'], axis=1, inplace=True)
            df_test_copy.drop(['Item_Outlet_Sales','Set'], axis=1, inplace=True)

            # save datasets
            df_train_copy.to_csv(self.output_path + '/train_final.csv', index=False)
            df_test_copy.to_csv(self.output_path + '/test_final.csv', index=False)
            logging.info("SUCCESS: train & test data was saved successfully")

        return None

    def run(self):
    
        df = self.read_data()
        df_transformed = self.data_transformation(df)
        self.write_prepared_data(df_transformed)

if __name__ == "__main__":
    FeatureEngineeringPipeline(input_path = '../data',
                               output_path = '../features').run()