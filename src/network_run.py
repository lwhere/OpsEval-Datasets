import os
import json
import prompt

from tqdm import tqdm
from groq import Groq

client = Groq(
    api_key = os.environ.get("GROQ_API_KEY"),
)

en = 1
cot = 1
noq = 5
shot = 3
model = "gemma-7b-it"
structure = "json"

with open(f"data/test/Wired Network {'English' if en == 1 else 'Chinese'}.json", encoding="utf-8") as f:
    data = json.load(f)

if not os.path.exists("data/response"):
    os.makedirs("data/response")

with open(f"data/response/Wired Network {'English' if en == 1 else 'Chinese'} by {model} "
          f"{'few' if shot == 3 else 'zero'}{'_naive' if cot == 0 and noq == 1 else ''}{'_cot' if cot == 1 else ''}"
          f"{'_self_con' if noq > 1 else ''}.json", "a", encoding="utf-8") as f:
    f.write("[\n")
    for index, item in tqdm(enumerate(data), total=len(data)):
        question = item["question"] + "\n" + "\n".join([
            chr(ord("@") + i + 1) + ". " + x for i, x in enumerate(item["choices"])])

        response = []
        for n in range(noq):
            while True:
                try:
                    def flatten(ll):
                        return [x for xs in ll for x in xs]
                    
                    if structure == "json":
                        struct_en = " return as JSON with structure {\"answer\":\"A,B,C\"}"
                        struct_zh = "，以JSON格式返回{\"answer\":\"A,B,C\"}"
                        suffix = "_json"
                    else:
                        struct_en = ""
                        struct_zh = ""
                        suffix = ""

                    chat_completion = client.chat.completions.create(
                        messages = [
                            {
                                "role": "system",
                                "content": "Given a choice question. \"{question}\" "
                                    f"Give the answer{struct_en}. Letters only, separated by comma (A, B, C, etc.), "
                                    "without answer contents or explanations."
                                    if en == 1 else
                                    "这是一个选择题。\"{question}\" "
                                    f"给出答案{struct_zh}，仅包含逗号分隔的字母，不包含答案内容或其他解释。",
                            },
                            *flatten([
                            {
                                "role": "user",
                                "content": prompt.network.en.question[i]["content"]
                                    if en == 1 else
                                    prompt.network.zh.question[i]["content"],
                            },
                            {
                                "role": "assistant",
                                "content": prompt.network.en.question[i]["answer"+suffix]
                                    if en == 1 else
                                    prompt.network.zh.question[i]["answer"+suffix],
                            }
                            ] for i in range(shot)),
                            {
                                "role": "user",
                                "content": question,
                            }
                        ] if cot == 0 else [
                            {
                                "role": "system",
                                "content": "Given a choice question. \"{question}\" Think step by step."
                                    "Analyze each choice in a section begin with `Analyzing each choice:`. "
                                    "Finally give the answer in a section begin with `So the answer is `"
                                    f"{struct_en}. Expecting letters only, separated by comma (A, B, C, etc.), "
                                    "without answer contents or explanations."
                                    if en == 1 else
                                    "这是一个选择题。\"{question}\" 展示推理过程。"
                                    "在一个段落中分析每个选项，以`分析每个选项：`开头。"
                                    f"最终在一个段落中给出答案，以`所以答案是`开头{struct_zh}，"
                                    "仅包含逗号分隔的字母，不包含答案内容或其他解释。",
                            },
                            *flatten([
                            {
                                "role": "user",
                                "content": prompt.network.en.question[i]["content"]
                                    if en == 1 else
                                    prompt.network.zh.question[i]["content"],
                            },
                            {
                                "role": "assistant",
                                "content": prompt.network.en.question[i]["analysis"]
                                        + prompt.network.en.question[i]["conclusion"+suffix]
                                    if en == 1 else
                                    prompt.network.zh.question[i]["analysis"]
                                        + prompt.network.zh.question[i]["conclusion"+suffix],
                            }
                            ] for i in range(shot)),
                            {
                                "role": "user",
                                "content": question,
                            }
                        ],
                        model = model,
                    ) if shot == 3 else client.chat.completions.create(
                        messages = [
                            {
                                "role": "user",
                                "content": f"Here is a choice question. \"{question}\" "
                                    f"Give the answer{struct_en}. Letters only, separated by comma (A, B, C, etc.), "
                                    "without answer contents or explanations."
                                    if en == 1 else
                                    f"这是一个选择题。\"{question}\" "
                                    f"给出答案{struct_zh}，仅包含逗号分隔的字母，不包含答案内容或其他解释。",
                            }
                        ] if cot == 0 else [
                            {
                                "role": "user",
                                "content": f"Here is a choice question. \"{question}\" Think step by step."
                                    f"Give the answer{struct_en}. Letters only, separated by comma (A, B, C, etc.), "
                                    "without answer contents or explanations."
                                    if en == 1 else
                                    f"这是一个选择题。\"{question}\" 展示推理过程。"
                                    f"给出答案{struct_zh}，仅包含逗号分隔的字母，不包含答案内容或其他解释。",
                            }
                        ],
                        model = model,
                    )
                    content = chat_completion.choices[0].message.content
                    if shot == 0 and cot == 1:
                        chat_completion = client.chat.completions.create(
                            messages = [
                                {
                                    "role": "user",
                                    "content": f"Here is a choice question. \"{question}\" Think step by step."
                                        if en == 1 else f"这是一个选择题。\"{question}\" 展示推理过程。",
                                },
                                {
                                    "role": "assistant",
                                    "content": content,
                                },
                                {
                                    "role": "user",
                                    "content": "So what is the answer?."
                                        f"(Give the answer{struct_en}. Letters only, separated by comma A, B, C, etc., "
                                        "without answer contents or explanations.)"
                                        if en == 1 else
                                        "所以答案是什么？"
                                        f"（给出答案{struct_zh}，仅包含逗号分隔的字母，不包含答案内容或其他解释。）",
                                }
                            ],
                            model = model,
                        )
                        content = chat_completion.choices[0].message.content
                    response.append(content)
                except Exception as e:
                    print(e)
                    continue
                break
        result = {"id": item["id"], "response": response}

        f.write(f"\t{json.dumps(result, ensure_ascii=False)}{',' if index != len(data) - 1 else ''}\n")
        f.flush()
    f.seek(f.tell() - 2, os.SEEK_SET)
    f.truncate()
    f.write("\n]\n")
