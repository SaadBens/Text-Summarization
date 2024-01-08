from textSummarization.config.configuration import ConfigurationManager
from textSummarization.conponents.data_validation import DataValiadtion
from textSummarization.logging import logger


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config=data_transformation_config)
        data_transformation.convert()