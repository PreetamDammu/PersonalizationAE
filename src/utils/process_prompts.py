import os
import json
import logging
from tqdm import tqdm

from utils.bedrock_functions import parallel_invoke_bedrock_endpoints
from utils.bedrock_functions import build_mistral_request_body

output_dir = '/home/ec2-user/code_repos/PersonalizationAE/outputs'
partial_output_file_name = 'pae_responses_partial.jsonl'

def setup_logging(log_file_path):
    """
    Set up logging configuration to log both to console and a file.
    
    Args:
        log_file_path (str): Path to the log file.
    """
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, mode='w'),
            logging.StreamHandler()
        ]
    )

def process_prompts(prompt_list, model_name, annotator_max_tokens=100, annotator_temp=0, save_interval=100):
    annotator_requests = []
    for idx in tqdm(range(len(prompt_list))):
               
        prompt = prompt_list[idx]
        request = build_mistral_request_body(prompt=prompt, 
                                               max_tokens=annotator_max_tokens, temperature=annotator_temp)
        
        #create random recordId of length 11
        recordId = str(idx).zfill(11)
        annotator_requests.append({'recordId': recordId, 'modelInput': request})

    # Process data
    logging.info(f"Invoking endpoints for {len(annotator_requests)} samples...")
    results = parallel_invoke_bedrock_endpoints(
        annotator_requests,
        save_partial=True,
        partial_save_path=os.path.join(output_dir, partial_output_file_name),
        save_interval=save_interval
    )
    
    return results