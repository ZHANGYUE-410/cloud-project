# main.py
import os
import time
from datetime import datetime

# 导入所有依赖函数
from crawler import run_crawler
from processor import run_processing
from visualizer import run_visualization
from app import app

def main():
    print("=" * 50)
    print("北京大学校园数据分析平台")
    print("=" * 50)
    
    try:
        # 1. 爬取数据
        print("\n[1/4] 开始爬取数据...")
        stats_crawl = run_crawler()
        
        # 2. 处理数据
        print("\n[2/4] 开始处理数据...")
        analysis = run_processing()
        
        # 3. 生成可视化
        print("\n[3/4] 生成可视化图表...")
        run_visualization()
        
        # 4. 启动Web服务（关键：host=0.0.0.0）
        print("\n[4/4] 启动Web服务...")
        print("✅ 平台已启动！访问 http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        raise

if __name__ == "__main__":
    # 确保数据目录存在
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    main()