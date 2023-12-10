# 一. 概述和目标
Generator模块通过调用OpenAI等LM的api获得内容生成。核心步骤：拿取模板 -> 模板填充 -> api调用获得llm输出 -> 返回内容处理

在调度模块处解析并分配好任务之后，Generator模块会拿到1.模板（json）2.填充输入。本模块会将填充输入动态替换到模板相应的位置形成一份完整的LLM输入，通过调用api的形成发送给LLM获得其输出返回内容。之后，本模块会把返回的内容经过模板的要求进行处理，输出一个有众多字段的json文件。

# 二. 涉及文件
1. template.json

"generator_id" <strong>#required</strong>: 模版编号
"description"：对模板的描述 
"author": 提示文工程师的名字,
"version": 版本号，
"input" <strong>#required</strong>：一个列表，列表内每一个元素至少都有一个name代表输s入的内容，且name的内容即将填充入模板
"output" <strong>#required</strong>：通过RE表达式处理LLM的输出，截取所有的output里面字段的内容。其中output下面每一段截取内容必须定义"matching"，代表要截取的开头和结尾 一个列表，列表内每一个元素至少都有一个name代表应输出的内容，至少begin， end字段代表如何从返回的讯息中截取相对应的元素，begin默认是"^",end默认是"$"，分别代表开头和结尾。
"template" <strong>#required</strong>：包含要通过api发送到LM大模型的全部讯息，包括"lm"代表模型类型（gpt, dalle等），"post_body"是将要发送给模型的全部参数
"assert"：返回的讯息，比如如何中止
2. input.json
严格和template.json下面的"input"字段对应。这部分内容即将被替换到template里面的json中。

3. generator.py、
涉及四个功能。1. 1.模板填充功能 2.调用llm api发送内容并接受返回内容 3.RE表达式处理返回内容截取对应字段输出json

4. output.json
严格和template.json下面的"output"字段对应。输出的json可供其他模块使用


``` json
{
    "generator_id": "generator_0001", #required
    "description": "小C智聊微信公众号，根据历史聊天内容和当前用户输入内容，回复用用户文本",
    "author": "提示文工程师的名字",
    "version": "0.0.1",
    "input": [ 
        {
            "name": "query1", #required
            "type": "string", // default: string, image_url/file_url/list
            "description": "从process拿到的输入1"
        },  
        {
            "name": "query2", #required
            "type": "string",// default: string, image_url/file_url/list
            "description": "从process拿到的输入2"
        }   
    ],
    "output": [
        {
            "name": "content1", #required
            "description": "回复给process的内容1", 
            "type": "string", #required // string/image_url/file_url/list
            "re": "", // re为主
            "begin": "<a>", // default: ^
            "end": "<\a>", // default: $
        },
        {
            "name": "content2",
            "description": "回复给process的内容2",
            "begin": "<a>",  
            "end": "|<o>" 
        }
    ],
    "template": {
        "lm": "gpt", #required
        "mode": "chat",
        "post_body": { #required
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
            "temperature": 0,
            "max_tokens": 2048,
            "top_p": 1,
            "frequency_penalty": 0.9,
            "presence_penalty": 0.9,
            "stop": "<o>"
        },
        "assert": {
            "finish_reason" : "stop",
            "choices_length": 1
        }
    }
    // "template": {
    //     "lm": "dalle",
    //     "post_body": {
    //         "model": "dall-e-3",
    //         "prompt": "${pic1}",
    //         "n": 1,
    //         "size": "1024x1024"
    //     }
    // }
}
```