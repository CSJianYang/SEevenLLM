#!/bin/bash

# 创建一个临时文件来存储并行任务
tempfile=$(mktemp)

# 指定目标文件夹名和文件名
folder_name="./result-sample"
#file_name="your_file_name"
# 最大并行进程数
max_jobs=16

# 创建一个信号量文件描述符
mkfifo /tmp/$$.fifo
exec 9<> /tmp/$$.fifo
rm /tmp/$$.fifo

# 初始化信号量
for ((i=0; i<max_jobs; i++)); do
    echo >&9
done
# 关联数组存储Python脚本和对应的日志文件名
declare -A script_log_mapping=(
    ["ex-score-sbert-en-path.py"]="debug_ex_en_sbert"
    ["ex-score-sbert-path.py"]="debug_ex_zh_sbert"
    ["gen_score_sbert-path.py"]="debug_gen_zh_sbert"
    ["gen_score_sbert-en-path.py"]="debug_gen_en_sbert"
)

# 遍历文件夹下的文件
find "$folder_name" -type f -name "test_result_*.jsonl" | while read -r file; do
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
        # 执行Python脚本并将结果写入日志文件，使用并行处理
        
        for script_name in "${!script_log_mapping[@]}"; do
            log_file="${script_log_mapping[$script_name]}-${extracted_part}.log"
            # 读取信号量以限制并行进程数
            read -u 9
            {
                python "$script_name" "$file" > "$target_directory/$log_file" 
                # 完成后释放信号量
                echo >&9
            } &
        done

        # 等待所有后台任务完成
        # wait
    fi
done

wait

# 关闭信号量文件描述符
exec 9>&-