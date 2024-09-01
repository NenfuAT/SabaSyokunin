import uvicorn
from fastapi import FastAPI


def Init():
	app = FastAPI()


	@app.get("/")
	async def root():
		return {"message": "Hello World"}

	@app.get("/api")
	async def root():
		return {"message": "It'sAPI"}
	uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")