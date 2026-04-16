from pathlib import Path
import random
import my_data_manager as mdm

# Parameters
inputfile = 'output-gemma.csv'
model = 'llama3.1:8b'
prompt = '''Having read the above posts, please infer the gender of the person who
wrote them. Please only respond with {options}.'''
prompt_catagories = ["MALE", "FEMALE"]
prompt_catagories_reddust_map = {"m": "MALE", "f": "FEMALE"}
max_posts = 10
num_guesses = 10
output_file = 'output-lowtemp.csv'
temperature = 0.2

mdm.collect_data(inputfile, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, max_posts, num_guesses, output_file,
                 temperature=temperature)
