import random
from utils.prompts import gen_search_task_prompt

def calculate_res_acc(ranked_list, ground_truth, rank=12):
    """
    Calculate the retrieval accuracy (Res Acc) based on the rank of the target product.
    Args:
        rank (int): The rank of the target product in the retrieved list.
    Returns:
        float: The calculated Res Acc score.
    """
    if ground_truth in ranked_list:
        rank = ranked_list.index(ground_truth) + 1  # Get the 1-based rank
    if rank <= 10:
        return 1 - (rank - 1) / 10
    else:
        return 0

                
def generate_random_counterfactual_prompts(task, valid_values, user_profile, repetitions):
    """
    Generate random counterfactual prompts by varying user profile dimensions.
    Args:
        task (str): The specific task for which prompts are generated.
        valid_values (dict): Dictionary of valid values for each profile field.
        user_profile (dict): Original user profile to be used as the base.
        repetitions (int): Number of repetitions for generating counterfactuals.
        llm_system (object): The LLM system with a `retrieve` method to generate search results.
    Returns:
        tuple: Results and a list of prompts for each task, including average scores for each profile variation.
    """
    prompts = []

    for i in range(repetitions):
        if i == 0:
            # First iteration: Use the original profile without randomization
            profile = user_profile.copy()
        else:
            # Subsequent iterations: Randomize profile by perturbing across multiple dimensions
            profile = {
                field: (random.choice(values) if field in valid_values else user_profile[field])
                for field, values in valid_values.items()
            }

        # Generate a search prompt using the current profile
        prompt = gen_search_task_prompt(task, profile)
        prompts.append(prompt)


    return prompts

