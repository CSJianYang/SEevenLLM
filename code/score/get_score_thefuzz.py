import json
from difflib import SequenceMatcher
from thefuzz import fuzz

def extract_values_from_json(json_data):
    values = []

    def extract_values_recursive(data):
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, (dict, list)):
                    extract_values_recursive(value)
                else:
                    values.append(value)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    extract_values_recursive(item)
                else:
                    values.append(item)

    extract_values_recursive(json_data)
    return values


def calculate_score(num_values):
    return 1.0 / num_values


def calculate_similarity_score(value, test_values, threshold,score):
    for test_value in test_values:
        similarity = fuzz.partial_ratio(value, str(test_value))
        #similarity = fuzz.ratio(value, str(test_value))
        if similarity >= threshold:
            return score
    return 0
def calculate_similarity_score_str(value, test_values, threshold,score):
    similarity = fuzz.partial_ratio(value, str(test_values))
    #similarity = fuzz.ratio(value, str(test_values))
    if similarity >= threshold:
        return score
    return 0

def extract_output_values(jsonl_file):
    output_values = {}

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)

            if data.get("task", "").endswith("-ex"):
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
                    values = "NULL"
                    if id_:
                        if id_ in output_values:
                            output_values[id_].extend(values)
                        else:
                            output_values[id_] = values
    return output_values


def calculate_accuracy_score(test_data, generated_data, threshold):
    accuracy_scores = {}

    for id_, test_values in test_data.items():
        #print(test_data)
        generated_values = generated_data.get(id_)
        if generated_values:
            #print(generated_values)
            score_list = []
            #print(type(test_values))
            if isinstance(test_values, (dict, list)):
                for test_value in test_values:
                    test_value = str(test_value)
                    score = calculate_score(len(test_values))
                    if len(test_value) > 1:
                        similarity_score = calculate_similarity_score(test_value, generated_values, threshold,score)
                        if similarity_score > 0:
                            score_list.append((test_value, similarity_score, "Similar Match"))
                        else:
                            score_list.append((test_value, 0, "Miss Similar Match"))
                    elif test_value in generated_values:
                        score_list.append((test_value, score, "Exact Match"))
                    else:
                        score_list.append((test_value, 0, "Miss Match"))
            else:
                #print(test_values)
                score = 1
                if len(test_values) > 1:
                        similarity_score = calculate_similarity_score_str(test_values, generated_values, threshold,score)
                        if similarity_score > 0:
                            score_list.append((test_values, similarity_score, "Similar Match"))
                        else:
                            score_list.append((test_value, 0, "Miss Similar Match"))
                elif test_value in generated_values:
                    score_list.append((test_values, score, "Exact Match"))
                else:
                    score_list.append((test_value, 0, "Miss Match"))
            if score_list:
                accuracy_scores[id_] = score_list

    return accuracy_scores


def calculate_total_score(accuracy_scores, start_id, end_id):
    total_score = 0

    for id_, score_list in accuracy_scores.items():
        if start_id <= id_ <= end_id:
            id_score = 0
            print(f"Scores for ID {id_}:")
            for test_value, score, match_type in score_list:
                print(f"{match_type}: {test_value} (Score: {score})")
                id_score += score
                total_score += score
            print(f"Total Score for ID {id_}: {id_score}")

    return total_score


# example
test_jsonl_file = './data/test.jsonl'
generated_jsonl_file = './SevenLLM-result/llama/test-result-llama2-7b.jsonl'

test_data = extract_output_values(test_jsonl_file)
generated_data = extract_output_values(generated_jsonl_file)

threshold = 60  # threshold
accuracy_scores = calculate_accuracy_score(test_data, generated_data, threshold)

start_id = 1
end_id = 300
total_score = calculate_total_score(accuracy_scores, start_id, end_id)

print(f"Total Score from ID {start_id} to {end_id}: {total_score}")
