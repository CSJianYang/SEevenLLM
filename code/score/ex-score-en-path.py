import json
from difflib import SequenceMatcher
from thefuzz import fuzz
from rouge import Rouge
import jieba
import logging
import sys
import os
from collections import Counter

def intersection_count(list1, list2):
    # 使用Counter来计算每个列表中元素的出现次数
    count1 = Counter(list1)
    count2 = Counter(list2)
    
    # 计算两个列表交集中元素的数量
    return sum(min(count1[item], count2[item]) for item in set(list1) & set(list2))


def extract_values_from_json(json_data):
    values = []

    def extract_values_recursive(data):
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, (dict, list)):
                    extract_values_recursive(value)
                else:
                    values.append(str(value))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    extract_values_recursive(item)
                else:
                    values.append(str(item))

    extract_values_recursive(json_data)
    return values


def calculate_score(num_values):
    return 1.0 / num_values



def extract_output_values(jsonl_file):
    output_values = {}

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)

            if data.get("task", "").endswith("-en-ex"):
                output = data.get("output")
                #print(output)
                if output:
                    if isinstance(output, (dict, list)):
                        values = extract_values_from_json(output)
                        id_ = data.get("id")
                        if id_:
                            if id_ in output_values:
                                output_values[id_].extend(values)
                            else:
                                output_values[id_] = values
                    else:
                        id_ = data.get("id")
                        #print("id" + str(id_))
                        values = output
                        if id_:
                            if id_ in output_values:
                                output_values[id_].extend(values)
                            else:
                                output_values[id_] = values
                else:
                    id_ = data.get("id")
                    #print("id" + str(id_))
                    values = ""
                    if id_:
                        if id_ in output_values:
                            output_values[id_].extend(values)
                        else:
                            output_values[id_] = values
    return output_values



def calculate_accuracy_score(test_data, generated_data, threshold):
    accuracy_scores = {}

    from tqdm import tqdm
    for id_, test_values in tqdm(test_data.items(),desc = 'Processing'):
        #print(test_data)
        score_list = []
        generated_values = generated_data.get(id_)
        if isinstance(test_values, (list)):
            Sgt = len(test_values)
            test_list = test_values
        elif isinstance(test_values, (str)):
            Sgt = 1
            test_list = [test_values]
        else:
            Sgt = 0
            test_list = []
        if isinstance(generated_values, (list)):
            Spd = len(generated_values)
            gene_list = generated_values
        elif isinstance(generated_values, (str)):
            Spd = 1
            gene_list = [generated_values]
        else:
            Spd = 0
            gene_list = []
        precision = intersection_count(test_list, gene_list) / Spd if Spd else 0
        recall = intersection_count(test_list, gene_list) / Sgt if Sgt else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
        logging.info(f"Value: {test_list} | Similarity Scores: {f1_score}")
        score_list.append(([test_list, gene_list], f1_score, "score-test"))
        accuracy_scores[id_] = score_list
    return accuracy_scores


def calculate_total_score(accuracy_scores, start_id, end_id):
    total_score = 0
    id_scores_avg = []
    for id_, score_list in accuracy_scores.items():
        if start_id <= id_ <= end_id:
            id_score = 0
            print(f"Scores for ID {id_}:")
            for test_value, score, match_type in score_list:
                print(f"{match_type}: {test_value} (Score: {score})")
                id_score += score
                total_score += score
            
            id_score_avg = id_score / len(score_list) if score_list else 0
            id_scores_avg.append(id_score_avg)
            print(f"Average Score for ID {id_}: {id_score_avg}")
            

    total_score_avg = sum(id_scores_avg) / len(id_scores_avg) if id_scores_avg else 0
    return total_score_avg


# 使用示例

test_jsonl_file = r"./test_all.jsonl"
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_file>")
    sys.exit(1)

generated_jsonl_file = sys.argv[1]

# 获取目录路径
directory_path = generated_jsonl_file.rsplit('/', 1)[0]

# 新的路径部分
log_str = "log/rougel_scores-en-ex.log"

# 拼接新路径
log_dir = os.path.join(directory_path, log_str)


logging.basicConfig(filename=log_dir, level=logging.INFO, format='%(asctime)s - %(message)s')


test_data = extract_output_values(test_jsonl_file)
generated_data = extract_output_values(generated_jsonl_file)

threshold = 60  # 相似匹配的阈值
accuracy_scores = calculate_accuracy_score(test_data, generated_data, threshold)

start_id = 601
end_id = 900
total_score = calculate_total_score(accuracy_scores, start_id, end_id)
# score = total_score / (end_id - start_id + 1) * 100
print(f"Total Score from ID {start_id} to {end_id}: {total_score}")
# print(f"Score from ID {start_id} to {end_id}: {score}")
with open("./result-f1.txt", "a") as f1:
    f1.write(f"{str(generated_jsonl_file)}: Total Score from ID {start_id} to {end_id}: {total_score}\n")