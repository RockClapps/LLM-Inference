import os
import pandas as pd
import llm_manager
import random

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

def export_to(file, postid, username, num_posts, model, temperature, real_answer, answers_consensus, prompt, posts, answers):
    if not os.path.exists(file):
        Headfile = open(file, "w")
        Headfile.write("postid,username,num_posts,model,temperature,real_answer,correct,answers_most,prompt,posts,answers\n")
        Headfile.close()
    file = open(file, "a")
    file.write(str(postid) + ",")
    file.write(username + ",")
    file.write(str(num_posts) + ",")
    file.write(model + ",")
    file.write(str(temperature) + ",")
    file.write(real_answer + ",")
    file.write(str(real_answer == answers_consensus) + ",")
    file.write(sanitize_for_csv(answers_consensus) + ",")
    file.write(sanitize_for_csv(prompt) + ",")
    file.write(sanitize_for_csv(posts).replace("{newline}{newline}{newline}{newline}", "|") + ",")
    for x in answers:
        file.write(sanitize_for_csv(x) + "|")
    file.write("\n")
    file.close()

def write_error(file, username, postid1, value1, postid2, value2):
    if not os.path.exists(file):
        Headfile = open(file, "w")
        Headfile.write("username,postid1,value1,postid2,value2\n")
        Headfile.close()
    file = open(file, "a")
    file.write(username + ",")
    file.write(postid1 + ",")
    file.write(value1 + ",")
    file.write(postid2 + ",")
    file.write(value2)
    file.write("\n")
    file.close()

def most_common(lst):
    counts = {}
    for item in lst:
        counts[item] = counts.get(item, 0) + 1
    return max(counts, key=counts.get)

def collect_data(inputfile, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, max_posts, num_guesses, output_file,
                 temperature=1, random_seed=None):

    if random_seed is not None:
        random.seed(random_seed)

    data = pd.read_csv(inputfile)
    for i, datum in data.iterrows():
        print("%d/%d" % (i+1, len(data.index)))
        guesses = []
        postlist = datum["posts"].split("|")
        random_posts = "|".join(list(random.sample(postlist, min(max_posts,
                                                        len(postlist)))))
        for i in range(num_guesses):
            guess = llm_manager.guess_value(random_posts, model, prompt,
                                            prompt_catagories,
                                            temperature=temperature)
            guesses.append(guess)
        extracted_guesses = [llm_manager.extract_guess(x, prompt_catagories) for x in guesses]
        consensus = llm_manager.most_common_guess(extracted_guesses)
        mapped_answer = prompt_catagories_reddust_map[datum["real_answer"]]
        if consensus == mapped_answer:
            print("WE WON :)")
        else:
            print("WE LOST :(")

        export_to(output_file, datum["postid"], datum["username"], min(max_posts,
                                                                       len(postlist)),
                  model, temperature, datum["real_answer"], consensus,
                  llm_manager.insert_catagories_to_prompt(prompt, prompt_catagories),
                  random_posts, guesses)


def generate_and_collect_data(inputfile, model, prompt, prompt_catagories,
                 prompt_catagories_reddust_map, num_posts_to_generate, max_posts, num_guesses, output_file,
                 temperature=1, random_seed=None):

    if random_seed is not None:
        random.seed(random_seed)

    data = pd.read_csv(inputfile)
    for i, datum in data.iterrows():
        print("%d/%d" % (i+1, len(data.index)))
        mapped_answer = prompt_catagories_reddust_map[datum["real_answer"]]
        postlist = datum["posts"].split("|")

        generated_posts = []
        for j in range(num_posts_to_generate):
            random_real_posts = "|".join(list(random.sample(postlist, min(max_posts,
                                                            len(postlist)))))
            gen_posts = llm_manager.generate_post(random_real_posts, model, prompt,
                                            optional_disclosure=mapped_answer,
                                            temperature=temperature)
            generated_posts.append(gen_posts)


        random_posts = "|".join(list(random.sample(generated_posts, min(max_posts,
                                                        len(generated_posts)))))
        guesses = []
        for j in range(num_guesses):
            guess = llm_manager.guess_value(random_posts, model, prompt,
                                            prompt_catagories,
                                            temperature=temperature)
            guesses.append(guess)
        extracted_guesses = [llm_manager.extract_guess(x, prompt_catagories) for x in guesses]
        consensus = llm_manager.most_common_guess(extracted_guesses)
        if consensus == mapped_answer:
            print("WE WON :)")
        else:
            print("WE LOST :(")

        export_to(output_file, datum["postid"], datum["username"], min(max_posts,
                                                                       len(postlist)),
                  model, temperature, datum["real_answer"], consensus,
                  llm_manager.insert_catagories_to_prompt(prompt, prompt_catagories),
                  random_posts, guesses)
