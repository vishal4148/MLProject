import os, sys
import pandas as pd
import numpy as np
from visa.constant import *
from visa.logger import logging
from visa.exception import CustomException
from visa.pipeline.pipeline import Pipeline 

def main():
    try:
        pass
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")

if __name__ =="main1":
    main()