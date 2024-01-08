import os
from textSummarization.logging import logger
from transformers import AutoTokenizer
from datasets import load_dataset, load_from_disk
from textSummarization.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)


    
    def convert_examples_to_features(self,example_batch):
        start_prompt = 'Summarize the following conversation.\n\n'
        end_prompt = '\n\nSummary: '
        prompt = [start_prompt + dialogue + end_prompt for dialogue in example_batch["dialogue"]]
        
        example_batch['input_ids'] = self.tokenizer(prompt, padding="max_length", truncation=True, return_tensors="pt").input_ids
        
        with self.tokenizer.as_target_tokenizer():
            example_batch['labels'] = self.tokenizer(example_batch["summary"], padding="max_length", truncation=True, return_tensors="pt").input_ids
            
        return example_batch
    

    def convert(self):
        dataset = load_from_disk(self.config.data_path)
        tokenized_dataset = dataset.map(self.convert_examples_to_features, batched = True)
        tokenized_dataset = tokenized_dataset.remove_columns(['id', 'topic', 'dialogue', 'summary',])
        tokenized_dataset.save_to_disk(os.path.join(self.config.root_dir,"DialogSum"))