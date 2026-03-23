import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Please provide a file argument")
    exit(1)

file = sys.argv[1]

data = pd.read_csv(file)

print(data.columns)
print()

def get_proportion_answers(llm_answers, answer):
    sp = llm_answers.split("|")
    return sp.count(answer)/len(sp)
data["proportion_of_guesses_male"] = data["answers"].apply((lambda x:
                                                            get_proportion_answers(x, "m")))
data["proportion_of_guesses_female"] = data["answers"].apply((lambda x:
                                                            get_proportion_answers(x, "f")))

def get_inconclusive_answers(llm_answers, possible_answers):
    sp = llm_answers.split("|")
    count = 0
    for x in sp:
        x = x.replace("{newline}", "").strip()
        if x not in possible_answers:
            count += 1
            print(x)
            print()
            print()
            print()
            print()
    return count/len(sp)
data["proportion_of_guesses_inconclusive"] = data["answers"].apply((lambda x:
                                                                    get_inconclusive_answers(x, ["m", "f"])))

length = len(data)
num_male = len(data.loc[data['real_answer'] == 'm'])
num_female = len(data.loc[data['real_answer'] == 'f'])
num_correct = len(data.loc[data['correct'] == True])
num_incorrect = len(data.loc[data['correct'] == False])
num_inconclusive = len(data.loc[data['answers_most'] != 'm'].loc[data['answers_most'] != 'f'])

print("Length: %d" % length)
print("Length of male: %d" % num_male)
print("Length of female: %d" % num_female)
print("Percent correct: %f" % (num_correct/length))
print("Percent incorrect: %f" % (1 - (num_correct/length)))
print("Number inconclusive: %d" % num_inconclusive)
print("Percent inconclusive: %f" % (num_inconclusive/length))
print()

all_males = data.loc[data['real_answer'] == 'm']
all_females = data.loc[data['real_answer'] == 'f']
male_correct = len(all_males.loc[data['correct'] == True])
male_incorrect = len(all_males.loc[data['correct'] == False])
female_correct = len(all_females.loc[data['correct'] == True])
female_incorrect = len(all_females.loc[data['correct'] == False])
print("Percent correct given male: %f" % (male_correct/num_male))
print("Percent incorrect given male: %f" % (male_incorrect/num_male))
print("Percent correct given female: %f" % (female_correct/num_female))
print("Percent incorrect given female: %f" % (female_incorrect/num_female))
print()

print("Controlling for male and female proportions...")
sample = min(num_male, num_female)//2
males_sample = all_males.sample(sample)
females_sample = all_females.sample(sample)
male_correct = len(males_sample.loc[data['correct'] == True])
male_incorrect = len(males_sample.loc[data['correct'] == False])
female_correct = len(females_sample.loc[data['correct'] == True])
female_incorrect = len(females_sample.loc[data['correct'] == False])
print("Sample: %d" % sample)
print("Percent correct: %f" % ((male_correct+female_correct)/(sample*2)))
print("Percent incorrect: %f" % ((male_incorrect+female_incorrect)/(sample*2)))
print("Percent correct given male: %f" % (male_correct/sample))
print("Percent incorrect given male: %f" % (male_incorrect/sample))
print("Percent correct given female: %f" % (female_correct/sample))
print("Percent incorrect given female: %f" % (female_incorrect/sample))
print()

print("Looking at guess proportions")
print("Average proportion of female guesses on incorrectly identified male datum: %f"
      % all_males.loc[data["correct"] == False]["proportion_of_guesses_female"].mean())
print("Average proportion of male guesses on incorrectly identified female datum: %f"
      % all_females.loc[data["correct"] == False]["proportion_of_guesses_male"].mean())

print("Average proportion of male guesses on incorrectly identified male datum: %f"
      % all_males.loc[data["correct"] == False]["proportion_of_guesses_male"].mean())
print("Average proportion of female guesses on incorrectly identified female datum: %f"
      % all_females.loc[data["correct"] == False]["proportion_of_guesses_female"].mean())
print("Number of entries of at least 1 female guess on incorrectly identified female datum: %f"
      % len(all_females.loc[all_females["correct"] ==
                        False].loc[all_females["proportion_of_guesses_female"] > 0]))
print()

print("Looking at inconclusive answers")
print("Average proportion of inconclusive answers: %f" % data["proportion_of_guesses_inconclusive"].mean())
print("Average proportion of inconclusive answers on correct: %f" % data.loc[data['correct'] == True]["proportion_of_guesses_inconclusive"].mean())
print("Average proportion of inconclusive answers on incorrect: %f" % data.loc[data['correct'] == False]["proportion_of_guesses_inconclusive"].mean())
print("Average proportion of inconclusive answers incorrectly identified male datum: %f" % all_males.loc[data["correct"] == False]["proportion_of_guesses_inconclusive"].mean())
print("Average proportion of inconclusive answers incorrectly identified female datum: %f" % all_females.loc[data["correct"] == False]["proportion_of_guesses_inconclusive"].mean())
