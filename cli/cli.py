import sys
import requests

def main():
    if len(sys.argv) < 3:
        print("Usage: python cli.py <host> <ports>")
        return

    host = sys.argv[1]
    ports = sys.argv[2]

    url = f"http://127.0.0.1:8000/scan?host={host}&ports={ports}"

    res = requests.get(url)
    data = res.json()

    for r in data["result"]:
        print(f"Port: {r['port']}")
        print(f"Service: {r['service']['product']}")
        print(f"AI: {r['ai']}")
        print("-" * 30)


if __name__ == "__main__":
    main()