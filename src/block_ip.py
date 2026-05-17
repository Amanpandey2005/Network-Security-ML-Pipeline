import subprocess

blocked_ips = set()

def block_ip(ip):

    try:

        if ip in blocked_ips:

            return

        command = f'netsh advfirewall firewall add rule name="BLOCK_{ip}" dir=in action=block remoteip={ip}'

        subprocess.run(command, shell=True)

        blocked_ips.add(ip)

        print(f"{ip} Blocked Successfully")

    except Exception as e:

        print("IP Block Error:", e)