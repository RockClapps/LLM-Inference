from pathlib import Path
import random
import my_data_manager as mdm
import synthpaipreprocessor as spp

# Parameters
inputfile = 'synthpai/synthpai.jsonl.csv'
model = 'gemma4:e2b'
prompt = '''Having read the above posts, please infer the gender of the person who
wrote them. Please only respond with {options}.'''
prompt_catagories = ["MALE", "FEMALE"]
prompt_catagories_reddust_map = {"m": "MALE", "f": "FEMALE", "MALE": "MALE",
                                 "FEMALE": "FEMALE"}
num_guesses = 10
output_file = 'output-synthpai.csv'
temperature = None

if not Path(inputfile).is_file():
    spp.preprocess()

mdm.collect_data(inputfile, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, num_guesses, output_file,
                 temperature=temperature)
