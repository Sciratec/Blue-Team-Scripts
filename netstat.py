import requests
from time import sleep
from json import loads
import subprocess


def ip_lookup(**socket):

    response = requests.get(f"https://ipinfo.io/{socket['ip']}/json")
    response = loads(response.text)
    print(f"IP - {socket['ip']} :: Org - {response['org']} :: Port - {socket['port']} :: Country - {response['country']}")
    sleep(2)


def netstat():

    netstat_results = subprocess.run(["NETSTAT.EXE", "-n"], stdout=subprocess.PIPE)
    lines = netstat_results.stdout.splitlines()
    est_foreign_conns = []
    for line in lines:
        if "ESTABLISHED" in line.decode('utf-8').split():
            foreign_socket = line.decode('utf-8').split()[2]
            if "[::1]" not in foreign_socket and "127.0.0.1" not in foreign_socket:
                foreign_socket = foreign_socket.split(":")
                ip = foreign_socket[0]
                port = foreign_socket[1]
                if ip not in est_foreign_conns:
                    est_foreign_conns.append(ip)
                    ip_lookup(ip=ip, port=port)


def main():
    netstat()


if __name__ == "__main__":
    main()
