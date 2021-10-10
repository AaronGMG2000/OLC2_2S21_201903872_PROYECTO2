from fastapi.middleware.cors import CORSMiddleware
from routes import IndexRouters as routes
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router)


@app.get('/')
async def root():
    return True

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=3000,
                reload=True, log_level="info", access_log=False)
