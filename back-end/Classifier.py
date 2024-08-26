from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
from sklearn.multiclass import OneVsRestClassifier

from sklearn.metrics import accuracy_score

import numpy as np

class Classifier:
    # 初始化方法
    # 功能：初始化Classifier类
    # 核心类成员
    # df：引用，指向包含category、embedding的DataFrame
    # model：机器学习模型
    # label_encoder：标签编码器。将类别转换为数字，并且可以逆转换
    # 参数
    # dataFrame：包含category、embedding的DataFrame
    # 返回值：无
    def __init__(self, dataFrame):
        self.df = dataFrame
        # 需要说明的是，如果用户新增数据，我们需要重新训练，故此处model设置为None
        self.model = None
        self.label_encoder = LabelEncoder()

    # train方法
    # 功能：训练分类器
    # 参数：无
    # 返回值：无
    def train(self):
        self.model = OneVsRestClassifier(xgb.XGBClassifier())
        self.df["category_encoded"] = self.label_encoder.fit_transform(self.df["category"])

        X = np.vstack(self.df['embedding'].values)
        y = self.df['category_encoded'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy * 100 : .2f}%", flush=True)

    # predict方法
    # 功能：预测类别
    # 参数
    # embedding_vector：嵌入向量
    # 返回值：预测的类别，字符串类型
    def predict(self, embedding_vector):
        probs = self.model.predict_proba([embedding_vector])
        max_prob = np.max(probs, axis=1)[0]
        category_encoded = np.argmax(probs, axis=1)
        if max_prob < 0.5:
            return "不确定分类"
        else:
            predicted_category = self.label_encoder.inverse_transform(category_encoded)[0]
            return predicted_category