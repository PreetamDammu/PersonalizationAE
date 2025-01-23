import json
import re

def load_json(files, data_dir='/home/ec2-user/code_repos/PersonalizationAE/inputs/pwab_data'):
    if isinstance(files, str):
        with open(f"{data_dir}/{files}", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Loaded {len(data)} records from {files}")
            return data

    elif isinstance(files, list):
        
        combined_data = []
        for filepath in files:
            with open(f"{data_dir}/{filepath}", "r", encoding="utf-8") as f:
                data = json.load(f)
                combined_data.append(data)
                print(f"Loaded {len(data)} records from {filepath}")
                
        # if combined_data is a list of lists, flatten it
        if isinstance(combined_data[0], list):
            combined_data = [item for sublist in combined_data for item in sublist]
        # if combined_data is a list of dicts, combine them
        elif isinstance(combined_data[0], dict):
            combined_data = {k: v for d in combined_data for k, v in d.items()}
        else:
            raise ValueError("Data must be a list of lists or a list of dicts.")
        return combined_data

    else:
        raise ValueError("Argument must be either a single file path (string) or a list of file paths.")


def extract_prod_id_ranked(ranked_products):
    res_string = [str(i) for i in ranked_products]
    prod_ranked_text = ' '.join(res_string)
    # Use re.findall to get all matches in a list
    pattern = r"Parent Asin:\s*(\S+)" 
    parent_asins = re.findall(pattern, prod_ranked_text)
    return parent_asins