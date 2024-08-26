import faiss
import numpy as np

class Searcher:
    # 初始化方法
    # 功能：初始化Searcher类
    # 核心类成员
    # df：引用，指向包含query、category、intent、embedding的DataFrame
    # index：faiss索引
    # 参数
    # dataFrame：包含query、category、intent、embedding的DataFrame
    # 返回值：无
    def __init__(self, dataFrame):
        self.df = dataFrame
        self.index = faiss.IndexFlatL2(self.df['embedding'].values[0].shape[0])
        self.index.add(np.vstack(self.df['embedding'].values))
    
    # add方法
    # 功能：将新的数据加入索引中
    # 参数
    # dataFrame：包含query、category、intent、embedding的DataFrame
    # 返回值：无
    def add(self, dataFrame):
        self.index.add(np.vstack(dataFrame['embedding'].values))

    # searchSimilarIntent方法
    # 功能：搜索最相似的查询，并返回对应的意图
    # 参数
    # embedding_vector：嵌入向量
    # 返回值：
    # nearestIntent：最接近的意图，字符串类型
    def searchSimilarIntent(self, embedding_vector):
        _, I = self.index.search(np.array([embedding_vector]), 1)
        nearestIntent = self.df.iloc[I[0][0]]["intent"]
        return nearestIntent