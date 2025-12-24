"""
数据处理模块 - 更新版（支持多数据类型）
"""
import pandas as pd
import json
from datetime import datetime
import os
import numpy as np

def load_data():
    """加载所有类型的数据"""
    print("📂 加载数据文件...")    
    data_files = {
        "books": "data/raw/books.csv",
        "courses": "data/raw/courses.csv", 
        "news": "data/raw/news.csv",
        "notices": "data/raw/notices.csv"  # 新增
    }    
    loaded_data = {}   
    for data_type, file_path in data_files.items():
        try:
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, encoding='utf-8')
                loaded_data[data_type] = df
                print(f"✅ 加载 {data_type}: {len(df)}条")
            else:
                print(f"⚠️ 文件不存在: {file_path}")
                loaded_data[data_type] = pd.DataFrame()
        except Exception as e:
            print(f"❌ 加载 {data_type} 失败: {e}")
            loaded_data[data_type] = pd.DataFrame()   
    return (
        loaded_data.get("books", pd.DataFrame()),
        loaded_data.get("courses", pd.DataFrame()),
        loaded_data.get("news", pd.DataFrame()),
        loaded_data.get("notices", pd.DataFrame())  # 新增返回值
    )
def clean_books(df):
    """清洗图书数据"""
    if df.empty:
        print("📚 图书数据为空")
        return df    
    print(f"🧹 清洗图书数据 ({len(df)}条)...")    
    # 去重
    df = df.drop_duplicates()    
    # 处理年份
    if 'year' in df.columns:
        df['year'] = df['year'].astype(str)
        df['year_clean'] = df['year'].str.extract(r'(\d{4})', expand=False)
        df['year_clean'] = pd.to_numeric(df['year_clean'], errors='coerce')
        df['year_clean'] = df['year_clean'].fillna(2023).astype(int)    
    # 确保必要列存在
    required_columns = {
        'title': '未命名图书',
        'author': '未知作者', 
        'category': '未分类',
        'publisher': '未知出版社'
    }    
    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default    
    print(f"✅ 图书清洗完成: {len(df)}条")
    return df
def clean_courses(df):
    """清洗课程数据"""
    if df.empty:
        print("📝 课程数据为空")
        return df    
    print(f"🧹 清洗课程数据 ({len(df)}条)...")    
    df = df.drop_duplicates()    
    # 处理学分
    if 'credit' in df.columns:
        df['credit'] = pd.to_numeric(df['credit'], errors='coerce')
        df['credit'] = df['credit'].fillna(2).astype(int)    
    # 处理学时
    if 'hours' in df.columns:
        df['hours'] = pd.to_numeric(df['hours'], errors='coerce')
        df['hours'] = df['hours'].fillna(32).astype(int)    
    # 确保必要列存在
    required_columns = {
        'name': '未命名课程',
        'teacher': '未知教师',
        'department': '未指定院系',
        'code': '未编号'
    }    
    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default    
    print(f"✅ 课程清洗完成: {len(df)}条")
    return df
def clean_news(df):
    """清洗新闻数据"""
    if df.empty:
        print("📰 新闻数据为空")
        return df    
    print(f"🧹 清洗新闻数据 ({len(df)}条)...")    
    df = df.drop_duplicates()    
    # 处理日期
    if 'date' in df.columns:
        df['date'] = df['date'].astype(str)
        df['date_clean'] = pd.to_datetime(df['date'], errors='coerce', format='mixed')
        df['date_clean'] = df['date_clean'].fillna(pd.Timestamp('2024-01-01'))   
    # 处理内容长度
    if 'summary' in df.columns:
        df['summary'] = df['summary'].astype(str)
        df['summary_length'] = df['summary'].str.len()
    elif 'content' in df.columns:
        df['content'] = df['content'].astype(str)
        df['content_length'] = df['content'].str.len()   
    # 确保必要列存在
    required_columns = {
        'title': '未命名新闻',
        'category': '综合新闻',
        'source': '未知来源'
    }   
    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default   
    print(f"✅ 新闻清洗完成: {len(df)}条")
    return df
def clean_notices(df):
    """清洗通知公告数据（新增函数）"""
    if df.empty:
        print("📢 公告数据为空")
        return df    
    print(f"🧹 清洗公告数据 ({len(df)}条)...")    
    df = df.drop_duplicates()    
    # 处理日期
    if 'date' in df.columns:
        df['date'] = df['date'].astype(str)
        df['date_clean'] = pd.to_datetime(df['date'], errors='coerce', format='mixed')
        df['date_clean'] = df['date_clean'].fillna(pd.Timestamp('2024-01-01'))   
    # 处理内容
    if 'content' in df.columns:
        df['content'] = df['content'].astype(str)
        df['content_length'] = df['content'].str.len()    
    # 分类处理
    if 'category' not in df.columns:
        if 'type' in df.columns:
            df['category'] = df['type']
        else:
            df['category'] = '通知公告'   
    # 确保必要列存在
    required_columns = {
        'title': '未命名通知',
        'category': '通知公告',
        'source': '北京大学相关部门'
    }   
    for col, default in required_columns.items():
        if col not in df.columns:
            df[col] = default    
    print(f"✅ 公告清洗完成: {len(df)}条")
    return df
def analyze_all_data(books, courses, news, notices):
    """分析所有数据"""
    print("📊 开始数据分析...")   
    analysis = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_records": len(books) + len(courses) + len(news) + len(notices),
            "books_count": len(books),
            "courses_count": len(courses), 
            "news_count": len(news),
            "notices_count": len(notices)  # 新增
        },
        "books_analysis": {},
        "courses_analysis": {},
        "news_analysis": {},
        "notices_analysis": {}  # 新增
    }    
    # 1. 图书分析
    if not books.empty:
        if 'category' in books.columns:
            cat_counts = books['category'].value_counts().head(10)
            analysis["books_analysis"]["top_categories"] = cat_counts.to_dict()
        
        if 'year_clean' in books.columns:
            analysis["books_analysis"]["year_stats"] = {
                "average_year": int(books['year_clean'].mean()),
                "latest_year": int(books['year_clean'].max()),
                "year_range": f"{int(books['year_clean'].min())}-{int(books['year_clean'].max())}"
            }    
    # 2. 课程分析
    if not courses.empty:
        if 'department' in courses.columns:
            dept_counts = courses['department'].value_counts().head(10)
            analysis["courses_analysis"]["top_departments"] = dept_counts.to_dict()
        
        if 'credit' in courses.columns:
            analysis["courses_analysis"]["credit_stats"] = {
                "average_credit": float(courses['credit'].mean()),
                "max_credit": int(courses['credit'].max()),
                "min_credit": int(courses['credit'].min())
            }    
    # 3. 新闻分析
    if not news.empty:
        if 'category' in news.columns:
            news_cat_counts = news['category'].value_counts().head(10)
            analysis["news_analysis"]["categories"] = news_cat_counts.to_dict()
        
        if 'date_clean' in news.columns:
            date_range = {
                "start": news['date_clean'].min().strftime("%Y-%m-%d"),
                "end": news['date_clean'].max().strftime("%Y-%m-%d")
            }
            analysis["news_analysis"]["date_range"] = date_range   
    # 4. 公告分析（新增）
    if not notices.empty:
        if 'category' in notices.columns:
            notice_cat_counts = notices['category'].value_counts().head(10)
            analysis["notices_analysis"]["categories"] = notice_cat_counts.to_dict()
        
        if 'date_clean' in notices.columns:
            notice_dates = {
                "start": notices['date_clean'].min().strftime("%Y-%m-%d"),
                "end": notices['date_clean'].max().strftime("%Y-%m-%d"),
                "total_days": (notices['date_clean'].max() - notices['date_clean'].min()).days
            }
            analysis["notices_analysis"]["date_info"] = notice_dates       
        if 'content_length' in notices.columns:
            analysis["notices_analysis"]["content_stats"] = {
                "avg_length": int(notices['content_length'].mean()),
                "max_length": int(notices['content_length'].max()),
                "min_length": int(notices['content_length'].min())
            }   
    print("✅ 数据分析完成")
    return analysis
def save_processed_data(books_clean, courses_clean, news_clean, notices_clean):
    """保存处理后的数据"""
    print("💾 保存处理后的数据...")    
    os.makedirs("data/processed", exist_ok=True)   
    # 保存每种数据
    data_to_save = [
        ("books", books_clean),
        ("courses", courses_clean),
        ("news", news_clean),
        ("notices", notices_clean)  # 新增
    ]   
    for name, df in data_to_save:
        if not df.empty:
            file_path = f"data/processed/{name}_clean.csv"
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"   ✅ {name}: {len(df)}条 -> {file_path}")    
    # 创建合并数据集（用于分析）
    merged_data = []    
    for name, df in data_to_save:
        if not df.empty:
            # 添加类型标识
            df_copy = df.copy()
            df_copy['data_type'] = name           
            # 选择通用列
            common_cols = []
            for col in ['title', 'name', 'author', 'teacher', 'category', 'date', 'date_clean']:
                if col in df_copy.columns:
                    common_cols.append(col)            
            common_cols.append('data_type')            
            if common_cols:
                merged_data.append(df_copy[common_cols])    
    if merged_data:
        merged_df = pd.concat(merged_data, ignore_index=True)
        merged_df.to_csv("data/processed/merged_data.csv", index=False, encoding='utf-8-sig')
        print(f"   ✅ 合并数据: {len(merged_df)}条 -> data/processed/merged_data.csv")
def save_analysis_results(analysis, books_clean, courses_clean, news_clean, notices_clean):
    """保存分析结果和样本数据"""
    print("📄 保存分析结果...")    
    # 自定义JSON序列化器
    def custom_serializer(obj):
        if isinstance(obj, (datetime, pd.Timestamp)):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif pd.isna(obj):
            return None
        raise TypeError(f"Type {type(obj)} not serializable")   
    # 保存分析结果
    try:
        with open("data/analysis.json", "w", encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2, default=custom_serializer)
        print("   ✅ 分析结果 -> data/analysis.json")
    except Exception as e:
        print(f"   ⚠️ 保存分析结果失败: {e}")   
    # 保存数据样本（前100条）
    print("📋 保存数据样本...")   
    sample_data = {
        "sample_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "books_sample": books_clean.head(100).to_dict('records') if not books_clean.empty else [],
        "courses_sample": courses_clean.head(100).to_dict('records') if not courses_clean.empty else [],
        "news_sample": news_clean.head(100).to_dict('records') if not news_clean.empty else [],
        "notices_sample": notices_clean.head(100).to_dict('records') if not notices_clean.empty else []  # 新增
    }   
    # 清理样本数据中的非序列化对象
    def clean_dict_list(data_list):
        cleaned = []
        for item in data_list:
            cleaned_item = {}
            for key, value in item.items():
                if isinstance(value, (datetime, pd.Timestamp)):
                    cleaned_item[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif pd.isna(value):
                    cleaned_item[key] = None
                elif isinstance(value, (np.integer, np.int64)):
                    cleaned_item[key] = int(value)
                elif isinstance(value, (np.floating, np.float64)):
                    cleaned_item[key] = float(value)
                else:
                    cleaned_item[key] = value
            cleaned.append(cleaned_item)
        return cleaned   
    for key in ['books_sample', 'courses_sample', 'news_sample', 'notices_sample']:
        if sample_data[key]:
            sample_data[key] = clean_dict_list(sample_data[key])    
    try:
        with open("data/samples.json", "w", encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2, default=custom_serializer)
        print("   ✅ 数据样本 -> data/samples.json")
    except Exception as e:
        print(f"   ⚠️ 保存样本失败: {e}")
def run_processing():
    """运行数据处理流程"""
    print("\n" + "=" * 60)
    print("数据处理流程")
    print("=" * 60)   
    start_time = time.time() if 'time' in globals() else datetime.now().timestamp()   
    try:
        # 1. 加载数据
        books, courses, news, notices = load_data()       
        if books.empty and courses.empty and news.empty and notices.empty:
            print("❌ 没有找到任何数据文件")
            return None    
        # 2. 清洗数据
        print("\n" + "-" * 40)
        print("数据清洗")
        print("-" * 40)        
        books_clean = clean_books(books)
        courses_clean = clean_courses(courses)
        news_clean = clean_news(news)
        notices_clean = clean_notices(notices)  # 新增        
        # 3. 保存处理后的数据
        print("\n" + "-" * 40)
        print("保存数据")
        print("-" * 40)      
        save_processed_data(books_clean, courses_clean, news_clean, notices_clean)      
        # 4. 分析数据
        print("\n" + "-" * 40)
        print("数据分析")
        print("-" * 40)       
        analysis = analyze_all_data(books_clean, courses_clean, news_clean, notices_clean)      
        # 5. 保存分析结果
        print("\n" + "-" * 40)
        print("保存结果")
        print("-" * 40)      
        save_analysis_results(analysis, books_clean, courses_clean, news_clean, notices_clean)       
        # 6. 显示统计信息
        total_time = (datetime.now().timestamp() - start_time) if 'time' in globals() else 0      
        print("\n" + "=" * 60)
        print("✅ 数据处理完成!")
        print("=" * 60)        
        print(f"\n📊 数据统计:")
        print(f"   图书数据: {len(books_clean)}条")
        print(f"   课程数据: {len(courses_clean)}条")
        print(f"   新闻数据: {len(news_clean)}条")
        print(f"   公告数据: {len(notices_clean)}条")
        print(f"   总计: {analysis['summary']['total_records']}条")        
        print(f"\n⏱️  处理耗时: {total_time:.2f}秒")
        print(f"📁 输出目录: data/processed/")
        print(f"📄 分析文件: data/analysis.json")
        print(f"📋 样本文件: data/samples.json")
        print("=" * 60)     
        return analysis       
    except Exception as e:
        print(f"\n❌ 数据处理失败: {e}")
        import traceback
        traceback.print_exc()
        return None
# 添加time模块导入（如果需要）
import time
if __name__ == "__main__":
    run_processing()