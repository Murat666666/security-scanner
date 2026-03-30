import httpx
import os

API_KEY = os.getenv("NVD_API_KEY")
URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


async def fetch_cves(product, version):
    query = f"{product} {version}"

    headers = {}
    if API_KEY:
        headers["apiKey"] = API_KEY

    params = {
        "keywordSearch": query,
        "resultsPerPage": 3
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.get(URL, params=params, headers=headers)
            data = res.json()

            return parse(data)
        except:
            return []


def parse(data):
    results = []

    for v in data.get("vulnerabilities", []):
        cve = v["cve"]

        severity = "unknown"
        metrics = cve.get("metrics", {})

        if "cvssMetricV31" in metrics:
            severity = metrics["cvssMetricV31"][0]["cvssData"]["baseSeverity"]

        results.append({
            "cve": cve["id"],
            "severity": severity
        })

    return results