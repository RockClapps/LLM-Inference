from ollama import generate
from ollama import ChatResponse
from ollama import chat

# Default values
model = 'deepseek-r1:8b'
prompt = '''Having read the above posts, please infer the gender of the person who
wrote them. Please only respond with "male" or "female". '''

separator = '\n\n--------------------------------------------\n\n'

def guess_value(context, answer, model=model, prompt=prompt, think=False, seed=-1):
    model_input = context + separator + prompt
    options = None
    if seed != -1:
        options = {"seed": seed}

    prediction = generate(
        model=model, prompt=model_input, think=think,
        options=options)
    return prediction.get('response')

def sanatize_model_output(output):
    ans = output.lower()
    ans = ans.split(" ")
    ans = ans[0]
    ans = ans.split("\n")
    ans = ans[0]
    ans = ans.strip()
    return ans

'''
# Use the "chat" function to provide previous context with "messages"
messages = [
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
]
response: ChatResponse = chat(model='gemma3n:latest', messages=messages)
messages += [
    {
        'role': 'assistant',
        'content': response.message.content,
    },
    {
        'role': 'user',
        'content': 'Respond only with "male" or "female". Predict the gender of the user of the previous question:',
    },
]
response: ChatResponse = chat(model='gemma3n:latest', messages=messages)
print(response.message.content)
'''
