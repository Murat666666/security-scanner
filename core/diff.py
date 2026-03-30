def diff_scans(old, new):
    old_ports = {r["port"] for r in old}
    new_ports = {r["port"] for r in new}

    return {
        "new_ports": list(new_ports - old_ports),
        "closed_ports": list(old_ports - new_ports)
    }