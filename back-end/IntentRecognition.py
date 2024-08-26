from OpenAI import getEmbedding
from Classifier import Classifier
from Searcher import Searcher

import numpy as np
import pandas as pd

class IntentRecognition:
    # 初始化方法
    # 功能：初始化IntentRecognition类
    # 核心类成员
    # intentDataFrame：包含query、category、intent、embedding的DataFrame
    # clf：分类器
    # searcher：搜索器
    # 参数
    # datasetName：数据集文件名称
    # embeddingName：嵌入向量文件名称
    # 返回值：无
    def __init__(self, datasetName: str, embeddingName: str):
        self.intentDataFrame = pd.concat([pd.read_csv(datasetName), pd.read_csv(embeddingName)], axis=1)
        # 将embedding列的字符串转换为numpy数组
        self.intentDataFrame['embedding'] = self.intentDataFrame['embedding'].apply(lambda x: np.fromstring(x.strip('[]'), sep=','))
        # 初始化搜索器
        self.searcher = Searcher(self.intentDataFrame)
        # 初始化分类器
        self.clf = Classifier(self.intentDataFrame)
        self.clf.train()

    # searchForIntent方法
    # 功能：根据用户输入的消息，搜索最相似的意图
    # 参数
    # message：用户输入的消息，字符串类型
    # 返回值
    # nearestIntent：最相似的意图，字符串类型
    def searchForIntent(self, message: str):
        messageEmbedding = getEmbedding(message)
        nearestIntent = self.searcher.searchSimilarIntent(messageEmbedding)
        return nearestIntent
    
    # classify方法
    # 功能：根据用户输入的消息，分类意图
    # 参数
    # message：用户输入的消息，字符串类型
    # 返回值
    # category：分类结果，字符串类型
    def classify(self, message: str):
        messageEmbedding = getEmbedding(message)
        category = self.clf.predict(messageEmbedding)
        return category

    # addCustomIntent方法
    # 功能：添加自定义数据
    # 参数
    # query：用户输入的消息，字符串类型
    # category：分类结果，字符串类型
    # intent：意图，字符串类型
    # 返回值：无
    def addCustomIntent(self, query: str, category: str, intent: str):
        # 生成一行新的DataFrame
        newDataFrame = pd.DataFrame([{"query": query, "category": category, "intent": intent, "embedding": getEmbedding(query)}])
        # 将新的DataFrame写入文件
        newDataFrame[["query", "category", "intent"]].to_csv("dataset.csv", mode='a', header=False, index=False)
        newDataFrame["embedding"].to_csv("embedding.csv",  mode='a', header=False, index=False)
        # 将新的DataFrame添加到intentDataFrame
        # 请注意这里不能使用append或者concat方法，因为这两个方法会生成新的DataFrame，而不是在原DataFrame上进行修改
        self.intentDataFrame.loc[len(self.intentDataFrame)] = newDataFrame.iloc[0]
        # 重新训练分类器
        self.clf.train()
        # 将新的DataFrame添加到搜索器
        self.searcher.add(newDataFrame)
        
