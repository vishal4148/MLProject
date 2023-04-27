
import os, sys
import pandas as pd
import numpy as np
from visa.constant import *
from visa.logger import logging
from visa.entity.config_entity import DataIngestionConfig
from visa.entity.artifact_entity import DataIngestionArtifact
from visa.exception import CustomException
from datetime import date
from sklearn.model_selection import train_test_split
from six.moves import urllib
 # download data (cloud,data_set,Github) -> Raw data
 # split data into train and test  -> Ingested data

class DataIngestion:
    def __init__(self,data_ingestion_config : DataIngestionConfig):     # we calling all from config_entity.py file(data_ingestion_config)
        try:
            logging.info(f"Data ingestion started")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def downlaod_data(self)-> str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url    # able to download dataset

            raw_data_dir = self.data_ingestion_config.raw_data_dir            # create a folder raw data dir

            os.makedirs(raw_data_dir,exist_ok= True)                        # if folder is not avai then exit the file 

            us_visa_file_name =  os.path.basename(download_url)                     

            raw_file_path = os.path.join(raw_data_dir,us_visa_file_name)    # join the files 

            logging.info(f"Downloading file from : [{download_url}] into : [{raw_data_dir}]")

            urllib.request.urlretrieve(download_url,raw_data_dir)

            logging.info(f" file: [{raw_file_path}] has been downloaded successfully")

            return raw_file_path

        except Exception as e:
            raise CustomException(e,sys) from e
        
    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir 
            file_name = os.listdir(raw_data_dir)[0]


            us_visa_file_name = os.path.join(raw_data_dir,file_name )  # we have csv file 

            today_date = date.today()
            current_year = today_date.year

            us_visa_dateframe = pd.read_csv(us_visa_file_name)

            us_visa_dateframe[COLUMN_COMPANY_AGE]= current_year - us_visa_dateframe[COLUMN_YEAR_ESTB]

            us_visa_dateframe.drop([COLUMN_ID,COLUMN_YEAR_ESTB], axis=1, inplace= True)

            us_visa_dateframe[COLUMN_CASE_STATUS] = np.where(us_visa_dateframe[COLUMN_CASE_STATUS] == 'Denied',1,0)

            train_Set = None
            test_Set= None

            train_Set,test_Set = train_test_split(us_visa_dateframe,test_size=0.2 , random_state= 42)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if train_Set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Traning data set to file: [{train_file_path}]")
                train_Set.to_csv(train_file_path,index= False)

            if test_Set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Testing data set to file: [{test_file_path}]")
                test_Set.to_csv(test_file_path,index= False)



            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested = True,
                                                            message = f"Data ingestion completed successfully")
            logging.info(f"Data ingestion Artifact: [{data_ingestion_artifact}]")
            
            return data_ingestion_artifact
        

        except Exception as e:
            raise CustomException (e,sys) from e
 
    def initate_data_ingestion (self):
        try:
            raw_data_file = self.downlaod_data()
            return self.split_data_as_train_test()
        
        except Exception as e:
            raise CustomException (e,sys) from e