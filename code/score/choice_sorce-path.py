import json
import sys
import os
def extract_output_values(jsonl_file):
    output_values = {}

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except json.decoder.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}. 错误行: {line}")
                continue

            if data.get("task", "").endswith("choice"):
                output = data.get("output")
                id_ = data.get("id")
                if id_:
                    if id_ in output_values:
                        output_values[id_].append(output)
                    else:
                        output_values[id_] = [output]

    return output_values

def process_generated_output(generated_output_values):
    processed_output_values = {}
    problematic_outputs = []

    for id_, outputs in generated_output_values.items():
        for output in outputs:
            if len(str(output)) > 1:
                problematic_outputs.append({"id": id_, "output": output})
                # 统计字符串中包含的选项
                valid_chars = [char for char in str(output) if char in ["A", "B", "C", "D"]]
                if len(valid_chars) == 1:  # 如果字符串中仅包含一个选项
                    processed_output_values[id_] = valid_chars[0]  # 匹配该选项
                else:
                    problematic_outputs.append({"id": id_, "output": output})
                    print(f"无法匹配结果：id={id_}, output={outputs[0]}")
            else:
                if any(char in ["A", "B", "C", "D"] for char in str(output)):
                    processed_output_values[id_] = output
                else:
                    print(f"无法匹配结果：id={id_}, output={outputs[0]}")
                    problematic_outputs.append({"id": id_, "output": output})

    return processed_output_values, problematic_outputs

def calculate_total_score(accuracy_scores, start_id, end_id):
    total_score = 0

    for id_, score_list in accuracy_scores.items():
        if start_id <= id_ <= end_id:
            id_score = 0
            #print(f"Scores for ID {id_}:")
            for test_value, score, match_type in score_list:
                #print(f"{match_type}: {test_value} (Score: {score})")
                id_score += score
                total_score += score
            #print(f"Total Score for ID {id_}: {id_score}")

    return total_score

# 示例测试数据集和生成数据集文件路径
test_dataset_file = "./test_all.jsonl"
if len(sys.argv) < 2:
    print("Usage: python script.py <path_to_file>")
    sys.exit(1)

generated_jsonl_file = sys.argv[1]
# 提取测试数据集和生成数据集中的输出值
test_output_values = extract_output_values(test_dataset_file)
generated_output_values = extract_output_values(generated_jsonl_file)

# 对生成数据集中的输出值进行处理
processed_generated_output_values, problematic_outputs = process_generated_output(generated_output_values)

# 初始化总分
total_score = 0
accuracy_scores = {}  # 收集得分信息

# 检查相同"id"属性的样本的一致性得分
for id_, test_outputs in test_output_values.items():
    if id_ in processed_generated_output_values:
        generated_output = processed_generated_output_values[id_]
        # 检查结果是否一致
        if test_outputs[0] == generated_output:
            total_score += 1
            # 保存得分信息
            accuracy_scores[id_] = [(test_outputs[0], 1, "Exact Match")]

# 输出总分
print("总分：", total_score)
# 提取路径部分
path = os.path.dirname(generated_jsonl_file)

# 构建新的文件路径
problematic_outputs_file = os.path.join(path, "problematic_outputs.jsonl")
# 输出问题数据集中的输出
if len(problematic_outputs) >= 1:
    with open(problematic_outputs_file, "a+", encoding="utf-8") as f:
        for output in problematic_outputs:
            f.write(json.dumps(output, ensure_ascii=False) + "\n")

# 计算特定范围内的得分
start_id = 1201
end_id = 1300
total_score_range = calculate_total_score(accuracy_scores, start_id, end_id)
print(f"Total Score for IDs {start_id} to {end_id} : {total_score_range}")


# 计算特定范围内的得分
start_id = 1201
end_id = 1225
total_score_range = calculate_total_score(accuracy_scores, start_id, end_id)
print(f"Total Score for IDs {start_id} to {end_id} (en-gen): {total_score_range}")

# 计算特定范围内的得分
start_id = 1226
end_id = 1250
total_score_range = calculate_total_score(accuracy_scores, start_id, end_id)
print(f"Total Score for IDs {start_id} to {end_id} (en-ex): {total_score_range}")


# 计算特定范围内的得分
start_id = 1251
end_id = 1275
total_score_range = calculate_total_score(accuracy_scores, start_id, end_id)
print(f"Total Score for IDs {start_id} to {end_id} (zh-ex): {total_score_range}")

# 计算特定范围内的得分
start_id = 1276
end_id = 1300
total_score_range = calculate_total_score(accuracy_scores, start_id, end_id)
print(f"Total Score for IDs {start_id} to {end_id} (zh-gen): {total_score_range}")