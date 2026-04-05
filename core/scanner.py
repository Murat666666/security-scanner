import asyncio


async def scan_port(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()

        service = detect_service(port)

        return {
            "port": port,
            "service": service,
            "ai": analyze(service)
        }
    except:
        return None


def detect_service(port):
    common = {
        22: "ssh",
        80: "http",
        443: "https",
        3306: "mysql"
    }

    name = common.get(port, "unknown")

    return {
        "name": name,
        "product": name.upper(),
        "version": "1.0"
    }


def analyze(service):
    if service["name"] in ["ssh", "mysql"]:
        return "⚠️ Medium risk service exposed"
    elif service["name"] == "unknown":
        return "❓ Unknown service"
    else:
        return "✔️ No vulnerabilities detected"


async def scan_target(host, ports):
    tasks = [scan_port(host, p) for p in ports]
    results = await asyncio.gather(*tasks)

    return [r for r in results if r]
