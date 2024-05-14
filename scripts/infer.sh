export MASTER_ADDR=localhost
export MASTER_PORT=2131
export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"

MODEL_DIR='./ckpt/qwen1.5-7b/'
OUT_DIR='./ckpt/qwen1.5-7b/'

torchrun --nproc_per_node 4 --master_port 7834 infer.py \
                        --base_model $MODEL_DIR \
                        --data_path "./data/test_all.jsonl" \
                        --out_path $OUT_DIR \
                        --batch_size 2