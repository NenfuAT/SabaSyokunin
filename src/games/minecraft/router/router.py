import os

import uvicorn
from fastapi import FastAPI
from service import start_server
from service import stop_server

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
	uvicorn.run(app, host="0.0.0.0", port=port, log_level="debug")