# app.py
from flask import Flask, render_template, jsonify
import pandas as pd
import os
import json
import warnings

# 忽略无关警告
warnings.filterwarnings('ignore')

# 初始化Flask应用
app = Flask(__name__, 
            template_folder='templates',  # 指定模板目录
            static_folder='static')       # 指定静态资源目录

# ===================== 目录初始化 =====================
# 确保所有必要目录存在
required_dirs = [
    'data/raw',
    'data/processed',
    'data/visualizations',
    'static/images',
    'templates'
]
for dir_path in required_dirs:
    os.makedirs(dir_path, exist_ok=True)

# ===================== 全局工具函数 =====================
def load_json_data(file_path):
    """安全加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_csv_sample(file_path, sample_size=10):
    """加载CSV文件的样本数据"""
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        # 处理空值
        df = df.fillna('未知')
        # 转换为字典（仅返回前N条）
        return df.head(sample_size).to_dict('records')
    except FileNotFoundError:
        return []

# ===================== 路由定义 =====================
@app.route('/')
def index():
    """主页面：加载统计数据、分析结果、图表信息"""
    print("📱 访问主页面...")
    
    # 1. 加载统计数据（爬虫生成）
    stats = load_json_data('data/statistics.json')
    # 补充默认值（避免数据缺失导致页面报错）
    stats_default = {
        'books_count': 0,
        'courses_count': 0,
        'news_count': 0,
        'notices_count': 0,
        'summary': {'total_records': 0}
    }
    stats = {**stats_default, **stats}

    # 2. 加载分析结果（处理器生成）
    analysis = load_json_data('data/analysis.json')

    # 3. 加载图表列表（匹配visualizer.py生成的图表）
    charts = [
        {"name": "图书分类分布", "file": "book_category.png", "desc": "Top10图书分类的数量分布"},
        {"name": "课程学分分布", "file": "course_credit.png", "desc": "课程学分的占比情况"},
        {"name": "新闻发布趋势", "file": "news_trend.png", "desc": "新闻发布的月度变化趋势"},
        {"name": "公告类型分布", "file": "notice_type.png", "desc": "各类公告的数量分布"}
    ]

    # 渲染模板
    return render_template('index.html', 
                           stats=stats, 
                           analysis=analysis, 
                           charts=charts)

@app.route('/api/samples')
def get_samples():
    """获取所有数据类型的样本（供前端展示）"""
    print("📊 加载数据样本...")
    return jsonify({
        'books_sample': load_csv_sample('data/processed/books_clean.csv'),
        'courses_sample': load_csv_sample('data/processed/courses_clean.csv'),
        'news_sample': load_csv_sample('data/processed/news_clean.csv'),
        'notices_sample': load_csv_sample('data/processed/notices_clean.csv')
    })

@app.route('/api/books')
def get_books():
    """获取图书完整数据"""
    return jsonify(load_csv_sample('data/processed/books_clean.csv', 100))

@app.route('/api/courses')
def get_courses():
    """获取课程完整数据"""
    return jsonify(load_csv_sample('data/processed/courses_clean.csv', 100))

@app.route('/api/news')
def get_news():
    """获取新闻完整数据"""
    return jsonify(load_csv_sample('data/processed/news_clean.csv', 100))

@app.route('/api/notices')
def get_notices():
    """获取公告完整数据"""
    return jsonify(load_csv_sample('data/processed/notices_clean.csv', 100))

@app.route('/api/health')
def health_check():
    """健康检查接口（供部署平台检测）"""
    return jsonify({
        'status': 'healthy',
        'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_dir_exists': os.path.exists('data')
    })

# ===================== 错误处理 =====================
@app.errorhandler(404)
def page_not_found(e):
    """404页面"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """500页面"""
    return render_template('500.html'), 500

# ===================== 启动配置 =====================
if __name__ == '__main__':
    # 本地运行配置（部署时由main.py调用）
    app.run(
        host='0.0.0.0',    # 允许外部访问
        port=5000,         # 端口
        debug=False,       # 生产环境关闭debug
        threaded=True      # 开启多线程
    )