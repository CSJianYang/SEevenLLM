# SEevenLLM


## Introduce

We introduce SEVENLLM, a comprehensive framework developed to enhance the understanding and task execution capabilities of Large Language Models (LLMs) in the analysis of cybersecurity events. SEVENLLM not only improves the understanding and operational task execution of LLMs within this domain but also proposes a set of evaluation methods tailored for these purposes. The various experiments conducted under this framework offer valuable references for your work in this area.

You can learn more about our work in [SEvenLLM: Benchmarking, Eliciting, and Enhancing Abilities of Large Language Models in Cyber Threat Intelligence](https://arxiv.org/abs/2405.0344).

## Dataset

We provide two datasets, **SEVENLLM-Instruct** and **SEVENLLM-Bench**, specifically designed for training and evaluating the capabilities of models. These datasets utilize the **Select-Instruct** method and have been vetted by experts in the relevant fields. 
![image](https://github.com/CSJianYang/SEevenLLM/assets/112760217/1c8f1a65-f030-47c7-aab4-0cd731ee0581)


Our main data generation process is shown in the figure above. You can access detailed information and download them through [this link](https://huggingface.co/datasets/Multilingual-Multimodal-NLP/SEVENLLM-Dataset).

## Start

### Reproduction

You can replicate our work as following. Replace the model base and dataset paths with your own file paths.

```bash
sh scripts/llama_train.sh

sh infer.sh
```


### Evaluation

We have employed five different methods to comprehensively evaluate the capabilities of the model: **GPT-4 Score**,**Rouge-L Score**,**Semantic Score**, multiple-choice assessment, and human expert evaluation. You can refer to our code at [this link](XXX).







