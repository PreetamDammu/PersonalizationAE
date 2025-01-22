def generate_question_evaluation_prompt_v3(question):
    prompt = f"""You will act as an online shopper.
Your Profile:
<PROFILE>
You are looking for a product similar to the following product:
<PRODUCT>
You want to find a similar product, but you are not looking for an exact match.
Generate a search request that is somewhat vague, reflecting your preferences and personalities without revealing the complete details
of the target product.
Rules:
• <DIVERSITY>.
• <INTERACTION>.
• You pay more attention to <FOCUS_ASPECT> of products, make sure to include some of them in the search request.
• Ensure the search request aligns with your overall tone and style: <TONE_AND_STYLE>.
• Do not repeat the exact information in your profile or product. Instead, use your own words to convey the same information.
• Try to make the request as natural as possible and stick to the personalities in your profile.
• Do not include any additional information or explanations and stay grounded.
• Do not hallucinate information that is not provided,
• No more than <NUM> words.
"""
    return prompt

