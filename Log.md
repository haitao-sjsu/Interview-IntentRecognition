### 8月24号，周六，10:00
开始尝试面试第3题，意图识别系统。面试第1题，是一道玩具智力题，我没有兴趣；面试第2题，我不太理解它的意思。第3题，和我上个学期的课程项目有些关联。

### 8月24号，周六，11:13
确定了一些大致的思路与框架：
* 基本思路：从微信学生群搜集一些学生常提出的问题，然后利用chatgpt生成对应的embedding vector，intent summary以及intent category。以此作为一个小型dataset。
* 如何识别意图：将用户的查询转化为embedding vector，并计算dataset里的所有vector与该vector之间的similarity。选取similarity最高的item，输出其intent summary，并将用户的该条记录记入dataset中。当然这个做法的是O（n）的复杂度，无法应用在大型项目上。
* 如何进行意图分类：利用dataset中的embedding vector和intent category作为supervised machine learning的training data，训练某个分类算法。再应用至用户的查询。
* 前端：React。一个流行的Javascript library。我从未使用过。预计需要1-2个小时学习，并完成一个简单的网页，允许用户输入查询句子，输出用户的意图及其分类。
* 后端：Flask。一个轻量级python library。

### 8月24号，周六，13:29
完成了dataset的搜集及格式化。格式大约是inquiry,intent summary,intent category。至于embedding vector，这玩意太长，直接写在dataset里会使文件的可读性变差。暂定如下：使用时调用openAI的API临时生成。

### 8月24号，周六，17:07
* 初步设计了核心类IntentRecognition，在其中设计了识别意图的算法searchForIntent()；
* 利用chatgpt完成了front-end的初步设计，使用了react。
* 利用chatgpt完成了back-end的初步设计，使用了Flask。并且初步和IntentRecognition进行了数据交互。
* First Milestone!

### 8月24号，周六，19:11
* 利用RandomForestClassifier训练了一个简单的分类器，但是因为数据太少，缺少测试数据。除此以外，还应当加入“无法分类”这个类别。
* 实现用户可以往DataFrame中添加自定义数据

### 8月24号，周六，22:17
* 利用chatgpt进行了训练数据的增广，使其从35行增加至60行。
* 更改了分类器，但是效果依然不好。明天继续尝试。
* chatgpt提示了一个库FAISS，能够在O(log(n))的时间内找到最相似的向量。明天尝试。
* 当有新数据加入时，更新硬盘上的数据，以及重新训练分类器。
* 把前端、后端以及核心类打通，开心！
* Second Milestone！

### 8月25号，周日，10:00
继续工作。

### 8月25号，周日，13:31
* 使用FAISS，设计了一个新的class Searcher，改进了搜索效率。
* 解决了Classifier中的引用问题。这样新的数据来时，可以在新旧数据的基础上，重新训练。
* 在预测分类时，当最大概率低于0.5时，则输出“不确定分类”。
* 作为一道面试题，代码部分就到此为止吧。剩下的时间写一写文档和代码注释
* Third Milestone!

### 8月25号，周日，17:35
文档完成。
