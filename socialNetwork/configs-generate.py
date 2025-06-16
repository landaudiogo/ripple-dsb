import json
from pathlib import Path
import yaml
import sys


USAGE = f"""
Usage: {sys.argv[0]} <ip-vm1> <ip-vm2> <ip-vm3> <original-service-config>

Arguments: 
    ip-vm1: vm1's IP address
    ip-vm2: vm2's IP address
    ip-vm3: vm3's IP address
    original-service-config: The original config file that located at `DeathStarBench/mediaMicroservices/config/service-config.json`
"""

def main(argv):
    if len(argv) != 5: 
        print(USAGE)
        sys.exit(1)

    vmips = {1: argv[1], 2: argv[2], 3: argv[3]}

    path = Path(argv[4])
    with open(path, "r") as f:
        svc_conf_og = json.load(f)

    vmservices = {}
    for i in range(1, 4):
        vmservices[i] = []
        with open(f"compose-vm{i}.yaml", "r") as f:
            compose = yaml.safe_load(f)

        for (service, value) in compose["services"].items():
            if service == "dns-media":
                continue
            host = value["hostname"]
            port = ""
            if host in svc_conf_og: 
                port = value["ports"][0].split(":")[0]
            if "social-network-microservices" in value["image"]:
                value["ports"][0] = f"{port}:{port}"
                value["volumes"] = [
                    "./compose-service-config.json:/social-network-microservices/config/service-config.json",
                    "/etc/resolv.conf:/etc/resolv.conf"
                ]
            vmservices[i].append(f"{host}:{port}")

        with open(f"compose-vm{i}.yaml", "w") as f:
            yaml.dump(compose, f, indent=2)


    svc_conf = {"secret": "secret"}
    for vm, services in vmservices.items():
        for service in services:
            host, port = service.split(":")
            if port == "":
                continue
            svc_conf[host] = {
                "addr": host,
                "port": int(port)
            }
    with open("compose-service-config.json", "w") as f:
        json.dump(svc_conf, f, indent=4)
    
    for i in range(1, 4):
        dns_proxy_config = {
            "version" : 2,
            "activeEnv" : "",
            "remoteDnsServers" : [],
            "envs" : [{
                "name": "",
                "hostnames": [{
                    "id" : 1,
                    "hostname" : "jaeger",
                    "ip" : vmips[3],
                    "ttl" : 60,
                    "type" : "A"
                }]
            }]
        }
        id = 2
        for key, services in vmservices.items():
            for service in services:
                host = service.split(":")[0]
                dns_proxy_config["envs"][0]["hostnames"].append({
                    "id" : id,
                    "hostname" : host,
                    "ip" : vmips[key],
                    "ttl" : 60,
                    "type" : "A"
                })
                id += 1
        with open(f"dns{i}-config.json", "w") as f:
            json.dump(dns_proxy_config, f, indent=4)


if __name__ == "__main__":
    main(sys.argv)
