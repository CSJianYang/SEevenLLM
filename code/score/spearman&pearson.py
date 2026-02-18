import os
import json
import pandas as pd
from scipy.stats import spearmanr, pearsonr

gpt_f1 = r".\sevenllm-qwen1.5-7b\test_en_qwen_sco.jsonl"
gpt_f2 = r".\sevenllm-qwen1.5-7b\test_qwen_zh_sco.jsonl"
# gpt_f = r"D:\school-works\2024.03-2024.06\航远师兄的工作\sample_0611\评分相似性2(1)\qwen1.5-7b-chat\qwen_7b_gpt.jsonl"
gpt_dic = dict()
gpt_gen = list()
gpt_ex = list()
human_file = r".\sevenllm-qwen1.5-7b\human_sevenllm-qwen-1_5-7b-change.jsonl"
human_dic = dict()
human_gen = list()
human_ex = list()


with open(human_file, 'r', encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        obj = json.loads(line)
        sentence = obj["result"][obj["result"].find("\"score\": \"") + len("\"score\": \""):]
        score = int(sentence[:sentence.find(",")].replace("\"", "").replace(" ", ""))
        human_dic.setdefault(int(obj["id"]), score)


with open(gpt_f1, 'r', encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        obj = json.loads(line)
        s_pos = obj["result"].find("\"score\": \"") + len("\"score\": \"")
        sentence = obj["result"][s_pos:]
        score = int(sentence[:sentence.find(",") - 1].replace("\"", "").replace(" ", ""))
        gpt_dic.setdefault(int(obj["id"]), score)


with open(gpt_f2, 'r', encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        obj = json.loads(line)
        s_pos = obj["result"].find("\"score\": \"") + len("\"score\": \"")
        sentence = obj["result"][s_pos:]
        score = int(sentence[:sentence.find(",") - 1].replace("\"", "").replace(" ", ""))
        gpt_dic.setdefault(int(obj["id"]), score)


gpt_list = sorted(gpt_dic.items(), key=lambda x: x[0], reverse=False)
gpt_dic = {x[0]: x[1] for x in gpt_list}
print(gpt_dic)

for i in range(1, 1201):
    if 901 <= i <= 1200 or 301 <= i <= 600:
        human_gen.append(human_dic[i])
        gpt_gen.append(gpt_dic[i])
    else:
        human_ex.append(human_dic[i])
        gpt_ex.append(gpt_dic[i])


df_ex = pd.DataFrame({"ex1": human_ex, "ex2": gpt_ex})
df_gen = pd.DataFrame({"gen1": human_gen, "gen2": gpt_gen})
df_all = pd.DataFrame({"all1": human_gen + human_ex, "all2": gpt_gen + gpt_ex})

print("ex：")
spearman_corr, spearman_p = spearmanr(df_ex["ex1"], df_ex["ex2"])
print(f"spearman Correlation:{spearman_corr},p-value: {spearman_p}")

pearson_corr,pearson_p=pearsonr(df_ex["ex1"], df_ex["ex2"])
print(f"Pearson correlation:{pearson_corr},p-value: {pearson_p}")

print()
print("gen：")
spearman_corr, spearman_p = spearmanr(df_gen["gen1"], df_gen["gen2"])
print(f"spearman Correlation:{spearman_corr},p-value: {spearman_p}")

pearson_corr,pearson_p = pearsonr(df_gen["gen1"], df_gen["gen2"])
print(f"Pearson correlation:{pearson_corr},p-value: {pearson_p}")

print()
print("all：")
spearman_corr, spearman_p = spearmanr(df_all["all1"], df_all["all2"])
print(f"spearman Correlation:{spearman_corr},p-value: {spearman_p}")

pearson_corr,pearson_p = pearsonr(df_all["all1"], df_all["all2"])
print(f"Pearson correlation:{pearson_corr},p-value: {pearson_p}")





