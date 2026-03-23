import os

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
