from ollama import generate
from ollama import ChatResponse
from ollama import chat

# Default values
catagories_placeholder_string = "{options}"

separator = '\n\n--------------------------------------------\n\n'

def guess_value(context, model, prompt, prompt_catagories, think=False, temperature=None, seed=None):
    model_input = context + separator + insert_catagories_to_prompt(prompt,
                                                                 prompt_catagories)
    options = {}
    if seed is not None:
        options["seed"] = seed
    if temperature is not None:
        if temperature > 1:
            print("ERROR: temperature parameter must be between 0 and 1")
            exit(1)
        options["temperature"] = temperature

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

def extract_guess(output, options):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    sanatized = sanatize_model_output(output)
    san_options = [sanatize_model_output(x) for x in options]

    for i in range(len(san_options)):
        if sanatized == san_options[i]:
            return options[i]
        if len(sanatized) > len(san_options[i]):
            if san_options[i] == sanatized[:len(san_options[i])] and sanatized[len(san_options) + 1] not in alphabet:
                return options[i]

    return "INCONCLUSIVE"

def insert_catagories_to_prompt(prompt, prompt_catagories):
    if catagories_placeholder_string not in prompt:
        print("ERROR: prompt needs to contain \"" + catagories_placeholder_string + "\" string")
        exit(1)
    if len(prompt_catagories) < 2:
        print("ERROR: prompt_catagories needs at least two options")
        exit(1)
    catagories_string = ""
    if len(prompt_catagories) == 2:
        catagories_string = prompt_catagories[0] + " or " + prompt_catagories[1]
    else:
        for i in range(len(prompt_catagories) - 1):
            catagories_string += prompt_catagories[i] + ", "
        catagories_string += "or " + prompt_catagories[-1]
    return prompt.replace(catagories_placeholder_string, catagories_string)

