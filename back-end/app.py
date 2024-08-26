from flask import Flask, request, jsonify
from flask_cors import CORS
# 导入IntentRecognition类
from IntentRecognition import IntentRecognition as IR

app = Flask(__name__)
CORS(app)
# 创建全局的意图识别器
globalIR = IR("dataset.csv", "embedding.csv")

@app.route('/api/recognize', methods=['POST'])
def recognize_intent():
    data = request.get_json()
    # 获取用户输入
    user_input = data.get('userInput')

    # 识别用户意图
    recognized_intent = globalIR.searchForIntent(user_input)
    # 对用户意图进行分类
    recognized_category = globalIR.classify(user_input)

    return jsonify({
        'intent': recognized_intent,
        'intentCategory': recognized_category
    })

@app.route('/api/submit_custom', methods=['POST'])
def submit_custom_intent():
    # 获取用户输入
    data = request.get_json()
    # 获取用户输入字符串
    user_input = data.get('userInput')
    # 获取用户自定义的意图
    custom_category = data.get('customCategory')
    # 获取用户自定义的类别
    custom_intent = data.get('customIntent')
    # 添加自定义意图
    globalIR.addCustomIntent(user_input, custom_category, custom_intent)

    return jsonify({'message': 'Custom intent and category submitted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
    