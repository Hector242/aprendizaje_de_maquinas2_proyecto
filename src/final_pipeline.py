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