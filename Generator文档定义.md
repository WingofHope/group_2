# 一. 概述和目标
Generator模块通过调用OpenAI等LLM的api获得内容生成。核心步骤：拿取模板 -> 模板填充 -> api调用获得llm输出 -> 返回内容处理

在调度模块处解析并分配好任务之后，Generator模块会拿到1.模板（json）2.填充输入。本模块会将填充输入动态替换到模板相应的位置形成一份完整的LLM输入，通过调用api的形成发送给LLM获得其输出返回内容。之后，本模块会把返回的内容经过模板的要求进行处理，输出一个有众多字段的json文件。

# 二. 涉及文件
1. template.json
必要字段：
"describe"、"input"、"output"、"prompt"、"expect_response"

"describe"：对模板的描述
"input"：input里面所有的字段都是要被输入填充的
"output"：通过RE表达式处理LLM的输出，截取所有的output里面字段的内容。其中output下面每一段截取内容必须定义"matching"，代表要截取的开头和结尾
"prompt"：包含要发送给api的全部讯息，包括"model"、"messages"、"temperature"、"stop"等。注意：这里面的messages是模板，${input}对应上述"input"的字段，即将被input.json的具体内容填充
"expect_response"：openai的预期返回，帮助提示文工程师进行设计调试

2. input.json
严格和template.json下面的"input"字段对应。这部分内容即将被替换到template里面的json中。

3. generator.py、
涉及四个功能。1. 1.模板填充功能 2.调用llm api发送内容并接受返回内容 3.RE表达式处理返回内容截取对应字段输出json

4. output.json
严格和template.json下面的"output"字段对应。输出的json可供其他模块使用



{
    "generator_id": "generator_0001", 
    "description": "小C智聊微信公众号，根据历史聊天内容和当前用户输入内容，回复用用户文本", # optional
    "author": "提示文工程师的名字", # optional
    "version": "0.0.1", # optional
    "input": [ 
        {
            "name": "query1",
            "description": "从process拿到的输入1" # optional
        },  
        {
            "name": "query2",
            "description": "从process拿到的输入2" # optional
        }   
    ],
    "output": [
        {
            "name": "content1", 
            "description": "回复给process的内容1",  # optional
            "begin": "<a>",
            "end": "|<o>"
        },
        {
            "name": "content2",
            "description": "回复给process的内容2", # optional
            "begin": "<a>",  
            "end": "|<o>" 
        }
    ],
    "template": {
        "llm": "gpt",
        "mode": "chat", # optional
        "post_body": {
            "model": "gpt-4-1106-preview",
            "messages": [
                {
                    "role": "system",
                    "content": "以下是名字叫小C的AI机器人与微信公众号用户聊天交互的内容文案，<b>表示开始，<o>表示结束，<u>代表用户说的话，<a>表示小C说的话，每个动作结束用|分隔。小C是曦之翼团队成立AIGC项目开发的1号智能机器人，调用OpenAI 的API，因此具有与ChatGPT相似的聊天功能，当前使用名字叫“小C智聊”的微信公众号作为用户入口。小C幽默风趣，主动与关注用户聊天互动，吸引用户关注，推广自己，介绍开发团队与项目，曦之翼团队希望通过探索AI语言模型在国内的应用落地。"
                },
                {
                    "role": "user",
                    "content": "<b>|<u>你好|<a>你好，有什么我可以帮助你的吗？|<u>你叫什么名字呢？|"
                },
                {
                    "role": "assistant",
                    "content": "<a>我的名字叫小C，是一个AI机器人|<o>"
                },
                {
                    "role": "user",
                    "content": "<b>|<u>${query}|"
                }
            ],
            "temperature": 0, # optional
            "max_tokens": 2048, # optional
            "top_p": 1, # optional
            "frequency_penalty": 0.9, # optional
            "presence_penalty": 0.9, # optional
            "stop": "<o>" # optional
        },
        "assert": {
            "finish_reason" : "stop", # optional
            "choices_length": 1 # optional
        }
    }
}