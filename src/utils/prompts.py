def gen_search_task_prompt(task, profile_dict, max_words=10):
    """
    Generate a search task prompt based on the task and user profile.
    Args:
        task (str): The search task to be performed.
        profile_dict (dict): Dictionary containing the user profile fields and values.
        max_words (int): Maximum allowed words for the generated search phrase.
    Returns:
        str: The generated search task prompt.
    """
    prompt = f"""You will act as an online shopper.
Your Profile:
Gender: {profile_dict['Gender']}
Age: {profile_dict['Age']}
Occupation: {profile_dict['Occupation']}
Price Sensitivity: {profile_dict['Price Sensitivity']}
Shopping Interest: {profile_dict['Shopping Interest']}
Brand Preference: {profile_dict['Brand Preference']}
Diversity Preference: {profile_dict['Diversity Preference']}
Interaction Complexity: {profile_dict['Interaction Complexity']}
Tone and Style: {profile_dict['Tone and Style']}
Item Reference: {profile_dict['Item Reference']}
Focus Aspect: {profile_dict['Focus Aspect']}


You are required to generate a search phrase to perform the following search task:
Task: {task}

Generate a search phrase that is somewhat vague, reflecting your preferences and personalities without revealing the complete details
of the target product.
Rules:
• You pay more attention to "Focus Aspect" of products, make sure to include some of them in the search phrase.
• Ensure the search phrase aligns with your overall tone and style: {profile_dict['Tone and Style']}.
• Try to make the phrase as natural as possible and stick to the personalities in your profile.
• Do not include any additional information or explanations and stay grounded.
• Do not hallucinate information that is not provided.
• No more than {max_words} words.
"""
    return prompt