import os

import json
from tqdm import tqdm
import pandas as pd
from utils.bedrock_functions import build_anthropic_request_body, invoke_bedrock_endpoint
from utils.prompts import gen_search_task_prompt
from utils.pae_functions import generate_random_counterfactual_prompts, calculate_res_acc
from utils.process_prompts import process_prompts
from utils.search_product_by_query import search_product_by_query

from utils.misc_helpers import load_json, extract_prod_id_ranked

import random
# Set random seed for reproducibility
random.seed(7)

cw_dir = '/home/ec2-user/code_repos/PersonalizationAE'
ip_dir = 'inputs/pwab_data'
op_dir = 'outputs'
filenames = os.listdir(f'{cw_dir}/{ip_dir}')

# Identify files belonging to 'all_products'
all_products_files = [
    f for f in filenames
    if f.startswith("all_products_part_") and f.endswith(".json")
]

# Identify files belonging to 'user_history'
user_history_files = [
    f for f in filenames
    if f.startswith("user_history_part_") and f.endswith(".json")
]

# Sort files if desired (e.g., to ensure consistent order)
all_products_files.sort()
user_history_files.sort()
all_products = load_json(all_products_files)
user_history = load_json(user_history_files)
user_instructions = load_json("user_instructions.json")
user_profiles = load_json("user_profiles.json")


user_prof_list = []
for i in range(len(user_instructions['train'])):
    user_prof_list.append(user_profiles[user_instructions['train'][i]['user_id']]['user_profile'])
df = pd.DataFrame(user_prof_list)


unique_vals = {}
for col in df.columns:
    unique_vals[col] = df[col].unique()
df_tasks = pd.DataFrame(user_instructions['train'])
df_tasks_search = df_tasks[df_tasks['type'] == 'search']

#randomly select 10 search tasks
df_search_sample = df_tasks_search.sample(n=10)

task_results = {}
for idx in tqdm(range(len(df_search_sample))):
    
    user_task = df_search_sample.iloc[idx]['task']
    target_prod = df_search_sample.iloc[idx]['target']['product_info']['parent_asin']
    user_profile = user_profiles[df_search_sample.iloc[idx]['user_id']]['user_profile']
    valid_values = unique_vals

    # Run the evaluation
    prompts = generate_random_counterfactual_prompts(user_task, valid_values, user_profile, repetitions=10)

    res = process_prompts(prompts, 'anthropic')
    res_dict = {}
    for i in range(len(res)):
        entry = []
        search_phrase_generated = res[i]['response']['outputs'][0]['text']
        entry.append(search_phrase_generated)
        
        search_res = search_product_by_query(search_phrase_generated)
        get_prod_ids = extract_prod_id_ranked(search_res)
        entry.append(get_prod_ids)
        
        
        entry.append(target_prod)
        entry.append(calculate_res_acc(get_prod_ids, target_prod))
        # entry.append()
        res_dict[i] = entry
        
    task_results[idx] = res_dict
    
    
# Save results to a file
os.makedirs(f'{cw_dir}/{op_dir}', exist_ok=True)
output_file = f'{cw_dir}/{op_dir}/search_task_resultsR.json'
with open(output_file, 'w') as f:
    json.dump(task_results, f)

