import subprocess
import logging

# adding logging
logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
# Pipeline entrypoint
try:
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

