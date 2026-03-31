from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core.scanner import scan_target
from core.db import init_db, save_scan, get_scans

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app = FastAPI()
init_db()


@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Security Scanner Running 🚀</h1>"


@app.get("/scan")
async def scan(host: str, ports: str):
    port_list = [int(p) for p in ports.split(",")]

    result = await scan_target(host, port_list)

    save_scan(host, ports, result)

    return {"result": result}


@app.get("/history")
def history():
    return {"scans": get_scans()}