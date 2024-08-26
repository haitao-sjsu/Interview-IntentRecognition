# 意图识别系统

## 使用说明
请参考视频链接：https://youtu.be/TmifyQZ5i3k

## 安装及启动说明
### 库依赖
* 前端
    * `React 18.3.1`
* 后端
    * `Flask 3.0.3`
    * `Flask-Cors 4.0.1`
    * `numpy 1.24.4`
    * `pandas 2.2.1`
    * `scikit-learn 1.0.2`
    * `xgboost 2.1.1`
    * `faiss-cpu 1.8.0`
    * `openai 1.42.0`

### 本地启动说明
1. 确保上述库均已安装。
2. 在`back-end`目录下启动后端Flask：
```bash
python app.py
```
3. 在`frond-end`目录下启动前端React：
```bash
npm start
```

## 设计概览
* 对方的需求文档描述并不清楚。我对需求的理解如下：
    * 意图识别：根据用户的输入，与已有数据进行相似度计算，找到最接近的向量，并输出其对应的意图描述；
    * 意图分类：利用已有数据，训练一个分类器，并预测用户输入的分类
* 前端采用React，后端采用Flask。我并未使用过这两个框架，skeleton code由ChatGPT辅助生成。
* 后端有三个类，分别是：
    * `IntentRecognition`：整个功能实现的类。具体描述见下。
    * `Classifier`：利用机器学习训练的模型，用于预测用户输入的分类。目前采用的是`xgboost`。此外，只要有新的数据，就会重新训练。具体描述见下。
    * `Searcher`：利用`faiss`设计的临近向量查找类，时间复杂度为O(log(n))。具体描述见下。

## 数据集说明
这是一个难点，因为对方并未提供数据集。我根据自己的理解建立了一个微型数据集，过程如下：
1. 从华人学生微信群搜集一些常见问题，并利用chatgpt和人工生成对应的分类及意图描述。
2. 利用chatgpt产生更多的常见问题，进行数据增广。
3. 在测试过程中，手动望数据集中增加数据。

目前数据集分为了两个文件，`back-end/dataset.csv`以及`back-end/embedding.csv`。里面有***70+***条数据。分成两个文件的目的是增加可读性。
* `back-end/dataset.csv`：训练分类器的数据集，包括`query`、`category`以及`intent`三列。
    * `query`：用户的查询问题。字符串格式。
    * `category`：所属的意图类别。字符串格式。
    * `intent`：基于`query`的意图描述，字符串格式。

* `back-end/embedding.csv`：训练分类器的数据集，包括`embedding`一列。
    * `embedding`：利用openai的API计算`query`的embedding，每个embedding的长度设定为256。

## 简要工作流程
1. 当系统启动时，系统会从硬盘读入两个文件`dataset.csv`以及`embedding.csv`，完成分类器的训练以及搜索器索引的建立。
2. 当用户输入并点击`Recognition`按钮后，分类器会预测用户输入的类别，搜索器会找到最相近的数据，并输出其意图。
3. 当用户输入自定义的意图及类别，并点击`Submit`按钮后，新的数据会写入dataset，分类器会重新训练，搜索器会增加相应的索引。

## 各文件简要说明
`README.md`: 即本说明文档。

`Log.md`：工程日志文档。记录了这两天的工作心得。

`back-end/app.py`：`Flask`启动文件。由ChatGPT生成其框架代码。其中有一个`IntentRecognition`类的全局对象，来处理用户的输入。

`back-end/IntentRecognition.py`：核心类。负责整个系统的功能实现。其包含的方法包括：
* `__init__`：用于初始化该类，包括初始化以下成员：
    * `intentDataFrame`：`pandas`的`DataFrame`类型，dataset从硬盘读入该变量；
    * `clf`：自定义的`Classifier`类型，用于对用户的输入进行意图分类；
    * `searcher`：自定义的`Searcher`类型，用于计算和用户的输入最相近的数据库输入，并输出其意图。
* `searchForIntent`：将用户的输入字符串转化为embedding，并计算最接近的意图。
* `classify`：将用户的输入字符串转化为embedding，并利用机器学习方法预测其类别。
* `addCustomIntent`：接受用户自定义的查询、意图及类别，更新dataset，重新训练`Classifier clf`，更新`Searcher searcher`内的索引。

`back-end/Searcher.py`：利用`faiss`实现快速搜索最相似的embedding，进而输出其意图。其包含的方法包括：
* `__init__`：用于初始化该类，包括初始化以下成员：
    * `df`：指向`intentDataFrame`的引用
    * `index`：`faiss`的索引类，以实现快速搜索。
* `add`：将用户新增加的数据加入索引中。
* `searchSimilarIntent`：索最相似的查询，并返回对应的意图。

`back-end/Classifier.py`：利用机器学习模型训练分类器，并预测用户的输入的类型。其包含的方法包括：
* `__init__`：用于初始化该类，包括初始化以下成员：
    * `df`：指向`intentDataFrame`的引用
    * `model`：机器学习模型
    * `label_encoder`：标签编码器。将类别转换为数字，并且可以逆转换
* `train`：训练分类器
* `predict`：根据用户的输入预测类别。

`back-end/OpenAI.py`：利用openai提供的API计算embedding。包括的函数有：
* `getEmbedding`：获取文本的嵌入向量
* `getResponse`：用于dataset的生成，项目中不需要调用
* `createEmbeddingFile`：用于dataset的生成，项目中不需要调用

`back-end/dataset.csv`：训练分类器的数据集，上面有详细描述。

`back-end/embedding.csv`：训练分类器的数据集，上面有详细描述。

`front-end/src/App.js`：前端的网页数据。由ChatGPT生成。

`front-end/src/App.css`：前端的网页样式。由ChatGPT生成。

## 可能的改进
1. 性能改进。由于数据集太小，导致分类器的训练效果不好，而且不稳定。
2. 流程改进。真正部署到线上，一些流程就不太合适：比如，每次有新的数据，就往硬盘上写；再比如，一有新的数据就重新训练。此外，当数据集变大了之后，训练好的模型以及建立好的索引需要及时存储，以免重复运算。
3. 前端UI改进。目前UI基本由chatGPT完成。