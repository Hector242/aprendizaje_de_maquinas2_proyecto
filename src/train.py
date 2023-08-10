"""
train.py

DESCRIPCIÓN: train.py will run the training job
AUTOR: Hector Sanchez
FECHA:09/08/2023
"""

# Imports
import logging
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# avoiding traceback
sys.excepthook = lambda exctype,exc,traceback : print("{}: {}".format(exctype.__name__,exc))

# adding logging
logging.basicConfig(
    filename='../logs/modelTrain.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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
        logging.info("INIT: load train dataset")
        try:
            pandas_df = pd.read_csv(self.input_path + '/train_final.csv')
            logging.info("SUCCESS: training data was loaded successfully")

        except FileNotFoundError:
            print("file or directory not found ->" + self.input_path + "/train_final.csv") 
            logging.error("FAILED: file or directory not found")

        return pandas_df

    
    def model_training(self, df: pd.DataFrame) -> object:
        """
        This function will build & train the model

        :param df: training dataset
        :type df: pd.Dataframe

        :rparam model_trained: returns the model trained
        :rtype model_trained: object
        """
        logging.info("INIT: model training started")
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
        logging.info("SUCCESS: model was successfully trained")

        return model_trained

    def model_dump(self, model_trained) -> None:
        """
        this function will save the model trained as a 
        pickle file
        
        :param model_trained: model trained
        :type model_trained: object
        """
        logging.info("INIT: saving model in pkl")
        # file name & path
        model_pkl_file = self.model_path + '/model.pkl'
        
        # save in binary wb (write binary)
        with open(model_pkl_file, 'wb') as file:
            pickle.dump(model_trained, file)    
        logging.info("SUCCESS: model was saved successfully")

        return None

    def run(self):
    
        df = self.read_data()
        model_trained = self.model_training(df)
        self.model_dump(model_trained)

if __name__ == "__main__":

    ModelTrainingPipeline(input_path = '../features',
                          model_path = '../model_trained').run()