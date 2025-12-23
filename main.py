print("\n[1/4] 开始爬取数据...")
from crawler import run_crawler
stats = run_crawler()  # 调用新的爬虫

def main():
    """主函数"""
    print("=" * 50)
    print("北京大学校园数据分析平台")
    print("=" * 50)
    
    try:
        # 1. 爬取数据
        print("\n[1/4] 开始爬取数据...")
        from crawler import run_crawler
        run_crawler()
        
        # 2. 处理数据
        print("\n[2/4] 开始处理数据...")
        from processor import run_processing
        run_processing()
        
        # 3. 生成可视化
        print("\n[3/4] 生成可视化图表...")
        from visualizer import run_visualization
        run_visualization()
        
        # 4. 启动Web服务
        print("\n[4/4] 启动Web服务...")
        print("✅ 平台已启动！访问 http://localhost:5000")
        print("📊 数据统计已保存到 data/statistics.json")
        
        # 启动Flask应用
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    main()