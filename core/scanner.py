import asyncio
from core.detector import detect_service
from core.vulns import fetch_cves
from core.ai import analyze_vulnerabilities


async def grab_banner(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)

        data = await reader.read(1024)
        banner = data.decode(errors="ignore")

        writer.close()
        await writer.wait_closed()

        return banner

    except:
        return ""


async def scan(host, ports):
    tasks = []

    for port in ports:
        tasks.append(scan_port(host, port))

    return await asyncio.gather(*tasks)


async def scan_port(host, port):
    try:
        banner = await grab_banner(host, port)

        return {
            "port": port,
            "status": "open",
            "banner": banner
        }
    except:
        return {"port": port, "status": "closed"}


async def scan_target(host, ports):
    results = await scan(host, ports)

    enriched = []

    for r in results:
        if r["status"] == "open":
            service = detect_service(r["banner"], r["port"])

            vulns = []
            if service["product"] != "unknown":
                vulns = await fetch_cves(service["product"], service["version"])

            ai = analyze_vulnerabilities(service["product"], vulns)

            enriched.append({
                **r,
                "service": service,
                "vulnerabilities": vulns,
                "ai": ai
            })

    return enriched