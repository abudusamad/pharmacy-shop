# CORS or "Cross-Origin Resource Sharing"
# refers to the situations when a frontend running in a browser has
# JavaScript code that communicates with a backend, and the backend is
# in a different "origin" than the frontend.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origin = [
	"http://localhost:8080",
	"http://localhost.tiangolo.com",
	"https://localhost.tiangolo.com",
	"http://localhost"
]


app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.get("/")
async def main():
	return {"message": "Hello World"}