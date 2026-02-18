import json
import re
from thefuzz import fuzz
from rouge import Rouge
import jieba
import logging
import sys
import os


def split_sentences(text, lang):
    if lang.endswith("-zh-gen"):
        # 使用"。！？"进行句子分割
        sentences = re.findall(r'[^。！？]+[。！？]?', str(text))
        seg_sentences = []
        for sentence in sentences:
            seg_list = ' '.join(jieba.cut(sentence))
            seg_sentences.append(seg_list)
        sentences = seg_sentences
    elif lang.endswith("-en-gen"):
        # 使用".!?"进行句子分割
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", text)

    # 去除空句子
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def calculate_score(num_sentences):
    return 1.0 / num_sentences

def calculate_sentence_similarity(test_sentence, generated_sentences, threshold,score):
    rouge = Rouge()
    similarities = []
    for generated_sentence in generated_sentences:
        scores = rouge.get_scores(test_sentence, generated_sentence)
        #similarity = fuzz.partial_ratio(test_sentence, generated_sentence)
        similarity = scores[0]['rouge-l']['f']
        # if similarity >= threshold:
        #     return score
        similarities.append(similarity)
    logging.info(f"Value: {test_sentence} | Similarity Scores: {similarities}")
    if similarities:
        max_similarity = max(similarities)
        return max_similarity
    else:
        return 0


def calculate_sentence_scores(test_data, generated_data, threshold, start_id=None, end_id=None):
    sentence_scores = {}

    from tqdm import tqdm
    for id_, test_data in tqdm(test_data.items(),desc = 'Processing'):
        if start_id is not None and id_ < start_id:
            continue
        if end_id is not None and id_ > end_id:
            break
        generated_text = generated_data.get(str(id_))
        if generated_text:
            task = test_data.get("task")
            test_text = test_data.get("text")
            test_sentences = split_sentences(test_text, task)
            generated_sentences = split_sentences(generated_text, task)
            score = calculate_score(len(test_sentences))
            for test_sentence in test_sentences:
                sentence_score = calculate_sentence_similarity(test_sentence, generated_sentences, threshold, score)
                sentence_scores.setdefault(id_, []).append((test_sentence, sentence_score))
    return sentence_scores

def calculate_total_score(sentence_scores):
    total_score = 0
    id_scores_avg = []
    for id_, score_list in sentence_scores.items():
        id_score = 0
        print(f"Scores for ID {id_}:")
        for test_sentence, score in score_list:
            print(f"Sentence: {test_sentence} (Score: {score})")
            id_score += score
            # total_score += score
        id_score_avg = id_score / len(score_list) if score_list else 0
        id_scores_avg.append(id_score_avg)
        print(f"Average Score for ID {id_}: {id_score_avg}")
        # print(f"Total Score for ID {id_}: {id_score}")
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
log_str = "log/rougel_scores-zh-gen.log"

# 拼接新路径
log_dir = os.path.join(directory_path, log_str)


logging.basicConfig(filename=log_dir, level=logging.INFO, format='%(asctime)s - %(message)s')

test_data = {}
generated_data = {}

with open(test_jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        id_ = data.get("id")
        output = data.get("output")
        task = data.get("task")
        if id_ and output and (task.endswith("-zh-gen")):
            test_data[id_] = {
                "text": output,
                "task": task
            }

with open(generated_jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        id_ = data.get("id")
        output = data.get("output")
        if id_ and output:
            generated_data[str(id_)] = output



threshold = 0.2  # 相似度的阈值
start_id = 301  # 开始ID范围（可选）
end_id = 600  # 结束ID范围（可选）
sentence_scores = calculate_sentence_scores(test_data, generated_data, threshold, start_id, end_id)

total_score = calculate_total_score(sentence_scores)

# score = total_score / (end_id - start_id + 1) * 100
print(f"Total Score: {total_score}")
# print(f"Score: {score}")
with open("./result-rouge.txt", "a") as f1:
    f1.write(f"{str(generated_jsonl_file)}: Total Score from ID {start_id} to {end_id}: {total_score}\n")
