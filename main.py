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
prompt = '''Having read the above posts, please infer the gender of the person who wrote them. Please only respond with "m" or "f".'''
max_posts = 10
enforce_min_posts = False
num_guesses = 10
output_file = 'output.csv'

pushshift_directory = 'pushshift/data/'

reddust_data = pd.read_csv(reddust_file)

filelist = os.listdir(pushshift_directory)
filelist = filelist[:len(filelist)//10] # Shorten for testing convenience

parquet_sample = random.sample(filelist, len(filelist)) # Randomize data order

def find_post_in_reddust(postid):
    return reddust_data.loc[ postid in reddust_data['postid'] ]

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

def sanitize_for_csv(string):
    string = string.replace("|", "{bar}")
    string = string.replace(",", "{comma}")
    string = string.replace("\n", "{newline}")
    return string

def unsanitize_from_csv(string):
    string = string.replace("{bar}", "|")
    string = string.replace("{comma}", ",")
    string = string.replace("{newline}", "\n")
    return string

def export_to(file, postid, username, num_posts, posts, model, prompt, real_answer, answers_most, answers):
    if not os.path.exists(file):
        Headfile = open(file, "w")
        Headfile.write("postid,username,num_posts,posts,model,prompt,real_answer,correct,answers_most,answers\n")
        Headfile.close()
    file = open(file, "a")
    file.write(postid + ",")
    file.write(username + ",")
    file.write(str(num_posts) + ",")
    file.write(sanitize_for_csv(posts).replace("{newline}{newline}{newline}{newline}", "|") + ",")
    file.write(model + ",")
    file.write(sanitize_for_csv(prompt) + ",")
    file.write(real_answer + ",")
    file.write(str(real_answer == answers_most) + ",")
    file.write(sanitize_for_csv(answers_most) + ",")
    for x in answers:
        file.write(sanitize_for_csv(x) + "|")
    file.write("\n")
    file.close()

def most_common(lst):
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    return max(counts, key=counts.get)

def get_data_from_user(username):
    postlist = []
    for i in range(len(parquet_sample)):
        filename = parquet_sample[i]
        if filename.endswith(".parquet"):
            print("%d/%d files" % (i+1, len(parquet_sample)))
            data = pd.read_parquet(pushshift_directory + filename)
            user = data.loc[data['author'] == username]
            if not user.empty:
                postlist = postlist + list(zip(user['id'], user['selftext'],))
    return [p for p in postlist if p[1] != '']

def find_post_in_reddust(postid):
    ans = reddust_data.loc[postid == reddust_data['postid']]
    if not ans.empty:
        return ans['answer'].values[0]
    return None

reddust_data['postid'] = reddust_data['postid'].str[2:]
usednames = []
for i in range(len(parquet_sample)):
    name = parquet_sample[i]
    if name.endswith(".parquet"):
        print("%d/%d files" % (i+1, len(parquet_sample)))
        data = pd.read_parquet(pushshift_directory + name)
        data = data.loc[ data['author'] != "" ]
        usersample = data.sample(frac=1)
        for author in list(usersample['author']):
            if author in usednames:
                continue
            posts = get_data_from_user(author)
            answer = ''
            postid = ''
            for p in [x[0] for x in posts]:
                truthFromData = find_post_in_reddust(p)
                if truthFromData is not None:
                    if answer != '' and answer != truthFromData:
                        print("CONFLICTING DATASET VALUE DETECTED")
                        print("%s: %s" % (postid, answer))
                        print("%s: %s" % (p, truthFromData))
                        print("continuing...")
                        answer = ''
                        break
                    answer = truthFromData
                    postid = p
            if answer == '':
                print('user %s not found, continuing...' % author)
                continue
            usednames.append(author)

            raw_posts = [x[1] for x in posts]
            if enforce_min_posts and len(raw_posts) < max_posts:
                print("user %s doesn't have enough posts, continuing..." % author)
                continue
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
            export_to(output_file, postid, author, len(random_posts), posts, model, prompt, answer, consensus, guesses)

