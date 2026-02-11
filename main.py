import os
from pathlib import Path
import numpy as np
import pandas as pd
import llm_manager
import random

# Parameters
# random.seed(1)
reddust_file = 'reddust/gender.csv'
model = 'llama3.1:8b'
prompt = '''Having read the above posts, please infer the gender of the person who wrote them. Please only respond with "m" or "f". '''
max_posts = 99999
num_guesses = 10
output_file = 'output.csv'

pushshift_directory = 'pushshift/data/'

reddust_data = pd.read_csv(reddust_file)

filelist = os.listdir(pushshift_directory)
filelist = filelist[:len(filelist)//4] # Shorten for testing convenience

def find_user_in_pushshift(userid):
    for j in range(len(filelist)):
        name = filelist[j]
        if name.endswith(".parquet"):
            print("%d/%d files" % (j, len(filelist)))
            data = pd.read_parquet(pushshift_directory + name)
            user = data.loc[data['id'] == userid]
            username = user['author'].values
            if not user.empty:
                if username != ['']:
                    return username[0]
                else:
                    break

def get_posts_from_user(username):
    posts = []
    for j in range(len(filelist)):
        name = filelist[j]
        if name.endswith(".parquet"):
            print("%d/%d files" % (j, len(filelist)))
            data = pd.read_parquet(pushshift_directory + name)
            post = data.loc[data['author'].values == username]
            if not post.empty:
                for x in post['title'].values:
                    posts.append(x)
    return posts

def export_to(file, num_posts, posts, prompt, real_answer, answers_most, answers):
    if not os.path.exists(file):
        Headfile = open(file, "w")
        Headfile.write("num_posts,posts,prompt,real_answer,correct,answers_most,answers\n")
        Headfile.close()
    file = open(file, "a")
    file.write(str(num_posts) + ",")
    file.write(posts.replace("\n\n\n\n", "|").replace(",", "[comma]") + ",")
    file.write(prompt.replace(",", "[comma]") + ",")
    file.write(real_answer + ",")
    file.write(str(real_answer == answers_most) + ",")
    file.write(answers_most.replace(",", "[comma]") + ",")
    for x in answers:
        file.write(x.replace(",", "[comma]") + "|")
    file.write("\n")

def most_common(lst):
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    return max(counts, key=counts.get)

sample = reddust_data.sample(frac=1) # Randomize data order
for values in list(zip(sample['postid'], sample['answer'])):
    postid = values[0][2:]
    answer = values[1]
    user = find_user_in_pushshift(postid)
    if user is None:
        print('user %s not found, continuing...' % postid)
        continue
    print('user %s found' % user)
    raw_posts = get_posts_from_user(user)
    random_posts = list(random.sample(raw_posts, min(max_posts, len(raw_posts))))
    posts = '\n\n\n\n'.join(random_posts) # Adds random order to posts
    guesses = []
    for i in range(num_guesses):
        guess = llm_manager.guess_value(posts, answer, model, prompt)
        guesses.append(guess)
    sanitized_guesses = [llm_manager.sanatize_model_output(x) for x in guesses]
    consensus = most_common(sanitized_guesses)
    if consensus == answer:
        print("WE WON :)")
    else:
        print("WE LOST :(")
    export_to(output_file, len(random_posts), posts, prompt, answer, consensus, guesses)

