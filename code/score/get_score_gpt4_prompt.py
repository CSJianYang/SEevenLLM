
# Scores:
# 1: very bad, 2: bad, 3: Neutral (Neither good nor bad), 4: good, 5: very good
EVALUATE_PROMPT="""As a knowledge analysis expert in the field of cybersecurity, please rate the following network security event Q&A results. The focus is on evaluating whether the provided answers align with the questions, whether the content is accurate, readable and valuable, and provide reasons. The required scoring range is from 1 to 5 points.If full marks are not given, optimized results must be given.
The content of the network security incident is: {input}
The question raised regarding the content of this cybersecurity incident is: {instruction}
The answer provided for this event's content and question is：{output}


Scoring method:
Using a 5-point scoring system, 1 point: very poor; 2 points: slightly poor; 3 points: usable; 4 points: good; 5 points: very good
Scoring reference criteria:
* Whether the answer is answered accurately as required by the question, whether the format is regular, and whether the language is coherent and readable.
* Whether the problem belongs to the field of network security incident analysis, whether the description is clear and has certain analytical significance.
* Whether the overall content has information value in the field of network security and whether it is challenging and difficult.

Returns a json format result, the generated example is as follows:
{{
    "score": "",
    "reason": "",
    "improved result":""
}}
Explanation of the example:
* score: Give a fraction, expressed numerically.
* reason: Give the reason for the score. If it fails to get a full score or is worse, please give a deduction point and describe the optimization results.
* Improved output: Give a better result based on the reason description to solve the shortcomings you mentioned. The format is required to be consistent with the output. When the score is lower than 5 points, improved output must be provided.

Notice: 
The modified data must be complete. When no modification is needed, it can be represented by an empty string. A complete json format result must be generated.
"""