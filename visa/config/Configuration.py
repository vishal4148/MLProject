import os ,sys
from visa.constant import *
from visa.logger import logging
from visa.exception import CustomException
from visa.entity .config_entity import *
from visa.utils.utils import read_yaml_file

class configuration:
    def __init__(self,
                 config_file_path:str = CONFIG_FILE_PATH,                             # calling config yaml file
                 current_time_stamp:str = CURRENT_TIME_STAMP) -> None:                 # while reading data from AWS or any other we cpature time
        # try:
            
             self.config_info = read_yaml_file(file_path=config_file_path)
             self.traning_pipeline_config = self.get_training_pipeline_config()
             self.time_stamp = current_time_stamp
        # except Exception as e:
            # raise CustomException (e,sys) from e
        
    def get_data_ingestion_config(self)-> DataIngestionConfig:          
        try:
            artifact_dir = self.traning_pipeline_config.artifact_dir                        # commmon for every pipeline
            
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
                                                       DATA_INGESTION_ARTIFACT_DIR,
                                                       self.time_stamp)                      # here we capture train,test ,ans raw data 
            
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]                 # Calling form constant folder
 
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            
            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY])
            
            ingested_train_dir = os.path.join(ingested_data_dir,
                                        data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY])
            
            ingested_test_dir = os.path.join(ingested_data_dir,
                                        data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY])
            
            data_ingestion_config = DataIngestionConfig(dataset_download_url=dataset_download_url,
                                                        raw_data_dir=raw_data_dir,
                                                        ingested_train_dir=ingested_train_dir,
                                                        ingested_test_dir=ingested_test_dir)
            return data_ingestion_config
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
   
    def get_training_pipeline_config(self) ->  TraningPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config =   TraningPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise CustomException(e,sys) from e
        