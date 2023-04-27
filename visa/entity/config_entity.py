# 2) secound step for pipline


from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",    # we coping values from config.yaml files we creating only folder name
                                 ["dataset_download_url",
                                  "raw_data_dir",
                                  "ingested_dir",
                                  "ingested_train_dir",
                                  "ingested_test_dir"])

TraningPipelineConfig = namedtuple("TraningPipelineConfig",["artifact_dir"])