from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# 确保数据目录存在
os.makedirs('data/processed', exist_ok=True)

@app.route('/')
def index():
    """主页面路由"""
    return render_template('index.html')

@app.route('/api/stock_data')
def get_stock_data():
    """获取股票数据"""
    try:
        df = pd.read_csv('data/processed/stock_data_clean.csv')
        return jsonify(df.head(100).to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notices')
def get_notices():
    """获取公告数据"""
    try:
        df = pd.read_csv('data/processed/notices_clean.csv')
        return jsonify(df.head(100).to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sentiment')
def get_sentiment():
    """获取情感分析数据"""
    try:
        df = pd.read_csv('data/processed/sentiment_analysis.csv')
        return jsonify(df.head(50).to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)