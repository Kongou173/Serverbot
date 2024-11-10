# ベースイメージとしてPython 3.9を指定
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt ./
COPY main.py ./
COPY keep_alive.py ./

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Botを実行
CMD ["python", "main.py"]
