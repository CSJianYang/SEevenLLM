import json
import re
from thefuzz import fuzz
from rouge import Rouge
import jieba

def split_sentences(text, lang):
    if lang.endswith("-zh-gen"):
        # use "。！？" split_sentences
        sentences = re.findall(r'[^。！？]+[。！？]?', str(text))
        seg_sentences = []
        for sentence in sentences:
            seg_list = ' '.join(jieba.cut(sentence))
            seg_sentences.append(seg_list)
        sentences = seg_sentences
    elif lang.endswith("-en-gen"):
        # use ".!?" split_sentences
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", text)

    # Remove empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def calculate_score(num_sentences):
    return 1.0 / num_sentences

def calculate_sentence_similarity(test_sentence, generated_sentences, threshold,score):
    rouge = Rouge()
    for generated_sentence in generated_sentences:
        scores = rouge.get_scores(test_sentence, generated_sentence)
        similarity = scores[0]['rouge-l']['f']
        if similarity >= threshold:
            return score
    return 0

def calculate_sentence_scores(test_data, generated_data, threshold, start_id=None, end_id=None):
    sentence_scores = {}

    for id_, test_data in test_data.items():
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
                sentence_score = calculate_sentence_similarity(test_sentence, generated_sentences, threshold,score)
                sentence_scores.setdefault(id_, []).append((test_sentence, sentence_score))

    return sentence_scores

def calculate_total_score(sentence_scores):
    total_score = 0

    for id_, score_list in sentence_scores.items():
        id_score = 0
        print(f"Scores for ID {id_}:")
        for test_sentence, score in score_list:
            print(f"Sentence: {test_sentence} (Score: {score})")
            id_score += score
            total_score += score
        print(f"Total Score for ID {id_}: {id_score}")

    return total_score

# 使用示例
test_jsonl_file = 'test.jsonl'
generated_jsonl_file = 'test_result_qwen7b.jsonl'

test_data = {}
generated_data = {}

with open(test_jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        id_ = data.get("id")
        output = data.get("output")
        task = data.get("task")
        if id_ and output and (task.endswith("-zh-gen") or task.endswith("-en-gen")):
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

threshold = 0.2  # threshold

start_id = 901  # start id
end_id = 1200  # end id
sentence_scores = calculate_sentence_scores(test_data, generated_data, threshold, start_id, end_id)

total_score = calculate_total_score(sentence_scores)

print(f"Total Score: {total_score}")
