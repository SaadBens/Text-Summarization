from textSummarization.pipeline.stage_data_ingestion import DataIngestionTrainingPipeline
from textSummarization.logging import logger


STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f"--------- stage {STAGE_NAME} started ---------") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f"--------- stage {STAGE_NAME} completed ---------")
except Exception as e:
        logger.exception(e)
        raise e