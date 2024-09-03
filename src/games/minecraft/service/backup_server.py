import os
import subprocess
import zipfile
from datetime import datetime

from fastapi.responses import JSONResponse


def BackupServer():
	try:
		result = subprocess.run(['screen', '-ls'], capture_output=True, text=True, check=False)
		if "papermc_server"in result.stdout:
			return JSONResponse(content={"status": "Server is running"}, status_code=409)
	except subprocess.CalledProcessError as e:
		print("no screen")
	# 圧縮するディレクトリと出力先の設定
	source_dir = '/src/server'
	backup_dir = '/src/backup'
	timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
	zip_name = f'server_backup_{timestamp}.zip'
	zip_path = os.path.join(backup_dir, zip_name)

	# 出力先ディレクトリが存在しない場合は作成
	if not os.path.exists(backup_dir):
		os.makedirs(backup_dir)

	try:
		zip_dir(source_dir, zip_path)
		return JSONResponse(content={"status": "Server backup successfully"}, status_code=200)
	except Exception as e:
		return JSONResponse(content={"status": "Server backup fail","error": str(e)}, status_code=500)

# 圧縮の実行
def zip_dir(dir_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # ディレクトリ内の全ファイルとサブディレクトリを追加
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # アーカイブ内のパスを作成
                arcname = os.path.relpath(file_path, start=dir_path)
                zipf.write(file_path, arcname)


