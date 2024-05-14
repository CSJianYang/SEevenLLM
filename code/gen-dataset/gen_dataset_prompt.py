PROMPT="""
{input}
Based on the above content and the task described next, combined with your knowledge of cyberspace security, focusing on high-quality instructions and output results.
The category of extraction task that need to be performed based on a cybersecurity incident is: {category}.
Regarding this task and the content of network security incidents, the thought you can refer to is: {thought}.


A sample format for generating results is as follows:
Sample：{{
    "category": "Key Entity Recognition",
    "instruction": "Execute the following information extraction task and return the results in json format: Analyze and extract key entities in cyber security incidents.",
    "input": "The ATW organization was established in June 2021. Although the account signature is set as a national organization, it is in fact a loose network organization spontaneously formed by professionals such as programmers and network engineers in Europe and North America. In October 2021, the ATW organization began to be active frequently, constantly opening new accounts on overseas social platforms such as Telegram groups (https://t.me/s/ATW2022, Email:AgainstTheWest@riseup.net, backup Email:apt49@riseup.net), Twitter (@_AgainstTheWest, https://mobile.twitter.com/_AgainstTheWest), Breadched (Account: AgainstTheWest), etc., to expand its propaganda channels and show a clear pro-American and Western political inclination.
    The technical team has been tracking for a long time and found that there are 6 active members of the ATW organization on weekdays, most of whom are engaged in related professions such as programmers and network engineers, mainly located in Switzerland, France, Poland, Canada and other countries. Among them, the identity information of 2 key members is as follows:
    Tillie Kottmann, born on August 7, 1999 in Lucerne, Switzerland, self-proclaims as a hacker, anarchist, homosexual, and regards herself as a woman. After Tillie Kottmann's Twitter account @nyancrimew was suspended by Twitter, it was re-registered for use in February 2022. From January 2023 to the present, she has posted and retweeted 78 times.
    Pawel Duda, a male, Polish, software engineer. This person usually conducts hacker technology research.
    The investigation found that the ATW organization claimed to attack and steal data related to party and government organs, scientific research institutions, etc., but actually all came from small and medium-sized information technology and software development companies that provide software development for important units. Stolen data is mostly test data during development. Mainly carry out large-scale scanning and attacks on technical vulnerabilities existing in open-source network systems such as SonarQube, Gogs, Gitblit, etc., and steal related source code, data, etc. The relevant information can be used to further exploit and penetrate the involved network information system, which is a typical supply chain attack.",
    "thought":"The task of key entity recognition in cyber security incidents needs to identify information such as attack organizations, related software, main characters, virtual accounts, emails, etc. in the text",
    "output": {{
    "Attack Organization": "ATW Organization",
    "Related Software": ["SonarQube","Gogs","Gitblit"],
    "Email":["AgainstTheWest@riseup.net","apt49@riseup.net"],
    "Main Characters":["Tillie Kottmann","Pawel Duda"],
    "URL":["https://t.me/s/ATW2022","https://mobile.twitter.com/_AgainstTheWest"],
    "Virtual Accounts": ["AgainstTheWest","@_AgainstTheWest"],
    "Attacker Regions": ["Switzerland","France","Poland","Canada"]
    }}
}}
Explanation of the sample：
* category: Indicates the task type. Use the given task category.
* instruction: It is an instruction generated for this task and is required to be as common as possible in all network security incident analysis problems.
* input: It is an excerpt of valuable information from the text. It must be a complete paragraph and contain as much information as possible.
* thought: It is a chain of thinking that involves step-by-step thinking in the process of generating output based on input based on the understanding of task category and instruction.You can use the given thought directly, or optimize based on instruction and input.
* output: It requires you to generate an appropriate form of answer based on your thought chain according to the requirements of the instruction and the content in the input. The output result must be consistent with the json format in the text.

# Notice: 
The output of this sample is only for the Key Entity Recognition task to clarify your overall output format. For the sample results of other tasks, please ensure that the result form is correct according to the task type. For example, when extracting relationships, it is best to use relational triples to represent the output.
Each generated sample is represented by a json and can be placed in one line.
"""