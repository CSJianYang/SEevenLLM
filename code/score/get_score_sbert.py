import json
import re
from thefuzz import fuzz
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


def split_sentences(text, lang):
    if lang.endswith("-zh-gen"):
        # use "。！? split sentences
        sentences = re.findall(r'[^。！？]+[。！？]?', str(text))
    elif lang.endswith("-en-gen"):
        # use ".!?" split sentences
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", text)

 
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences

def calculate_score(num_sentences):
    return 1.0 / num_sentences

def calculate_sentence_similarity(test_sentence, generated_sentences, threshold,score):
    sentences1 = []
    sentences1.append(test_sentence)
    model = SentenceTransformer('./paraphrase-multilingual-MiniLM-L12-v2')
    embeddings1 = model.encode(sentences1)
    for generated_sentence in generated_sentences:
        sentences2 = []
        sentences2.append(generated_sentence)
        embeddings2 = model.encode(sentences2)
        cosine_scores = cos_sim(embeddings1, embeddings2)
        similarity = cosine_scores.item()

        if similarity >= threshold:
            return score
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

# example
test_jsonl_file = './data/test.jsonl'
generated_jsonl_file = './SevenLLM-result/test-result-llama2-7b.jsonl'

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

threshold = 0.6  # threshold
start_id = 1  # strat id
end_id = 1200  # end id
sentence_scores = calculate_sentence_scores(test_data, generated_data, threshold, start_id, end_id)

total_score = calculate_total_score(sentence_scores)
score = total_score / 3 
print(f"Total Score: {total_score}")
print(f"Score: {score}")