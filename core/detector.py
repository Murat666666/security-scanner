import re

def detect_service(banner, port):
    banner = banner.lower()

    if "ssh" in banner:
        return {
            "name": "ssh",
            "product": "openssh",
            "version": extract_version(banner)
        }

    if "http" in banner:
        return extract_http_info(banner)

    if port == 443:
        return {"name": "https", "product": "unknown", "version": "unknown"}

    return {"name": "unknown", "product": "unknown", "version": "unknown"}


def extract_version(text):
    match = re.search(r"\d+\.\d+(\.\d+)?", text)
    return match.group(0) if match else "unknown"


def extract_http_info(text):
    if "apache" in text:
        return {
            "name": "http",
            "product": "apache",
            "version": extract_version(text)
        }

    if "nginx" in text:
        return {
            "name": "http",
            "product": "nginx",
            "version": extract_version(text)
        }

    return {"name": "http", "product": "unknown", "version": "unknown"}