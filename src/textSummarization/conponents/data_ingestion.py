import os
import urllib.request as request
import zipfile
from textSummarization.logging import logger
from textSummarization.utils.common import get_size
from textSummarization.entity import DataIngestionConfig 
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def download_dataset(self):
        if not os.path.exists(self.config.local_data_file):
            # Download the DialogSum dataset from Hugging Face
            dataset = load_dataset(self.config.dataset_name)
            logger.info(f"Downloaded {self.config.dataset_name} dataset successfully.")
            dataset.save_to_disk(os.path.join(self.config.root_dir,"DialogSum"))
        
        else:
            logger.error(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")        
    