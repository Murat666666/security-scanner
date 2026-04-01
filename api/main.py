from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from core.scanner import scan_target
from core.db import init_db, save_scan

app = FastAPI()
init_db()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Security Scanner</title>
    </head>
    <body style="font-family: Arial; padding:40px;">
        <h1>🚀 Security Scanner</h1>

        <form method="post">
            <input name="host" placeholder="IP (127.0.0.1)" required>
            <input name="ports" placeholder="Ports (22,80)" required>
            <button type="submit">Scan</button>
        </form>
    </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
async def scan_web(host: str = Form(...), ports: str = Form(...)):
    port_list = [int(p) for p in ports.split(",") if p.strip().isdigit()]

    result = await scan_target(host, port_list)

    save_scan(host, ports, result)

    # sonucu HTML olarak göster
    rows = ""
    for r in result:
        rows += f"<tr><td>{r['port']}</td><td>{r['service']}</td><td>{r['ai']}</td></tr>"

    return f"""
    <html>
    <body style="font-family: Arial; padding:40px;">
        <h1>Scan Result</h1>

        <table border="1" cellpadding="10">
            <tr>
                <th>Port</th>
                <th>Service</th>
                <th>AI</th>
            </tr>
            {rows}
        </table>

        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """
