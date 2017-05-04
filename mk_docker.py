#!/usr/bin/python -d
# created by jan.szczyra@ista.com

import docker
import requests

# config
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# variables
status = '0'
data = ' Container-check '

# checking if docker is installed and if API is recent
try:
    ver = client.version()
    version = ver['Version']
except requests.exceptions.ConnectionError:
    status = '1'
    data = data + 'RUNNING_CONTAINERS=0'
    version = 'Docker not installed'
    message = status + data + ' Docker ver: ' + version
    print message
    sys.exit(1)
except docker.errors.APIError:
    status = '1'
    data = data + 'RUNNING_CONTAINERS=0'
    version = 'Docker API not compatibile'
    message = status + data + ' Docker ver: ' + version
    print message
    sys.exit(1)

# handling containers (tests)
# for container in client.containers.list(all):
    # container.start()
    # container.stop()

# build running container list
containers = client.containers.list()

try:
    for container in containers:
        stat = container.stats(decode=False, stream=False)
        # print repr(stat)
        # print container.name
        cpu_usage = stat['cpu_stats']['cpu_usage']['total_usage']
        cpu_total = stat['cpu_stats']['system_cpu_usage']/1024
        mem_usage = stat['memory_stats']['usage']
        mem_total = stat['memory_stats']['limit']
        # handling non-networked containers
        try:
            net_total = stat['networks'].values()[0]['rx_bytes'] + stat['networks'].values()[0]['tx_bytes']
        except KeyError:
            net_total = 0
        data = data + \
        'CPU_' + container.name + '=' + \
        str(cpu_usage) + ';;;0;' + str(cpu_total) + '|' \
        'MEM_' + container.name + '=' + \
        str(mem_usage) + ';;;0;' + str(mem_total) + '|' \
        'NET_' + container.name + '=' + \
        str(mem_usage) + ';;;0;|'
    running = 'RUNNING_CONTAINERS=' + str(len(containers))
    data = data + running + ' ' + running
except KeyError:
    status = '1'
    data = data + 'No running containers!'
finally:
    message = status + data + ' Docker ver: ' + version
    print message
