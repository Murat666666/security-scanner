def analyze_vulnerabilities(service, vulns):
    if not vulns:
        return "✔️ No known vulnerabilities"

    critical = [v for v in vulns if v["severity"] == "CRITICAL"]
    high = [v for v in vulns if v["severity"] == "HIGH"]

    if critical:
        return f"🚨 CRITICAL RISK ({len(critical)} vulnerabilities)"

    if high:
        return f"⚠️ HIGH RISK ({len(high)} vulnerabilities)"

    return f"ℹ️ {len(vulns)} vulnerabilities found"
