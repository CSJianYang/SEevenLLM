PROMPT = """
{input}

Based on the above content, combined with your knowledge of cyberspace security, select four extraction tasks and three generation tasks that best fit the content of cybersecurity incidents.
The task list is as follows:
Extraction Tasklist:
[
    "Key Entity Recognition","Main Relation Extraction",
    "Important Event Extraction",
    "Malware Feature Extraction",
    "Cybersecurity Event Classification",
    "Attack Tool Identification",
    "Domain Intelligence Acquisition",
    "Time Element Acquisition",
    "Network Protocol Utilization",
    "Attack Fingerprint Identification",
    "Encryption-Decryption Algorithm Identification",
    "Vulnerability Information Extraction",
    "Attacker Information Extraction",
    "Attack Target Intelligence Gathering",
]
Generation Tasklist:
[
    "Vulnerability Exploitation Analysis",
    "Attack Means Analysis",
    "Attack Strategy Analysis",
    "Attack Intent Analysis",
    "Correlation Analysis",
    "Threat Analysis",
    "Risk Assessment",
    "Impact Scope",
    "Trend Prediction",
    "Behavioral Pattern Analysis",
    "Protection Strategy Research",
    "Incident Response Planning",
    "Security Policy Audit",
    "Summary Generation",
    "Security Alert Generation"
]

A sample format for generating results is as follows:
Sample:
{{
    "Extraction Task":[
    {{
    "category": "Key Entity Recognition",
    "thought":"The task of key entity recognition in cyber security incidents needs to identify information such as attack organizations, related software, main characters, virtual accounts, emails, etc. in the text"
    }},
    {{
    "category": "Main Relation Extraction",
    "thought": "When performing primary relationship extraction, we need to identify entities in the text and the relationships between these entities. In this text, we can see that there are two attacked entities (Hejing Technology and TSMC), one attacker entity (WannaCry ransomware virus), and the relationship between these entities, such as infection, loss, etc."
    }},
    {{
    "category": "Malware Feature Extraction",
    "thought": "The malware feature extraction task requires identifying key information such as the name, attack method, propagation method, attack target, damage effect, and extortion method of the malware described in the text."
    }},
    {{
    "category": "Time Element Acquisition",
    "thought": "The task of obtaining the time elements of cybersecurity events requires identifying specific dates, years, or time periods mentioned in the text. These time points may be related to events such as virus outbreaks, attack occurrences, or loss statistics."
    }}],
    "Generation Task":[
    {{
    "category": "Summary Generation",
    "thought":"This text mainly introduces that Anheng Threat Intelligence Center discovered and reported a new 0Day vulnerability, which affects multiple versions of Windows 10, including the latest 20H2 fully patched version. When generating the summary, I needed to highlight the novelty of the vulnerability, its scope of impact, and the interaction between the Arnhem Threat Intelligence Center and Microsoft."
    }},
    {{
    "category": "Trend Prediction",
    "thought": "This text mentioned that the conflict between India and Pakistan has led to an increase in cyber attacks between the two countries, as well as the trend of APT attacks as an emerging means of gaming. When predicting future trends, I need to consider the current international political situation, technological developments, and the evolution of APT attacks, and how these factors affect the development of cybersecurity incidents."
    }},
    {{
    "category": "Correlation Analysis",
    "thought": "When conducting correlation analysis, I need to consider the similarities between attack samples, including attack methods, malware used, attack targets, etc. The bait file mentioned in the text is highly consistent with the previously analyzed samples in terms of macro code, release method, file structure, etc., and continues to be iteratively updated, but the changes are not significant, which indicates that the attackers may come from the same organization or network. While updating attack tools to adapt to defensive measures, certain attack patterns are maintained."
    }}
    ]
}}

# Notice: 
Please generate a suitable task based on the text content and provide a chain of thought for selecting this task.
The generated results are expressed in the form of a dictionary combining list and json just as the sample.
"""