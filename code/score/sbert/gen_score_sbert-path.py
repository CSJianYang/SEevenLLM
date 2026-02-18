import json
import re
from thefuzz import fuzz
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import sys
import logging
import os
model = SentenceTransformer('./paraphrase-multilingual-MiniLM-L12-v2')

# import contextlib
# import os 
# @contextlib.contextmanager
# def suppress_stdout_stderr():
#     with open(os.devnull, 'w') as devnull:
#         old_stdout = sys.stdout
#         old_stderr = sys.stderr
#         try:
#             sys.stdout = devnull
#             sys.stderr = devnull
#             yield
#         finally:
#             sys.stdout = old_stdout
#             sys.stderr = old_stderr
def split_sentences(text, lang):
    if lang.endswith("-zh-gen"):
        # 使用"。！?进行句子分割
        sentences = re.findall(r'[^。！？]+[。！？]?', str(text))
    elif lang.endswith("-en-gen"):
        # 使用".!?"进行句子分割
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", text)

    # 去除空句   
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def calculate_score(num_sentences):
    return 1.0 / num_sentences

def calculate_sentence_similarity(test_sentence, generated_sentences, threshold,score):
    sentences1 = []
    sentences1.append(test_sentence)
    # model = SentenceTransformer('./paraphrase-multilingual-MiniLM-L12-v2')
    embeddings1 = model.encode(sentences1)
    similarities = []

    for generated_sentence in generated_sentences:
        sentences2 = []
        sentences2.append(generated_sentence)
        embeddings2 = model.encode(sentences2)
        cosine_scores = cos_sim(embeddings1, embeddings2)
        similarity = cosine_scores.item()
        similarities.append(similarity)

    #     #similarity = fuzz.partial_ratio(test_sentence, generated_sentence)
    #     if similarity >= threshold:
    #         return score
    # return 0
    logging.info(f"Value: {test_sentence} | Similarity Scores: {similarities}")
    if similarities:
        max_similarity = max(similarities)
        return max_similarity
    else:
        return 0

def calculate_sentence_scores(test_data, generated_data, threshold, start_id=None, end_id=None):
    sentence_scores = {}

    #for id_, test_data in test_data.items():
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
            score = 1
            for test_sentence in test_sentences:
                sentence_score = calculate_sentence_similarity(test_sentence, generated_sentences, threshold,score)
                sentence_scores.setdefault(id_, []).append((test_sentence, sentence_score))
        else:
            # print("The NULL answer is :" + str(id_))
            task = test_data.get("task")
            test_text = test_data.get("text")
            test_sentences = split_sentences(test_text, task)
            for test_sentence in test_sentences:
                sentence_scores.setdefault(id_, []).append((test_sentence, 0))
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
# test_jsonl_file = './test_all-659.jsonl'

test_jsonl_file = './test_all.jsonl'
# generated_jsonl_file = './test-result-llama2-7b-cot.jsonl'
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_file>")
    sys.exit(1)

generated_jsonl_file = sys.argv[1]

# 获取目录路径
directory_path = generated_jsonl_file.rsplit('/', 1)[0]

# 新的路径部分
log_str = "log/sbert_scores-zh-gen.log"

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

threshold = 0.6  # 相似度的阈值
start_id = 301  # 开始ID范围（可选）
end_id = 600  # 结束ID范围（可选）
sentence_scores = calculate_sentence_scores(test_data, generated_data, threshold, start_id, end_id)

total_score = calculate_total_score(sentence_scores)
# score = total_score / 3 
print(f"Total Score: {total_score}")
# print(f"Score: {score}")