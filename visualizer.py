# visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings

# 忽略matplotlib字体/显示警告
warnings.filterwarnings('ignore')

# 设置matplotlib中文显示（解决中文乱码）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def run_visualization():
    """
    生成可视化图表（main.py调用的核心函数）
    基于processed目录下的清洗后数据，生成各类统计图表
    """
    print("📈 开始生成校园数据可视化图表...")
    
    # 确保可视化目录存在
    os.makedirs('data/visualizations', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)  # 供Flask前端访问
    
    # 定义图表生成函数（模块化）
    def plot_book_category():
        """图书分类分布图表"""
        try:
            df = pd.read_csv('data/processed/books_clean.csv')
            if df.empty:
                print("⚠️ 图书数据为空，跳过图书分类图表生成")
                return
            
            # 取Top10分类
            cat_counts = df['category'].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(12, 6))
            cat_counts.plot(
                kind='bar', 
                color='#1f77b4', 
                ax=ax,
                edgecolor='black',
                alpha=0.8
            )
            ax.set_title('图书分类分布（Top10）', fontsize=14, pad=20)
            ax.set_xlabel('图书分类', fontsize=12)
            ax.set_ylabel('数量', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(axis='y', alpha=0.3)
            
            # 保存图表（双路径：可视化目录+静态资源目录）
            fig.savefig('data/visualizations/book_category.png', dpi=300, bbox_inches='tight')
            fig.savefig('static/images/book_category.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            print("✅ 图书分类图表生成完成")
        except Exception as e:
            print(f"❌ 图书分类图表生成失败: {str(e)}")

    def plot_course_credit():
        """课程学分分布图表"""
        try:
            df = pd.read_csv('data/processed/courses_clean.csv')
            if df.empty:
                print("⚠️ 课程数据为空，跳过课程学分图表生成")
                return
            
            credit_counts = df['credit'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(8, 5))
            credit_counts.plot(
                kind='pie', 
                autopct='%1.1f%%', 
                ax=ax,
                colors=['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'],
                explode=[0.05] * len(credit_counts)  # 轻微分离扇区
            )
            ax.set_title('课程学分分布', fontsize=14, pad=20)
            ax.set_ylabel('')  # 隐藏y轴标签
            
            fig.savefig('data/visualizations/course_credit.png', dpi=300, bbox_inches='tight')
            fig.savefig('static/images/course_credit.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            print("✅ 课程学分图表生成完成")
        except Exception as e:
            print(f"❌ 课程学分图表生成失败: {str(e)}")

    def plot_news_trend():
        """新闻发布时间趋势图表"""
        try:
            df = pd.read_csv('data/processed/news_clean.csv')
            if df.empty:
                print("⚠️ 新闻数据为空，跳过新闻趋势图表生成")
                return
            
            # 转换发布时间为日期格式
            df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
            df = df.dropna(subset=['publish_date'])
            
            # 按月份统计
            df['month'] = df['publish_date'].dt.to_period('M')
            month_counts = df['month'].value_counts().sort_index()
            
            fig, ax = plt.subplots(figsize=(12, 6))
            month_counts.plot(
                kind='line', 
                marker='o', 
                color='#e377c2', 
                ax=ax,
                linewidth=2,
                markersize=6
            )
            ax.set_title('新闻发布月度趋势', fontsize=14, pad=20)
            ax.set_xlabel('月份', fontsize=12)
            ax.set_ylabel('发布数量', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(alpha=0.3)
            
            fig.savefig('data/visualizations/news_trend.png', dpi=300, bbox_inches='tight')
            fig.savefig('static/images/news_trend.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            print("✅ 新闻趋势图表生成完成")
        except Exception as e:
            print(f"❌ 新闻趋势图表生成失败: {str(e)}")

    def plot_notice_type():
        """公告类型分布图表"""
        try:
            df = pd.read_csv('data/processed/notices_clean.csv')
            if df.empty:
                print("⚠️ 公告数据为空，跳过公告类型图表生成")
                return
            
            type_counts = df['type'].value_counts()
            fig, ax = plt.subplots(figsize=(10, 6))
            type_counts.plot(
                kind='barh', 
                color='#7f7f7f', 
                ax=ax,
                edgecolor='black',
                alpha=0.8
            )
            ax.set_title('公告类型分布', fontsize=14, pad=20)
            ax.set_xlabel('数量', fontsize=12)
            ax.set_ylabel('公告类型', fontsize=12)
            ax.grid(axis='x', alpha=0.3)
            
            fig.savefig('data/visualizations/notice_type.png', dpi=300, bbox_inches='tight')
            fig.savefig('static/images/notice_type.png', dpi=300, bbox_inches='tight')
            plt.close(fig)
            print("✅ 公告类型图表生成完成")
        except Exception as e:
            print(f"❌ 公告类型图表生成失败: {str(e)}")

    # 执行所有图表生成
    plot_book_category()
    plot_course_credit()
    plot_news_trend()
    plot_notice_type()

    print("\n🎉 所有可视化图表生成完成！")
    print("📁 图表保存路径：")
    print("   - 数据目录：data/visualizations/")
    print("   - 静态资源：static/images/（供前端访问）")

# 测试代码（本地运行时可执行）
if __name__ == "__main__":
    # 本地测试：创建测试数据目录
    os.makedirs('data/processed', exist_ok=True)
    # 调用可视化函数
    run_visualization()