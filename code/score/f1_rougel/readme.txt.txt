1. 为了能够对中文分词，必须把jieba.cache放在同一路径下
2. 将其他模型的生成结果放在jsonl的"output"中，注意ex任务必须要是json格式：
"output": {"恶意软件名称": "Griffon木马", "混淆技术": ["大量注释文本对抗检测", "UVRqb函数提取不可见表格字符串", "偏移算法IBjdq1x92解密字符串"], "执行逻辑": ["使用UVRqb函数从word文档不可见表格提取字符串", "偏移算法IBjdq1x92解密字符串"], "通信逻辑": ["尝试链接到bypassociation.com域名的不同路径"], "URL": ["https[:]/bypassociation.com/[path1]/[path2]?type=name"], "path1路径选项": ["images", "pictures", "img", "info", "new"], "path2路径选项": ["sync", "show", "hide", "add", "new", "renew", "delete"]}
gen任务是字符串格式
"output": "Godlua Backdoor是一个高度隐蔽的恶意软件，使用HTTPS和DNS over HTTPS技术来保护其与C2服务器的通信。它具备强大的适应性，能够针对不同的计算机平台进行攻击，并且支持多种C2指令来执行攻击者的命令。Godlua Backdoor的两个版本显示了其不断演变和更新的能力，其中活跃版本已经针对Windows和Linux平台进行了优化，并增加了新的功能。通过分析其C2协议和加密算法，可以看出其使用了复杂的冗余机制来存储C2地址，以及通过动态运行Lua代码对特定目标如www.liuxiaobei.top网站发起HTTP Flood攻击，显示了其攻击手段的多样性和针对性。总体来看，Godlua Backdoor对网络空间安全构成了严重威胁，需要网络安全专家对其相关IP、URL和域名进行监控和封锁，以减轻其潜在的破坏。"
3.  将结果命名为test-result-xxx.jsonl，如test-result-qwen1_5-cot.jsonl，放置在result文件夹中
4. 运行score_batch.sh，分数结果会出现在score文件夹的test-result-qwen1_5-cot-ex-en.log文件中，ex-en对应英文抽取、gen-en对应英文生成、ex-zh对应中文抽取、gen-zh对应中文生成，然后填入表格https://my.feishu.cn/sheets/K6W7sGWVNhan8Htx4zDcwQtendh?from=from_copylink