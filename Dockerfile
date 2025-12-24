# Dockerfile
FROM python:3.9-slim

# 安装系统依赖（matplotlib需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制并安装Python依赖
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . .

# 创建必要目录
RUN mkdir -p data/raw data/processed static templates

# 暴露端口
EXPOSE 5000

# 启动主程序
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]