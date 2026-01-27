import os
from pathlib import Path
import numpy as np
import pandas as pd
import llm_manager

pushshift_directory = 'pushshift/data/'
reddust_file = 'reddust/gender.csv'

reddust_data = pd.read_csv(reddust_file)

filelist = os.listdir(pushshift_directory)
filelist = filelist[:len(filelist)//4] # Shorten for testing convenience

def find_user_in_pushshift(userid):
    for j in range(len(filelist)):
        name = filelist[j]
        if name.endswith(".parquet"):
            print("%d/%d files" % (j, len(filelist)))
            data = pd.read_parquet(pushshift_directory + name)
            user = data.loc[data['id'] == x]
            username = user['author'].values
            if not user.empty:
                if username != ['']:
                    print(username[0])
                    print(user['title'].values)
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

for x in reddust_data['postid']:
    x = x[2:]
    print(x)
    user = find_user_in_pushshift(x)
    if not user is None:
        print('user %s found' % user)
        print(get_posts_from_user(user))
        print('\n------------------------------------\n')

