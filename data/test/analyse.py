import json
import re

file_name = "Wired Network.json"

with open(file_name) as f:
    data = json.load(f)
question_answer = []
multi_choice = []
for item in data:
    if 'solution' in item:
        multi_choice.append(item)
    else:
        question_answer.append(item)
print(len(data))
print(f"{len(question_answer)} question_answer")
print(f"{len(multi_choice)} multi_choice")
# 初始化计数变量
single_choice = 0
two_choice = 0
three_choice = 0
four_choice = 0
single_choice_data = []
three_choice_data = []
four_choice_data = []
other_choice_data = []



# 遍历 JSON 数据
for item in data:
    answer = item['answer']

    # 使用正则表达式检查选项数量
    if re.match(r'^[A-F]{1}$', ''.join(answer)):
        single_choice += 1
        single_choice_data.append(item)
    elif re.match(r'^[A-F](,?[A-F]){1}$', ''.join(answer)):
        two_choice += 1
    elif re.match(r'^[A-F](,?[A-F]){2}$', ''.join(answer)):
        three_choice += 1
        three_choice_data.append(item)
    elif re.match(r'^[A-F](,?[A-F]){3}$', ''.join(answer)):
        four_choice += 1
        four_choice_data.append(item)
    else:
        other_choice_data.append(item)

# 输出结果
print(f"单项答案数量: {single_choice}")
print(f"两项答案: {two_choice}")
print(f"三项答案: {three_choice}")
print(f"其他答案的数量: {len(other_choice_data)}")

with open(file_name.split('.j')[0]+"_single_choice_data"+".json", "w", encoding="utf-8") as f:
    json.dump(single_choice_data, f, ensure_ascii=False)

with open(file_name.split('.j')[0]+"_other_choice_data"+".json", "w", encoding="utf-8") as f:
    json.dump(other_choice_data, f, ensure_ascii=False)
