"""
Web应用 - 数据展示界面
"""
from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """首页"""
    # 加载统计数据
    with open('data/statistics.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    # 加载分析结果
    with open('data/analysis.json', 'r', encoding='utf-8') as f:
        analysis = json.load(f)
    
    # 加载图表信息
    with open('static/charts_info.json', 'r', encoding='utf-8') as f:
        charts = json.load(f)
    
    return render_template('index.html', 
                         stats=stats, 
                         analysis=analysis,
                         charts=charts)

@app.route('/api/data')
def get_data():
    """获取数据API"""
    try:
        # 返回前100条数据样本
        with open('data/samples.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "数据加载失败"})

@app.route('/api/stats')
def get_stats():
    """获取统计API"""
    try:
        with open('data/statistics.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)
        return jsonify(stats)
    except:
        return jsonify({"error": "统计加载失败"})

@app.route('/api/charts')
def get_charts():
    """获取图表列表API"""
    try:
        with open('static/charts_info.json', 'r', encoding='utf-8') as f:
            charts = json.load(f)
        return jsonify(charts)
    except:
        return jsonify([])

if __name__ == '__main__':
    # 创建必要目录
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # 简单HTML模板
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>北京大学校园数据分析平台</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
            h1 { color: #333; text-align: center; }
            .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }
            .stat-card { background: #4ECDC4; color: white; padding: 20px; border-radius: 8px; text-align: center; }
            .charts { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
            .chart img { width: 100%; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .data-sample { background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 北京大学校园数据分析平台</h1>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📚 图书数据</h3>
                    <h2>{{ stats.books }}</h2>
                    <p>条记录</p>
                </div>
                <div class="stat-card">
                    <h3>📝 课程数据</h3>
                    <h2>{{ stats.courses }}</h2>
                    <p>条记录</p>
                </div>
                <div class="stat-card">
                    <h3>📰 新闻数据</h3>
                    <h2>{{ stats.news }}</h2>
                    <p>条记录</p>
                </div>
            </div>
            
            <h2>📈 可视化图表</h2>
            <div class="charts">
                {% for chart in charts %}
                <div class="chart">
                    <h3>{{ chart.name }}</h3>
                    <p>{{ chart.desc }}</p>
                    <img src="/static/{{ chart.file }}" alt="{{ chart.name }}">
                </div>
                {% endfor %}
            </div>
            
            <h2>📋 数据样本（前10条）</h2>
            <div id="data-sample">
                <p>加载中...</p>
            </div>
        </div>
        
        <script>
            // 加载数据样本
            fetch('/api/data')
                .then(res => res.json())
                .then(data => {
                    let html = '';
                    // 显示图书样本
                    html += '<h3>📚 图书样本</h3>';
                    data.books_sample.slice(0,10).forEach(book => {
                        html += `<div class="data-sample">
                            <strong>${book.title}</strong> - ${book.author}<br>
                            类别: ${book.category} | 年份: ${book.year}
                        </div>`;
                    });
                    
                    // 显示课程样本
                    html += '<h3>📝 课程样本</h3>';
                    data.courses_sample.slice(0,10).forEach(course => {
                        html += `<div class="data-sample">
                            <strong>${course.name}</strong> - ${course.teacher}<br>
                            院系: ${course.department} | 学分: ${course.credit}
                        </div>`;
                    });
                    
                    document.getElementById('data-sample').innerHTML = html;
                });
        </script>
    </body>
    </html>
    '''
    
    # 保存HTML模板
    os.makedirs('templates', exist_ok=True)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    app.run(host='0.0.0.0', port=5000, debug=True)