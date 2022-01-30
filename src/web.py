from fastapi import FastAPI, Path, Request, responses
from database import Database
from logger import log
from smtp import SMTPServer
import uvicorn
import os

app = FastAPI()


@app.middleware("http")
async def endpoints_protection(request: Request, call_next):
    provided_secret = request.headers.get("ss2a-apikey", None)
    expected_secret = os.environ.get("SS2A_APIKEY", None)
    if provided_secret != expected_secret:
        return responses.JSONResponse(status_code=403)
    response = await call_next(request)
    return response


@app.get("/")
async def home():
    return {}


@app.get("/emails/{email}/")
async def get_emails(email=Path(...)):
    return Database.instance.get_email(email)


@app.get("/smtp/status/")
async def smtp_status():
    return {"status": SMTPServer.instance.status()}


@app.post("/smtp/start/")
async def smtp_start():
    await SMTPServer.instance.start()
    return {}


@app.post("/smtp/stop/")
async def smtp_stop():
    await SMTPServer.instance.stop()
    return {}


def start_web_server():
    log("Starting Web Server")
    uvicorn.run("web:app", host="0.0.0.0", port=5000, log_level="info")
