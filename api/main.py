from fastapi import FastAPI, Form
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
        <style>
            body {
                background-color: #020617;
                color: #e2e8f0;
                font-family: Arial;
                text-align: center;
                padding: 50px;
            }
            input, button {
                padding: 12px;
                margin: 10px;
                border-radius: 8px;
                border: none;
            }
            input {
                width: 250px;
            }
            button {
                background-color: #22c55e;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #16a34a;
            }
            .box {
                background: #1e293b;
                padding: 40px;
                border-radius: 15px;
                display: inline-block;
            }
        </style>
    </head>
    <body>

        <div class="box">
            <h1>🛡️ Security Scanner</h1>

            <form method="post">
                <input name="host" placeholder="IP or domain (scanme.nmap.org)" required><br>
                <input name="ports" placeholder="Ports (22,80,443)" required><br>
                <button type="submit">🚀 Scan</button>
            </form>
        </div>

    </body>
    </html>
    """


@app.post("/", response_class=HTMLResponse)
async def scan_web(host: str = Form(...), ports: str = Form(...)):
    try:
        port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]

        result = await scan_target(host, port_list)
        save_scan(host, ports, result)

        rows = ""

        for r in result:
            service = r.get("service", {})

            service_text = f"{service.get('name','')} {service.get('product','')} {service.get('version','')}".strip()

            ai = r.get("ai", "")
            vulns_count = len(r.get("vulns", []))

            if "CRITICAL" in ai:
                ai_class = "danger"
            elif "HIGH" in ai:
                ai_class = "warn"
            else:
                ai_class = "safe"

            rows += f"""
            <tr>
                <td>{r['port']}</td>
                <td>{service_text}</td>
                <td>{vulns_count}</td>
                <td class="{ai_class}">{ai}</td>
            </tr>
            """

        return f"""
        <html>
        <head>
            <style>
                body {{
                    background-color: #020617;
                    color: white;
                    font-family: Arial;
                    padding: 40px;
                    text-align: center;
                }}
                table {{
                    margin: auto;
                    border-collapse: collapse;
                    width: 70%;
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #334155;
                }}
                th {{
                    background-color: #1e293b;
                }}
                tr:nth-child(even) {{
                    background-color: #0f172a;
                }}
                .safe {{ color: #22c55e; }}
                .warn {{ color: #facc15; }}
                .danger {{ color: #ef4444; }}
                a {{
                    color: #38bdf8;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>

        <h1>📊 Scan Result</h1>

        <table>
        <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Vulnerabilities</th>
            <th>Status</th>
        </tr>

        {rows}

        </table>

        <br><br>
        <a href="/">⬅ Back</a>

        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <html>
        <body style="background:#020617;color:white;font-family:Arial;text-align:center;padding:50px;">
            <h1>❌ Error</h1>
            <p>{str(e)}</p>
            <br><a href="/" style="color:#38bdf8;">⬅ Back</a>
        </body>
        </html>
        """
