from fastapi.responses import JSONResponse
import subprocess
import sys
def StopServer():
    try:
        # シェルスクリプトをバックグラウンドで実行
        process = subprocess.Popen(
            ["bash", "/src/script/stop_server.sh"],  # スクリプトのパスを指定
            stdout=subprocess.PIPE,  # 標準出力をキャプチャ
            stderr=subprocess.PIPE,  # 標準エラー出力をキャプチャ
            text=True,  # 結果を文字列として取得
            bufsize=1,  # 行バッファリングを有効にする
            universal_newlines=True,  # 改行を自動で変換
            start_new_session=True  # 新しいセッションを作成してバックグラウンドで実行
        )

        for line in process.stdout:
            print(line, end='')  # 標準出力のログを表示

        # 標準エラー出力をリアルタイムで表示
        for line in process.stderr:
            print(line, end='', file=sys.stderr)  # 標準エラー出力のログを表示

        # プロセスの終了を待つ
        process.wait()
        
        # スクリプトの終了コードに基づくレスポンス
        if process.returncode == 0:
            return JSONResponse(content={"status": "Server sopped successfully"}, status_code=200)
        elif process.returncode == 1:
            return JSONResponse(content={"status": "Server is not running"}, status_code=409)
        else:
            return JSONResponse(content={"status": "Server failed to stop", "error": f"Error code: {process.returncode}"}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"status": "An error occurred while running the script", "error": str(e)}, status_code=500)

