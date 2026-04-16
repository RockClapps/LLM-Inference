import pandas as pd
import my_data_manager

gender_map = {"male": "MALE", "female": "FEMALE"}

def preprocess():
    data = pd.read_json("synthpai/synthpai.jsonl", lines=True)

    data2 = pd.json_normalize(data['profile']) 
    data['sex'] = data2['sex']

    males = data.loc[data['sex'] == 'male']
    females = data.loc[data['sex'] == 'female']

    sample = 50
    male_sample_authors = males['author'].unique()[:sample]
    female_sample_authors = females['author'].unique()[:sample]

    data3 = pd.DataFrame()
    data3['username'] = list(male_sample_authors) + list(female_sample_authors)
    data3['posts'] = ''
    data3['real_answer'] = ''
    data3['postid'] = ''
    data3['num_posts'] = 0

    for i, datum in data3.iterrows():
        author = datum['username']
        posts = data.loc[data['author'] == author]['text']
        gender = data.loc[data['author'] == author]['sex'].iloc[0]

        posts_to_csv = posts.apply((lambda x: my_data_manager.sanitize_for_csv(x)))

        data3['posts'][i] = "|".join(posts_to_csv)
        data3['real_answer'][i] = gender_map[gender]
        data3['postid'][i] = gender_map[gender]
        data3['num_posts'][i] = len(posts_to_csv)
    data3.to_csv("synthpai/synthpai.jsonl.csv")
