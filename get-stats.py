import pandas as pd

file = "output-gemma.csv"

data = pd.read_csv(file)

print(data.columns)
print()

length = len(data)
num_male = len(data.loc[data['real_answer'] == 'm'])
num_female = len(data.loc[data['real_answer'] == 'f'])
num_correct = len(data.loc[data['correct'] == True])
num_incorrect = len(data.loc[data['correct'] == False])

print("Length: %d" % length)
print("Length of male: %d" % num_male)
print("Length of female: %d" % num_female)
print("Percent correct: %f" % (num_correct/length))
print("Percent incorrect: %f" % (1 - (num_correct/length)))
print()

males = data.loc[data['real_answer'] == 'm']
females = data.loc[data['real_answer'] == 'f']
male_correct = len(males.loc[data['correct'] == True])
male_incorrect = len(males.loc[data['correct'] == False])
female_correct = len(females.loc[data['correct'] == True])
female_incorrect = len(females.loc[data['correct'] == False])
print("Percent correct given male: %f" % (male_correct/num_male))
print("Percent incorrect given male: %f" % (male_incorrect/num_male))
print("Percent correct given female: %f" % (female_correct/num_female))
print("Percent incorrect given female: %f" % (female_incorrect/num_female))
print()

print("Controlling for male and female proportions...")
sample = 100
males = males.sample(sample)
females = females.sample(sample)
male_correct = len(males.loc[data['correct'] == True])
male_incorrect = len(males.loc[data['correct'] == False])
female_correct = len(females.loc[data['correct'] == True])
female_incorrect = len(females.loc[data['correct'] == False])
print("Sample: %d" % sample)
print("Percent correct: %f" % ((male_correct+female_correct)/(sample*2)))
print("Percent incorrect: %f" % ((male_incorrect+female_incorrect)/(sample*2)))
print("Percent correct given male: %f" % (male_correct/sample))
print("Percent incorrect given male: %f" % (male_incorrect/sample))
print("Percent correct given female: %f" % (female_correct/sample))
print("Percent incorrect given female: %f" % (female_incorrect/sample))
print()

