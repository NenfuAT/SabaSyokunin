import os
import subprocess

from fastapi.responses import JSONResponse


def DeleteServer():
    # 対象ディレクトリと保持するファイルのリスト
    target_dir = '/src/server'
    files_to_keep = {'eula.txt', 'paper.jar'}
    result = subprocess.run(['screen', '-ls'], capture_output=True, text=True, check=False)
    if "papermc_server"in result.stdout:
        return JSONResponse(content={"status": "Server is running"}, status_code=409)
    # 実行
    try:
        clean_directory(target_dir, files_to_keep)
        return JSONResponse(content={"status": "Server delete successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "Server delete fail"}, status_code=400)

# ディレクトリ内の全てのファイルとディレクトリを削除
def clean_directory(dir_path, keep_files):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        # ディレクトリ内のファイルをチェックして削除
        for file in files:
            if file not in keep_files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"削除しました: {file_path}")
        
        # ディレクトリが空であれば削除
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # 空であることを確認してから削除
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"削除しました: {dir_path}")


