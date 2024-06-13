
EVALUATE_PROMPT="""
Please act as an impartial judge and evaluate the quality of the responses provided by two AI assistants to the user question displayed below. 
Your evaluation should consider the accuracy of the content, the conformity to formatting standards, and the consistency of the language used. 
You will be given a reference answer, assistant A’s answer, and assistant B’s answer.
Your job is to evaluate which assistant’s answer is better. Begin your evaluation by comparing both assistants’ answers with the reference answer.
Identify and correct any mistakes. Whether the answer format complies with the requirements of the instructions is also considered.
Avoid any positional biases and ensure that the order in which the responses were presented does not influence your decision.
Do not allow the length of the responses to influence your evaluation.
You can provide your explanation in 'reason'. After providing your explanation, output your final verdict by strictly following this format: [[A]]: assistant A is better, [[B]]: assistant B is better, and [[C]]: Two answers tie. 
[User Question]
Below is an instruction that describes a task, paired with an input that provides further context. 
Write a response that appropriately completes the request.\n
### Instruction:\n{instruction}\n### Input:\n{input}\n
[The Start of Reference Answer]{Referencr_answer}[The End of Reference Answer]
[The Start of Assistant A’s Answer]{Answer_A}[The End of Assistant A’s Answer]
[The Start of Assistant B’s Answer]{Answer_B}[The End of Assistant B’s Answer]

Please note that you are evaluating which answer is better based on the question, not answering the [User Question]. Your answer is '[[A]]',  '[[B]]' or '[[C]]' with json format.
The answer example is :
{{"answer":"[[A]]","reason":""}}
"""
