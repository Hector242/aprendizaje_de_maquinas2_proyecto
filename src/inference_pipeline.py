import subprocess
import logging

# adding logging
logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
try:
    logging.info("INIT: feature engineering started")
    subprocess.run(['Python', 'feature_engineering.py'], check=True)
    logging.info("SUCCESS: feature engineering successfully completed")
    
except subprocess.CalledProcessError:
    logging.error("FAILED: Opss! something went wrong in feature_engineering.py")

try:
    logging.info("INIT: model prediction started")
    subprocess.run(['Python', 'predict.py'], check=True)
    logging.info("SUCCESS: model prediction successfully completed")

except subprocess.CalledProcessError:
    logging.error("FAILED: Opss! something went wrong in predict.py")

