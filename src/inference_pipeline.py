"""
inference_pipeline.py

DESCRIPTIÓN: inference_pipeline.py will run the pipeline for make inference from the model 
AUTOR: Hector Sanchez
FECHA:09/08/2023
"""
import subprocess
import logging
import argparse

# adding logging
logging.basicConfig(
    filename='../logs/inferencePipe.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# allowing and taking arguments with --json-path
parser = argparse.ArgumentParser(description="Json from user")
parser.add_argument("--json-path", type=str, help="Path to Json file")
args = parser.parse_args()


# Pipeline entrypoint
try:
    # chooce between --json-path provided or not
    if args.json_path:
        json_path = args.json_path
        logging.info(f"Received JSON path: {json_path}")

        #feature engineering script
        logging.info("INIT: feature engineering started")
        subprocess.run(['Python', 'feature_engineering.py', '--json-path', json_path], check=True, 
                       capture_output=True, text=True)
        logging.info("SUCCESS: feature engineering successfully completed")

        #predict script
        logging.info("INIT: model prediction started")
        subprocess.run(['Python', 'predict.py', '--json-path', json_path], check=True, 
                   capture_output=True, text=True)
        logging.info("SUCCESS: model prediction successfully completed")

    else:
        #feature engineering script
        logging.info("INIT: feature engineering started")
        subprocess.run(['Python', 'feature_engineering.py'], check=True, 
                       capture_output=True, text=True)
        logging.info("SUCCESS: feature engineering successfully completed")

        #predict script
        logging.info("INIT: model prediction started")
        subprocess.run(['Python', 'predict.py'], check=True, 
                   capture_output=True, text=True)
        logging.info("SUCCESS: model prediction successfully completed")
    
except subprocess.CalledProcessError as e:
    logging.error(f"FAILED: Opss! something went wrong in {e}")

