import subprocess
import logging

# adding logging
logging.basicConfig(
    filename='../logs/TrainPipe.log',
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Pipeline entrypoint
try:
    #feature engineering script
    logging.info("INIT: feature engineering started")
    subprocess.run(['Python', 'feature_engineering.py'],check=True, 
                   capture_output=True, text=True)
    logging.info("SUCCESS: feature engineering successfully completed")

    # train scrpt
    logging.info("INIT: model training started")
    subprocess.run(['Python', 'train.py'],check=True, 
                   capture_output=True, text=True)
    logging.info("SUCCESS: model training successfully completed")

except subprocess.CalledProcessError as e:
        logging.error(f"FAILED: Oops! Something went wrong in {e}")