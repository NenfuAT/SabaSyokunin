FROM python:latest

# 作業ディレクトリの設定
WORKDIR /src

# ソースコードのコピー
COPY ./src/discordbot .

# パッケージリストの更新とFFmpegのインストール
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# upgrade pip コマンド
RUN pip install --upgrade pip 

# python ライブラリのインストール
RUN pip install -r lib/requirements.txt

CMD ["python", "main.py"]