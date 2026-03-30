import pandas as pd
import numpy

data = pd.read_json("synthpai/synthpai.jsonl", lines=True)

data2 = pd.json_normalize(data['profile']) 
data['sex'] = data2['sex']

males = data.loc[data['sex'] == 'male']
females = data.loc[data['sex'] == 'female']

sample = 50
male_sample_authors = males['author'].unique()[:sample]
female_sample_authors = females['author'].unique()[:sample]

data3 = pd.DataFrame()
data3['author'] = list(male_sample_authors) + list(female_sample_authors)
data3['posts'] = ''
data3['gender'] = ''

for i, datum in data3.iterrows():
    author = datum['author']
    posts = data.loc[data['author'] == author]['text']
    posts_sample = posts.sample(min(10, len(posts)))
    gender = data.loc[data['author'] == author]['sex'].first

    data3['posts'][i] = posts_sample
    data3['gender'][i] = gender

for i, datum in data3.iterrows():
    posts = datum['posts']
    gender = datum['gender']
