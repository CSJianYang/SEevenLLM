#!/bin/bash



# 指定目标文件夹名和文件名
folder_name="./result"
#file_name="your_file_name"

# 关联数组存储Python脚本和对应的日志文件名
declare -A script_log_mapping=(
    ["ex-score-en-path.py"]="debug_ex_en_rougeL"
    ["ex-score-path.py"]="debug_ex_zh_rougeL"
    ["gen_score_rougeL-path.py"]="debug_gen_zh_rougeL"
    ["gen_score_rougeL-en-path.py"]="debug_gen_en_rougeL"
    ["choice_sorce-path.py"]="debug_choice"
)

# 遍历文件夹下的文件
find "$folder_name" -type f -name "test-result-*.jsonl" | while read -r file; do
    if [ -f "$file" ]; then

        filename=$(basename "$file")

        # 从文件名中提取XXX数字部分
        # number=$(echo "$file" | sed 's/.*test_result_\([0-9]\{3,5\}\)\.jsonl/\1/')
        extracted_part=$(echo "$filename" | sed 's/test_result_\(.*\)\.jsonl/\1/')


        # 提取文件所在的目录路径
        directory_path=$(dirname "$file")
        echo "Directory Path: $directory_path"
        echo "Extracted Part: $extracted_part"
        # 创建目标目录（如果不存在）
        target_directory="$directory_path/score"
        mkdir -p "$target_directory"
        log_directory="$directory_path/log"
        mkdir -p "$log_directory"
        # 执行Python脚本并将结果写入日志文件
        for script_name in "${!script_log_mapping[@]}"; do
            log_file="${script_log_mapping[$script_name]}-${extracted_part}.log"
            python $script_name "$file" > "$target_directory/$log_file"
            # (python "$script_name" "$file" > "$target_directory/$log_file") &
        done
    fi
done
