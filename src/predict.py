"""
predict.py

DESCRIPCIÓN:predict.py will give prediction on a .csv from a test datset or from custom file
AUTOR: Hector Sanchez
FECHA:09/08/2023
"""

# Imports
import logging
import sys
import pandas as pd
import pickle
import argparse

# avoiding traceback
sys.excepthook = lambda exctype,exc,traceback : print("{}: {}".format(exctype.__name__,exc))

# adding logging
logging.basicConfig(
    filename='../logs/predictions.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# allowing and taking arguments with --json-path
parser = argparse.ArgumentParser(description="Json from user")
parser.add_argument("--json-path", type=str, help="Path to Json file")
args = parser.parse_args()

class MakePredictionPipeline(object):
    
    def __init__(self, input_path, output_path, model_path: str = None):
        self.input_path = input_path
        self.output_path = output_path
        self.model_path = model_path
                
                
    def load_data(self) -> pd.DataFrame:
        """
        This function load the test dataset

        :rparam test_dataset: dataset to evaluate the model with
        .rtype test_dataset: pd.Dataframe
        """
        logging.info("INIT: load test dataset")
        # chooce between --json-path provided or not
        if args.json_path:
            json_path = args.json_path
            logging.info(f"Received JSON path: {json_path}")

            try:
                # Load json-data for inference
                test_dataset = pd.read_csv(self.input_path + '/custom_data.csv')
                logging.info("dataset from json loaded")

                # adding missing features that are on train data
                list_feature = ['Outlet_Type_Grocery Store', 'Outlet_Type_Supermarket Type1',
                                'Outlet_Type_Supermarket Type2', 'Outlet_Type_Supermarket Type3']
                # to add the right order
                test_dataset.drop(columns='Outlet_Type_Supermarket Type1', inplace=True)

                for column in list_feature:
                    test_dataset[column] = 0

            except ValueError as ve:
                logging.error(f"FAILED: ValueError occurred: {ve}")
            except Exception as e:
                logging.error(f"FAILED: An unexpected error occurre: {e}")
        else:
            try:
                # Load test dataset
                test_dataset = pd.read_csv(self.input_path + '/test_final.csv')
                logging.info("SUCCESS: test data was loaded successfully")

            except FileNotFoundError:
                print("file or directory not found ->" + self.input_path + "/test_final.csv")
                logging.error("FAILED: file or directory not found")

        return test_dataset

    def load_model(self) -> object:
        """
        This function load the model trained

        :rparam model: model trained
        :rtype model: object
        """ 
        # Get path
        model_pkl_file = self.model_path + '/model.pkl'
        logging.info("INIT: load model")
        try:
            # load model from pickle file
            with open(model_pkl_file, 'rb') as file:  
                model = pickle.load(file)
            logging.info("SUCCESS: model was loaded successfully")

        except FileNotFoundError:
            print("file or directory not found ->" + model_pkl_file)
            logging.error("FAILED: file or directory not found")

        return model


    def make_predictions(self, test_data: pd.DataFrame, model: object) -> pd.DataFrame:
        """
        This fuction build the predictions

        :param test_data: test dataset for model evaluation
        :type test_data: pd.Datafram

        :param model: model trained
        :type model: object

        :rparam y_pred: predictions
        :rtype y_pred: pd.Dataframe
        """
        logging.info("INIT: starting model predictions")
        try:
            # make predictions over test dataset
            y_pred = model.predict(test_data)
            logging.info("SUCCESS: Prediction passed successfully")

        except ValueError as ve:
            logging.error(f"FAILED: ValueError occurred during prediction: {ve}")
        except Exception as e:
            logging.error(f"FAILED: An unexpected error occurred during prediction: {e}")

        #convert to datafram
        y_pred = pd.DataFrame(y_pred)

        # rename output column
        y_pred.rename(columns={0:'y_predicted'}, inplace= True)

        return y_pred


    def write_predictions(self, predicted_data: pd.DataFrame) -> None:
        """
        This function save the predictions

        :param predicted_data: predicted data
        :type predicted_data: pd.Datafram
        """
        logging.info("INIT: saving model predictions")
        #Save predicted data on csv
        predicted_data.to_csv(self.output_path + '/prediction.csv')
        logging.info("SUCCESS: model predictions successfully saved")

        return None


    def run(self):

        data = self.load_data()
        model = self.load_model()
        df_preds = self.make_predictions(data, model)
        self.write_predictions(df_preds)


if __name__ == "__main__":
    
    #spark = Spark()
    
    pipeline = MakePredictionPipeline(input_path = '../features',
                                      output_path = '../predictions',
                                      model_path = '../model_trained')
    pipeline.run()  