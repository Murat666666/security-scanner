def analyze_vulnerabilities(service, vulns):
    if not vulns:
        return "✔️ No vulnerabilities detected"

    critical = [v for v in vulns if v["severity"] == "CRITICAL"]
    high = [v for v in vulns if v["severity"] == "HIGH"]

    if critical:
        return f"🚨 Critical risk! {len(critical)} critical vulnerabilities"

    if high:
        return f"⚠️ High risk! {len(high)} high vulnerabilities"

    return f"ℹ️ {len(vulns)} vulnerabilities found"