# main.py
import os
import time
from datetime import datetime

# 导入所有依赖函数
from crawler import run_crawler
from processor import run_processing
from visualizer import run_visualization
from app import app

# 修复：删除重复的stats = run_crawler() 避免提前执行爬虫
# stats = run_crawler()  # 这行是多余的，已删除

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
        
        # 4. 启动Web服务（适配Zeabur端口规则）
        print("\n[4/4] 启动Web服务...")
        # 关键修复：读取Zeabur自动注入的PORT环境变量，兼容本地和部署环境
        port = int(os.environ.get("PORT", 5000))  # Zeabur默认PORT=8080，本地默认5000
        host = "0.0.0.0"  # 必须绑定0.0.0.0才能被Zeabur访问
        print(f"✅ 平台已启动！访问 http://{host}:{port}")
        app.run(
            host=host,
            port=port,
            debug=False,  # 生产环境关闭debug
            threaded=True  # 开启多线程，提升并发能力
        )
        
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        raise

if __name__ == "__main__":
    # 确保所有必要目录存在
    required_dirs = [
        'data/raw',
        'data/processed',
        'data/visualizations',
        'static',
        'static/images',  # 新增：可视化图表保存目录
        'templates'
    ]
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # 修复：删除重复的main()调用，避免执行两次全流程
    main()  # 仅保留一次调用