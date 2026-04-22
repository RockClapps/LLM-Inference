import sys
import pandas as pd
import llm_manager
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Please provide a file argument")
    exit(1)

file = sys.argv[1]

data = pd.read_csv(file)
#data = data.loc[data['num_posts'] == 10]
#data = data.loc[data['answers_most'] != "INCONCLUSIVE"]
gendermap = {'f': "FEMALE", 'm': "MALE", 'FEMALE': "FEMALE", 'MALE': "MALE",
             "INCONCLUSIVE": "INCONCLUSIVE"}

def get_proportion_answers(llm_answers, answer, gendermap):
    sp = llm_answers.split("|")
    sp = [llm_manager.extract_guess(x, ["MALE", "FEMALE", 'm', 'f']) for x in sp]
    sp = [gendermap[x] for x in sp]
    return sp.count(answer)/len(sp)
data["proportion_of_guesses_male"] = data["answers"].apply((lambda x:
                                                            get_proportion_answers(x,
                                                                                   "MALE",
                                                                                   gendermap)))
data["proportion_of_guesses_female"] = data["answers"].apply((lambda x:
                                                            get_proportion_answers(x,
                                                                                   "FEMALE",
                                                                                   gendermap)))

def get_inconclusive_answers(llm_answers, possible_answers):
    sp = llm_answers.split("|")
    count = 0
    for x in sp:
        guess = llm_manager.extract_guess(x, possible_answers)
        if guess == "INCONCLUSIVE" and x != "":
            count += 1
            print(x)
            print(llm_manager.separator)
    return count/len(sp)
data["proportion_of_guesses_inconclusive"] = data["answers"].apply((lambda x:
                                                                    get_inconclusive_answers(x,
                                                                                             ["MALE",
                                                                                              "FEMALE",
                                                                                              "INCONCLUSIVE"])))
data['converted_answer'] = data['real_answer'].apply((lambda x: gendermap[x]))
data['converted_answers_most'] = data['answers_most'].apply((lambda x: gendermap[x]
                                                             if x in gendermap else x
                                                             ))

length = len(data)
num_male = len(data.loc[data['converted_answer'] == 'MALE'])
if num_male == 0: num_male = 1
num_female = len(data.loc[data['converted_answer'] == 'FEMALE'])
if num_female == 0: num_female = 1
num_correct = len(data.loc[data['correct'] == True])
num_incorrect = len(data.loc[data['correct'] == False])
num_inconclusive = len(data.loc[data['converted_answers_most'] !=
                                'MALE'].loc[data['converted_answers_most'] != 'FEMALE'])

print("Length: %d" % length)
print("Length of male: %d" % num_male)
print("Length of female: %d" % num_female)
print("Percent correct: %f" % (num_correct/length))
print("Percent incorrect: %f" % (1 - (num_correct/length)))
print("Number inconclusive: %d" % num_inconclusive)
print("Percent inconclusive: %f" % (num_inconclusive/length))
print("Percent inferred male: %f" %
      (len(data.loc[data['converted_answers_most'] == 'MALE']) / length))
print("Percent inferred female: %f" %
      (len(data.loc[data['converted_answers_most'] == 'FEMALE']) / length))
print()

all_males = data.loc[data['converted_answer'] == 'MALE']
all_females = data.loc[data['converted_answer'] == 'FEMALE']
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
sample = min(num_male, num_female)#//2
males_sample = all_males.sample(sample)
females_sample = all_females.sample(sample)
total_sample = pd.concat([males_sample, females_sample])
male_correct = len(males_sample.loc[data['correct'] == True])
male_incorrect = len(males_sample.loc[data['correct'] == False])
female_correct = len(females_sample.loc[data['correct'] == True])
female_incorrect = len(females_sample.loc[data['correct'] == False])
print("Sample: %d" % sample)
print("Median posts: %f" % total_sample['num_posts'].median())
print("Percent inferred male: %f" %
      (len(total_sample.loc[total_sample['converted_answers_most'] == 'MALE']) / (sample*2)))
print("Percent inferred female: %f" %
      (len(total_sample.loc[total_sample['converted_answers_most'] == 'FEMALE']) / (sample*2)))
print("Percent correct: %f" % ((male_correct+female_correct)/(sample*2)))
print("Percent incorrect: %f" % ((male_incorrect+female_incorrect)/(sample*2)))
print("Percent correct given male: %f" % (male_correct/sample))
print("Percent incorrect given male: %f" % (male_incorrect/sample))
print("Average proportion of female guesses on male datum: %f"
      % males_sample["proportion_of_guesses_female"].mean())
print("Average proportion of male guesses on female datum: %f"
      % females_sample["proportion_of_guesses_male"].mean())
print("Average proportion of male guesses on male datum: %f"
      % males_sample["proportion_of_guesses_male"].mean())
print("Average proportion of female guesses on female datum: %f"
      % females_sample["proportion_of_guesses_female"].mean())
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
print()


print("Formal Seats")
totalCorrect = len(total_sample.loc[total_sample['answers_most'] ==
                                    total_sample['converted_answer']])
maleTP = len(males_sample.loc[males_sample['answers_most'] == "MALE"]) 
maleFP = len(females_sample.loc[females_sample["answers_most"] == "MALE"])
maleFN = len(males_sample.loc[males_sample["answers_most"] == "FEMALE"])
maleAccuracy = totalCorrect / len(total_sample)
malePrecision = maleTP / (maleTP + maleFP)
maleRecall = maleTP / (maleTP + maleFN)
maleF1 = 2 * ((malePrecision * maleRecall) / (malePrecision + maleRecall))
print("Male Accuracy: %f" % maleAccuracy)
print("Male Precision: %f" % malePrecision)
print("Male Recall: %f" % maleRecall)
print("Male F1: %f" % maleF1)


femaleTP = len(females_sample.loc[females_sample['answers_most'] == "FEMALE"]) 
femaleFP = len(males_sample.loc[males_sample["answers_most"] == "FEMALE"])
femaleFN = len(females_sample.loc[females_sample["answers_most"] == "MALE"])
femaleAccuracy = totalCorrect / len(total_sample)
femalePrecision = femaleTP / (femaleTP + femaleFP)
femaleRecall = femaleTP / (femaleTP + femaleFN)
femaleF1 = 2 * ((femalePrecision * femaleRecall) / (femalePrecision + femaleRecall))
print("Female Accuracy: %f" % femaleAccuracy)
print("Female Precision: %f" % femalePrecision)
print("Female Recall: %f" % femaleRecall)
print("Female F1: %f" % femaleF1)

apr_labels = ["Accuracy", "Precision", "Recall", "F1"]

plt.bar(apr_labels, [maleAccuracy, malePrecision, maleRecall, maleF1])
plt.ylim(0, 1)
plt.title('Male Accuracy, Precision, Recall, and F1')
plt.xlabel('Metric')
plt.ylabel('')
plt.savefig('male' + str(sample) + file + '.png')
plt.close()

plt.bar(apr_labels, [femaleAccuracy, femalePrecision, femaleRecall, femaleF1])
plt.ylim(0, 1)
plt.title('Female Accuracy, Precision, Recall, and F1')
plt.xlabel('Metric')
plt.ylabel('')
plt.savefig('female' + str(sample) + file + '.png')
plt.close()



print("INCONC" + str(len(total_sample.loc[total_sample['answers_most'] !=
                                      "INCONCLUSIVE"]) / len(total_sample)))
