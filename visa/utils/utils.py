import os , sys
from  visa.exception import CustomException
import yaml

def read_yaml_file(file_path:str) -> str:
    try:
        with open (file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys) from e