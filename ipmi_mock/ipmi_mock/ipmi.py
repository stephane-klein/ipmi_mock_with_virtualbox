import os
import json
import subprocess

rel_ip_vagrant_hostname = None

def load_config(config_file):
    global rel_ip_vagrant_hostname
    with open(config_file, 'r') as f:
        rel_ip_vagrant_hostname = json.loads(f.read())

    import pprint; pprint.pprint(rel_ip_vagrant_hostname)

def on(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("On %s - %s" % (ip, vagrant_hostname))

    subprocess.Popen("vagrant up %s --no-provision" % vagrant_hostname, shell=True)

    return True

def off(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("Off %s - %s" % (ip, vagrant_hostname))

    subprocess.Popen("vagrant halt %s -f" % vagrant_hostname, shell=True)

    return True

def cycle(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("Cycle %s - %s" % (ip, vagrant_hostname))

    subprocess.Popen("vagrant reload %s --no-provision" % vagrant_hostname, shell=True)

    return True

def status(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("Status %s - %s" % (ip, vagrant_hostname))

    p = subprocess.Popen(
        "vagrant status %s --machine-readable" % vagrant_hostname,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate()
    errcode = p.returncode

    status = [line.split(b",")[-1] for line in out.splitlines() if line.split(b",")[2] == b'state']
    if len(status):
        return True, status[0]

    return False, ""
