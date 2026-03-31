from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from core.scanner import scan_target
from core.db import init_db, save_scan, get_scans

import asyncio

app = FastAPI()
init_db()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Ana sayfa, formu gösterir
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/", response_class=HTMLResponse)
async def run_scan(
    request: Request,
    host: str = Form(...),
    ports: str = Form(...)
):
    # Formdan gelen IP ve portları al
    port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
    
    # Scan işlemini çalıştır
    result = await scan_target(host, port_list)
    
    # Sonucu veritabanına kaydet
    save_scan(host, ports, result)
    
    # Template ile sonucu gönder
    return templates.TemplateResponse("index.html", {"request": request, "result": result})
    

@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    scans = get_scans()
    return templates.TemplateResponse("history.html", {"request": request, "scans": scans})
