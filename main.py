import logging
import sys
import datetime
import uvicorn
from fastapi import FastAPI
from app.settings import SettingsLocal
from app.database import SessionLocal, AutoBase
from app.logger import get_logger

app = FastAPI(
    debug=SettingsLocal.APP_DEBUG,
    title=SettingsLocal.APP_NAME,
)

logger = get_logger(__name__)

@app.get("/")
async def root():
    return {
        "message": "Welcome to {}".format(SettingsLocal.APP_NAME),
        "time": datetime.datetime.now()
    }


@app.get("/search")
async def say_hello(query: str):
    logger.info(f"Query is {query}")
    return {"message": f"Hello {query}"}

# just for development locally
if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=3335,
        reload=True,
        workers=None,
        root_path="",
        proxy_headers=True,
        log_level=SettingsLocal.LOG_LEVEL
    )