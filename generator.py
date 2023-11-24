# template version 3
# 2023/10/06
# Hou Yi

# Task: template fill
# read template.json and fill the input into {} and send the messages to openai

import openai
import re
import os
import json
from collections import defaultdict


# openai.api_key = os.getenv("OPENAI_API_KEY")
# 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     "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"
openai.api_key = "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" # GPT-4

template_file = "/Users/yihou/Documents/projects/ai_agent_23_10/Genrator模块设计/template1.json"
data_file = "/Users/yihou/Documents/projects/ai_agent_23_10/Genrator模块设计/input1.json"
# 打开并读取JSON文件
with open(template_file, 'r', encoding='utf-8') as file:
    template = json.load(file)
with open(data_file, 'r', encoding='utf-8') as file:
    data = json.load(file)
    
# ur_input = input("用户：") 
# user_inputs = [ur_input]
def template_fill(template, data):
    user_inputs = data["input"]
    assert len(user_inputs) == len(template["input"])

    for message in template["prompt"]["messages"]:

        # 1. try catch, raise error
        # for key in list(template["input"].keys()):
        #     try: 
        #         placeholder = "${{{}}}".format(key)
        #         message["content"] = message["content"].replace(placeholder, user_inputs[key])
        #     except KeyError:
        #         print(f"User input doesn't contain the key: {key}.")

        # 2. dont raise error, if user_inputs has key, replace, otherwise, keep original
        for key in template["input"].keys():
            placeholder = "${{{}}}".format(key) # ${query}
            if key in user_inputs:
                message["content"] = message["content"].replace(placeholder, user_inputs[key])
                
    response = openai.ChatCompletion.create(
        **template["prompt"]
    )
    content = response.choices[0].message.content
    output = defaultdict(str)

    for key, value in template["output"].items():
        if "regular_expression" in value:
            expression = value["regular_expression"]
            #matches = re.findall(expression, content, re.DOTALL)
            matches = re.search(expression, content, re.DOTALL)
            returned_answer = matches.group(1).strip()
            output[key] = returned_answer
        else:
            #output[key] = "Not find matched answer!"
            output[key] = content

    # print(output)
    return output

if __name__ == "__main__":
    returned_message = template_fill(template, data)
    print(returned_message)