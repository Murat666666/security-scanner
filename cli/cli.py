import asyncio
import sys
from core.scanner import scan_target


async def main():
    host = sys.argv[1]
    ports = [int(p) for p in sys.argv[2].split(",")]

    result = await scan_target(host, ports)

    for r in result:
        print(f"\nPort: {r['port']}")
        print(f"Service: {r['service']}")
        print(f"AI: {r['ai']}")


if __name__ == "__main__":
    asyncio.run(main())
