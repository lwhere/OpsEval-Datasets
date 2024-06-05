import os
import json

def all_upper(l):
    for x in l:
        if not x.isupper() or not x.isascii():
            return False
    return True

def trim(s):
    f = 0
    s = s.replace("and", ",")
    b = 0
    for i in range(len(s)):
        if s[i].isupper():
            b = i
            f = 1
            break
    e = len(s)
    for i in range(b+1, len(s)):
        if not s[i].isascii() or not s[i].isalpha() and s[i] != " " and s[i] != ",":
            e = i
            break
    return s[b:e] if f == 1 else ""

def extract(s):
    for i, c in enumerate(s):
        if not c.isalpha() and c != " " and c != ",":
            return list(filter(None, [trim(x) for x in [x.strip() for x in s[:i].split(",")]]))
    return list(filter(None, [trim(x) for x in [x.strip() for x in s.split(",")]]))

def format_sc(l):
    return list(filter(all_upper, [extract(trim(x)) for x in l]))

def format_cot(l):
    def find(s):
        t = s.split("\n")
        i = t[-1].lower().rfind("answer")
        if i != -1:
            return t[-1][i+1:]
        i = t[0].lower().find("answer")
        if i != -1:
            return t[0][i+1:]
        for x in t[::-1]:
            i = x.lower().rfind("answer is")
            if i != -1:
                return x[i+1:]
            i = x.lower().rfind("answers are")
            if i != -1:
                return x[i+1:]
        t[0] = trim(t[0])
        if t[0][0].isupper() and (len(t[0]) == 1 or t[0][1] == "."):
            return t[0][0]
        return ""
    return list(filter(all_upper, [extract(trim(find(x))) for x in l]))

def format_cot_cn(l):
    def find(s):
        t = s.split("\n")
        i = t[-1].lower().rfind("答案")
        if i != -1:
            return t[-1][i+1:]
        i = t[0].lower().find("答案")
        if i != -1:
            return t[0][i+1:]
        return ""
    return list(filter(all_upper, [extract(trim(find(x))) for x in l]))

def most_common(l):
    if not l:
        return []
    o = [l.count(x) for x in l]
    m = 0
    for i in range(len(o)):
        if o[i] > o[m]:
            m = i
    return l[m]

if __name__ == "__main__":
    en = 0
    cot = 1
    noq = 1
    model = "gemma-7b-it"

    with open(f"data/test/Wired Network {'English' if en == 1 else 'Chinese'}.json", encoding="utf-8") as f:
        data = json.load(f)

    ss = f"few{'_naive' if cot == 0 and noq == 1 else ''}{'_cot' if cot == 1 else ''}" \
        f"{'_self_con' if noq > 1 else ''}"
    filename = f"Wired Network {'English' if en == 1 else 'Chinese'} by {model} {ss}.json"

    with open(f"data/response/{filename}", encoding="utf-8") as f:
        response = json.load(f)

    data_map = {item["id"]: set([x.strip() for x in item["answer"].split(",")]) for item in data}

    result = []
    response_map = {}
    format = format_sc if cot == 0 else (format_cot if en == 1 else format_cot_cn)
    for item in response:
        ans = most_common(format(item["response"]))
        response_map.update({item["id"]: set(ans)})
        result.append(dict(item, **{"response": ans}))

    # print(dict(list(result_map.items())[180:200]))

    n = 0
    for k, v in data_map.items():
        if v == response_map.get(k, set()):
            n += 1
    print(f"{ss}={n}/{len(data)}={n/len(data)}")

    if not os.path.exists("data/format"):
        os.makedirs("data/format")

    with open(f"data/format/{filename}", "w", encoding="utf-8") as f:
        f.write("[\n")
        for i, x in enumerate(result):
            f.write(f"\t{json.dumps(x, ensure_ascii=False)}{',' if i != len(result) - 1 else ''}\n")
        f.seek(f.tell() - 2, os.SEEK_SET)
        f.truncate()
        f.write("\n]\n")
