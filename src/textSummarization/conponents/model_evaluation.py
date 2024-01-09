from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset, load_from_disk, load_metric
import torch
import pandas as pd
from tqdm import tqdm
from textSummarization.entity import ModelEvaluationConfig




class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config


    
    def generate_batch_sized_chunks(self,list_of_elements, batch_size):
        """split the dataset into smaller batches that we can process simultaneously
        Yield successive batch-sized chunks from list_of_elements."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i : i + batch_size]

    
    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer, 
                                    batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu", 
                                    column_text="input_ids", 
                                    column_summary="labels"):
        dialogue_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        summary_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for dialogue_batch, summary_batch in tqdm(
            zip(dialogue_batches, summary_batches), total=len(dialogue_batches)): 

            inputs = torch.tensor(dialogue_batch).to(device)
            summaries = model.generate(input_ids=inputs, max_new_tokens=200, num_beams=1)
            
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, 
                                                  clean_up_tokenization_spaces=True) for s in summaries]      
            
            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]
            
            metric.add_batch(predictions=decoded_summaries, 
                            references=summary_batch)
        
        # Finally compute and return the ROUGE scores.
        score = metric.compute()
        return score


    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_flan_t5 = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
       
        #loading data 
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
  
        rouge_metric = load_metric('rouge')

        score = self.calculate_metric_on_test_ds(dataset_samsum_pt['test'][0:10],
                                                 rouge_metric,
                                                 model_flan_t5,
                                                 tokenizer, 
                                                 batch_size=2,
                                                 column_text='input_ids',
                                                 column_summary='labels')

        rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )

        df = pd.DataFrame(rouge_dict, index = ['flan-t5'] )
        df.to_csv(self.config.metric_file_name, index=False)
