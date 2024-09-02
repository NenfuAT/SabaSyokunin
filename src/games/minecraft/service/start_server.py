from fastapi.responses import JSONResponse
import subprocess
import sys


def StartServer():
    try:
        process = subprocess.Popen(
            ['tail', '-f','/src/log/output.log'],  # スクリプトのパスを指定
            stdout=subprocess.PIPE,  # 標準出力をキャプチャ
            stderr=subprocess.PIPE,  # 標準エラー出力をキャプチャ
            text=True,  # 結果を文字列として取得
            bufsize=1,  # 行バッファリングを有効にする
            universal_newlines=True,  # 改行を自動で変換
            start_new_session=True  # 新しいセッションを作成してバックグラウンドで実行
        )
        print("start tail")
        # 検索する文字列を設定
        help_message = 'For help, type "help"'
        
		# シェルスクリプトをバックグラウンドで実行
        result=subprocess.run(["bash", "/src/script/start_server.sh"])
        # スクリプトの終了コードに基づくレスポンス
        if result.returncode == 1:
            return JSONResponse(content={"status": "Server is already running"}, status_code=409)
        print("start server")
        # 標準出力をリアルタイムで表示し、指定のメッセージを検出
        for line in process.stdout:
            print(line, end='')  # 標準出力のログを表示
            if ':' in line:
                post_colon = line.split(':', 1)[1]  # `:`以降の部分を取得
                if help_message in post_colon:
                    print(post_colon)
                    return JSONResponse(content={"status": "Server started successfully"}, status_code=200)

        # 標準エラー出力をリアルタイムで表示
        for line in process.stderr:
            print(line, end='', file=sys.stderr)  # 標準エラー出力のログを表示

        # プロセスの終了を待つ
        process.wait()
        
        

    except Exception as e:
        return JSONResponse(content={"status": "An error occurred while running the script", "error": str(e)}, status_code=500)

