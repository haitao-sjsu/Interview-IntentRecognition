import openai
import pandas as pd

MODEL = "gpt-3.5-turbo"
MODEL_EMBEDDING = "text-embedding-3-small"
client = openai.OpenAI()

# getEmbedding函数
# 功能：获取文本的嵌入向量
# 参数
# text：字符串类型，待获取嵌入向量的文本
# 返回值：文本的嵌入向量
def getEmbedding(text):
    return client.embeddings.create(input=[text], model=MODEL_EMBEDDING, dimensions=256).data[0].embedding

# 用于dataset的生成，项目中不需要调用
def getResponse(sysMsg, usrMsg):
    messages =   [  
    {'role':'system', 
    'content': sysMsg},    
    {'role':'user', 
    'content': usrMsg},  
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content

# 用于dataset的生成，项目中不需要调用
def createEmbeddingFile(inputFileName):
    data = pd.read_csv(inputFileName)
    data["embedding"] = data["query"].apply(getEmbedding)
    data["embedding"].to_csv("embedding.csv", index=False)

#createEmbeddingFile("dataset.csv")