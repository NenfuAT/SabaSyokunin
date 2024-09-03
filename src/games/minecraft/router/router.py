import os

import uvicorn
from fastapi import FastAPI
from service import backup_server, start_server, stop_server,delete_server


def Init():
	app = FastAPI()
	port = os.environ['MINECRAFT_API_PORT']


	@app.get("/")
	async def root():
		return {"message": "Hello World"}

	@app.get("/api")
	async def api():
		return {"message": "It'sAPI"}
	
	@app.get("/api/start")
	async def api_start():
		res= start_server.StartServer()
		return res
	@app.get("/api/stop")
	async def api_stop():
		res= stop_server.StopServer()
		return res
	@app.get("/api/backup")
	async def api_backup():
		res= backup_server.BackupServer()
		return res
	@app.get("/api/delete")
	async def api_delete():
		res= delete_server.DeleteServer()
		return res
	uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")