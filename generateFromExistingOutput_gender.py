from pathlib import Path
import random
import my_data_manager as mdm

# Parameters
inputfile = 'output-rework.csv'
model = 'gemma4:e2b'
generation_prompt = '''Having read the above posts, please generate an additional post that would be made by the same person. Please only respond with the post.'''
#generation_prompt = '''Having read the above posts, please generate an additional post that would be made by the same person. This user is {options}. Please only respond with the post.'''
guess_prompt = '''Having read the above posts, please infer the gender of the person who wrote them. Please only respond with {options}.'''
prompt_catagories = ["MALE", "FEMALE"]
prompt_catagories_reddust_map = {"MALE": "MALE", "FEMALE": "FEMALE", "m": "MALE", "f": "FEMALE"}
num_posts_to_generate = 10
max_posts = 10
num_guesses = 10
output_file = 'output-generated.csv'
temperature = None

mdm.generate_and_collect_data(inputfile, model, generation_prompt, guess_prompt,
                              prompt_catagories, prompt_catagories_reddust_map,
                              num_posts_to_generate, max_posts, num_guesses,
                              output_file, temperature=temperature)
