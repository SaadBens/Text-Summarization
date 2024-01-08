import os
from textSummarization.logging import logger
from textSummarization.entity import DataValidationConfig

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config


    
    def validate_dataset(self) -> bool:
        try:
            dataset = load_from_disk(self.config.local_data_file)
            
            # Validate the required files of the dataset
            all_files = os.listdir(self.config.local_data_file)
            validation_status_files = all(file in all_files for file in self.config.ALL_REQUIRED_FILES)

            # Validate the required features of the dataset
            validation_status_features = all(
                all(feature in dataset[split].features for feature in self.config.REQUIRED_FEATURES)
                for split in dataset.keys()
            )

            # Combine validation statuses
            final_validation_status = validation_status_files and validation_status_features
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status files: {validation_status_files}, features: {validation_status_features}")

            if not final_validation_status:
                missing_elements = "Missing files or features in dataset."
                logger.error(missing_elements)
                raise ValueError(missing_elements)

            return final_validation_status

        except Exception as e:
            logger.error(f"Error in dataset validation: {e}")
            raise e