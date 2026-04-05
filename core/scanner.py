import asyncio
from core.detector import detect_service
from core.vulns import fetch_cves
from core.ai import analyze_vulnerabilities


async def grab_banner(reader, writer):
    try:
        writer.write(b"HEAD / HTTP/1.0\r\n\r\n")
        await writer.drain()
        data = await asyncio.wait_for(reader.read(1024), timeout=2)
        return data.decode(errors="ignore")
    except:
        return ""


async def scan_port(host, port):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=3
        )

        banner = await grab_banner(reader, writer)
        writer.close()

        service = detect_service(banner, port)

        vulns = await fetch_cves(service["product"], service["version"])

        ai = analyze_vulnerabilities(service, vulns)

        return {
            "port": port,
            "service": service,
            "vulns": vulns,
            "ai": ai
        }

    except:
        return None


async def scan_target(host, ports):
    tasks = [scan_port(host, p) for p in ports]
    results = await asyncio.gather(*tasks)

    return [r for r in results if r]
