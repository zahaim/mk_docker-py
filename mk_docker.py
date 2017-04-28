#!/usr/bin/python -d
# created by jan.szczyra@ista.com

import docker

# config
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# variables
status = '0'
data = ' Container-check '

# checking if docker is installed
try:
    ver = client.version()
    version = ver['Version']
except requests.exceptions.ConnectionError:
    status = '1'
    version = 'Docker not installed'
    message = status + data + ' Docker ver: ' + version
    print message

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
        cpu_total = stat['cpu_stats']['system_cpu_usage']
        mem_usage = stat['memory_stats']['usage']
        mem_total = stat['memory_stats']['limit']
        net_total = stat['networks'].values()[0]['rx_bytes'] + stat['networks'].values()[0]['tx_bytes']
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
