import os
import json
import subprocess
from multiprocessing import Process

rel_ip_vagrant_hostname = None

def load_config(config_file):
    global rel_ip_vagrant_hostname
    with open(config_file, 'r') as f:
        rel_ip_vagrant_hostname = json.loads(f.read())

    import pprint; pprint.pprint(rel_ip_vagrant_hostname)

def on(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("On %s - %s" % (ip, vagrant_hostname))
    def start():
        print(subprocess.run("vagrant up %s --no-provision" % vagrant_hostname, shell=True, check=True))

    Process(target=start).start()

    return True

def off(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("Off %s - %s" % (ip, vagrant_hostname))
    def start():
        print(subprocess.run("vagrant halt %s" % vagrant_hostname, shell=True, check=True))

    Process(target=start).start()

    return True

def cycle(ip):
    vagrant_hostname = rel_ip_vagrant_hostname.get(ip)
    print("Cycle %s - %s" % (ip, vagrant_hostname))
    def start():
        print(subprocess.run("vagrant reload %s --no-provision" % vagrant_hostname, shell=True, check=True))

    Process(target=start).start()

    return True
