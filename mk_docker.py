#!/usr/bin/python -d
# created by jan.szczyra@ista.com

import docker

# config
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
ver = client.version()

# handling containers (tests)
# for container in client.containers.list(all):
    # container.start()
    # container.stop()

# variables
status = '0'
data = ' Container-check '
containers = client.containers.list('status=running')

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
    data = data + 'RUNNING_CONTAINERS=' + str(len(containers))
except KeyError:
    status = '1'
    data = data + 'No running containers!'
finally:
    message = status + data
    print message
