"""
processing_pipeline.py

DESCRIPTIÓN: processing_pipeline.py it's for run the whole pipeline to train and test the model 
AUTOR: Hector Sanchez
FECHA:09/08/2023
"""
import subprocess
import logging

# adding logging
logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Menu Function
def print_menu()->None:
    print("""
    On the following question reply with yes or no. 
    
    The question will ask you if you want or not to use
    Test dataset for inference. In case you choose no, you
    will require to provide a custom Json file.
    
    The Path to this Json file is ../Notebook/example.json
    """)

# Pipeline entrypoint
try:
    # asking user for data
    print_menu()
    choice = input("Are you using Default Test for prediction: ")
    # chooce between --json-path provided or not
    if choice == "no":
        # Json path from user
        json_path = input("Please, provide the Json file path: ")

        #train_pipeline
        logging.info("INIT: Train pipeline started")
        subprocess.run(['Python', 'train_pipeline.py'], check=True, 
                       capture_output=True, text=True)
        logging.info("SUCCESS: feature engineering successfully completed")
        
        #inference_pipeline
        logging.info("INIT: Inference pipeline started")
        subprocess.run(['Python', 'inference_pipeline.py', '--json-path', json_path], check=True, 
                   capture_output=True, text=True)
        logging.info("SUCCESS: model prediction successfully completed")

    else:
        #train_pipeline
        logging.info("INIT: Train pipeline started")
        subprocess.run(['Python', 'train_pipeline.py'], check=True, 
                       capture_output=True, text=True)
        logging.info("SUCCESS: feature engineering successfully completed")

        #inference_pipeline
        logging.info("INIT: Inference pipeline started")
        subprocess.run(['Python', 'inference_pipeline.py'], check=True, 
                   capture_output=True, text=True)
        logging.info("SUCCESS: model prediction successfully completed")
    
except subprocess.CalledProcessError as e:
    logging.error(f"FAILED: Opss! something went wrong in {e}")