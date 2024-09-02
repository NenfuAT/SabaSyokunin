FROM ubuntu:latest

# 作業ディレクトリの設定
WORKDIR /src


# ソースコードのコピー
COPY ./src/games/minecraft .


# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    apt-get install -y screen curl jq openjdk-21-jre-headless && \
    rm -rf /var/lib/apt/lists/*

# 仮想環境の作成
RUN python3 -m venv /venv

# 仮想環境のパスを環境変数に設定
ENV PATH="/venv/bin:$PATH"

# pipのアップグレード
RUN pip install --upgrade pip

# Pythonライブラリのインストール
RUN pip install -r lib/requirements.txt

# 起動時にエントリーポイントスクリプトを実行
CMD ["bash", "-c", "chmod 700 /src/script/entrypoint.sh && /src/script/entrypoint.sh"]

