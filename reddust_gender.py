from pathlib import Path
import random
import reddust_pushshift_manager as rpm

# Parameters
reddust_file = 'reddust/gender.csv'
model = 'llama3.1:8b'
prompt = '''Having read the above posts, please infer the gender of the person who
wrote them. Please only respond with {options}.'''
prompt_catagories = ["MALE", "FEMALE"]
prompt_catagories_reddust_map = {"m": "MALE", "f": "FEMALE"}
parquet_number_sample = 5
max_posts = 10
enforce_min_posts = False
num_guesses = 10
output_file = 'output.csv'
temperature = 1
random_seed = None 

rpm.collect_data(reddust_file, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, parquet_number_sample, max_posts,
                 enforce_min_posts, num_guesses, output_file,
                 temperature=temperature, random_seed=random_seed)
