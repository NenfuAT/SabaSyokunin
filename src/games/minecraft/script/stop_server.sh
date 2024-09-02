#!/bin/bash
cd server

# サーバーが実行中の screen セッションを確認
session_name="papermc_server"

# セッションが存在するか確認
if ! screen -list | grep -q "$session_name"; then
    echo "No screen session found with name '$session_name'."
    exit 1
fi

# サーバーの停止コマンドを送信
screen -S "$session_name" -p 0 -X stuff "stop$(printf \\r)"

# サーバーが停止するのを待つ
sleep 10

# サーバーが停止したことを確認
if screen -list | grep -q "$session_name"; then
    echo "Failed to stop PaperMC server. Please check manually."
    exit 1
else
    echo "PaperMC server stopped successfully."
fi
