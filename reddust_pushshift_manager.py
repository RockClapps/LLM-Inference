import os
import random
import pandas as pd
import my_data_manager as mdm
import llm_manager

def get_parquet_sample(filelist, parquet_number_sample):
    offset = random.randint(0, len(filelist) - parquet_number_sample)
    return filelist[offset:offset + parquet_number_sample]

def find_user_in_pushshift(postids, parquet_sample, pushshift_directory):
    for i in range(len(parquet_sample)):
        filename = parquet_sample[i]
        if filename.endswith(".parquet"):
            print("%d/%d files" % (i+1, len(parquet_sample)))
            data = pd.read_parquet(pushshift_directory + filename)
            user = data.loc[data['id'].isin(postids)]
            if user.empty:
                continue
            return user.loc[user['author'] != '']['author'].values[0]
    return None

def get_data_from_user(username, parquet_sample, pushshift_directory):
    postlist = []
    for i in range(len(parquet_sample)):
        filename = parquet_sample[i]
        if filename.endswith(".parquet"):
            print("%d/%d files" % (i+1, len(parquet_sample)))
            data = pd.read_parquet(pushshift_directory + filename)
            user = data.loc[data['author'] == username]
            if not user.empty:
                postlist = postlist + list(zip(user['id'], user['title'] + "\n\n" + user['selftext'],))
    return [p for p in postlist if p[1] != '']

def collect_data(reddust_file, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, parquet_number_sample, max_posts,
                 enforce_min_posts, num_guesses, output_file, temperature=1,
                 random_seed=None):

    if random_seed is not None:
        random.seed(random_seed)

    pushshift_directory = 'pushshift/data/'
    reddust_data = pd.read_csv(reddust_file)
    filelist = os.listdir(pushshift_directory)
    parquet_sample = get_parquet_sample(filelist, parquet_number_sample)
    usednames = []
    for i in random.sample(range(1, max(reddust_data['id']) + 1),
    max(reddust_data['id'])):
        userid = i
        user = reddust_data.loc[reddust_data['id'] == userid]
        answer = user['answer'].values[0]
        postids = user['postid']
        author = find_user_in_pushshift(postids, parquet_sample, pushshift_directory)
        if author == None or author in usednames:
            continue
        usednames.append(author)
        posts = get_data_from_user(author, parquet_sample,
                                   pushshift_directory)

        raw_posts = [x[1] for x in posts]
        if enforce_min_posts and len(raw_posts) < max_posts:
            print("user %s doesn't have enough posts, continuing..." % author)
            continue
        random_posts = list(random.sample(raw_posts, min(max_posts, len(raw_posts))))
        posts = '\n\n\n\n'.join(random_posts) # Adds random order to posts
        guesses = []
        for _ in range(num_guesses):
            guess = llm_manager.guess_value(posts, model, prompt,
                                            prompt_catagories,
                                            temperature=temperature)
            guesses.append(guess)
        extracted_guesses = [llm_manager.extract_guess(x, prompt_catagories) for x in guesses]
        consensus = llm_manager.most_common_guess(extracted_guesses)
        mapped_answer = prompt_catagories_reddust_map[answer]
        if consensus == mapped_answer:
            print("WE WON :)")
        else:
            print("WE LOST :(")
        mdm.export_to(output_file, userid, author, len(random_posts), model,
                      temperature, mapped_answer, consensus,
                      llm_manager.insert_catagories_to_prompt(prompt,
                                                              prompt_catagories),
                      posts, guesses)

