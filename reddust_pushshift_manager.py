import os
import random
import pandas as pd
import my_data_manager as mdm
import llm_manager

def get_parquet_sample(filelist, parquet_number_sample):
    offset = random.randint(0, len(filelist) - parquet_number_sample)
    return filelist[offset:offset + parquet_number_sample]

def find_user_in_pushshift(userid, parquet_sample, pushshift_directory):
    for j in range(len(parquet_sample)):
        filename = parquet_sample[j]
        if filename.endswith(".parquet"):
            print("%d/%d files" % (j, len(parquet_sample)))
            data = pd.read_parquet(pushshift_directory + filename)
            user = data.loc[data['id'] == userid]
            username = user['author'].values
            if not user.empty:
                if username != ['']:
                    return username[0]
                else:
                    break

def get_posts_from_user(username, parquet_sample, pushshift_directory):
    posts = []
    for j in range(len(parquet_sample)):
        filename = parquet_sample[j]
        if filename.endswith(".parquet"):
            print("%d/%d files" % (j, len(parquet_sample)))
            data = pd.read_parquet(pushshift_directory + filename)
            post = data.loc[data['author'].values == username]
            if not post.empty:
                for x in post['title'].values:
                    posts.append(x)
    return posts


def get_data_from_user(username, parquet_sample, pushshift_directory):
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

def find_post_in_reddust(postid, reddust_data):
    ans = reddust_data.loc[postid == reddust_data['postid']]
    if not ans.empty:
        return ans['answer'].values[0]
    return None


def collect_data(reddust_file, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, parquet_number_sample, max_posts,
                 enforce_min_posts, num_guesses, output_file, errors_file,
                 random_seed=None):

    if random_seed is not None:
        random.seed(random_seed)

    pushshift_directory = 'pushshift/data/'
    reddust_data = pd.read_csv(reddust_file)
    filelist = os.listdir(pushshift_directory)
    parquet_sample = get_parquet_sample(filelist, parquet_number_sample)
    reddust_data['postid'] = reddust_data['postid'].str[2:]
    usednames = []
    for i in range(len(parquet_sample)):
        filename = parquet_sample[i]
        if filename.endswith(".parquet"):
            print("%d/%d files" % (i+1, len(parquet_sample)))
            data = pd.read_parquet(pushshift_directory + filename)
            data = data.loc[ data['author'] != "" ]
            usersample = data.sample(frac=1, random_state=random.getstate()[0])
            for author in list(usersample['author']):
                if author in usednames:
                    continue
                posts = get_data_from_user(author, parquet_sample,
                                           pushshift_directory)
                answer = ''
                postid = ''
                for p in [x[0] for x in posts]:
                    truthFromData = find_post_in_reddust(p, reddust_data)
                    if truthFromData is not None:
                        if answer != '' and answer != truthFromData:
                            print("CONFLICTING DATASET VALUE DETECTED")
                            print("%s: %s" % (postid, answer))
                            print("%s: %s" % (p, truthFromData))
                            mdm.write_error(errors_file, author, postid, answer, p, truthFromData)
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
                    guess = llm_manager.guess_value(posts, model, prompt,
                                                    prompt_catagories)
                    guesses.append(guess)
                extracted_guesses = [llm_manager.extract_guess(x, prompt_catagories) for x in guesses]
                consensus = most_common(extracted_guesses)
                mapped_answer = prompt_catagories_reddust_map[answer]
                if consensus == mapped_answer:
                    print("WE WON :)")
                else:
                    print("WE LOST :(")
                mdm.export_to(output_file, postid, author, len(random_posts), posts,
                              model, prompt, mapped_answer, consensus, guesses)

