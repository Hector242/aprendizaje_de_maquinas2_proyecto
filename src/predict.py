"""
predict.py

COMPLETAR DOCSTRING

DESCRIPCIÓN:
AUTOR:
FECHA:
"""

# Imports
import logging
import sys
import pandas as pd
import pickle

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
        # make predictions over test dataset
        y_pred = model.predict(test_data)

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