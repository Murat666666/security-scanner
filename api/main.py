from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.scanner import scan_target
from core.db import init_db, save_scan, get_scans

import os

app = FastAPI()

# ✅ doğru path (Render uyumlu)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

init_db()


# ✅ TEK homepage (HTML)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/scan")
async def scan(host: str, ports: str):
    port_list = [int(p) for p in ports.split(",")]
    result = await scan_target(host, port_list)

    save_scan(host, ports, result)

    return {"result": result}


@app.get("/history")
def history():
    return {"scans": get_scans()}
