# 2) secound step for pipline
from collections import namedtuple

# we coping values from config.yaml files we creating only folder name
DataIngestionConfig=namedtuple("DataIngestionConfig",
["dataset_download_url","raw_data_dir","ingested_train_dir","ingested_test_dir"])


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])