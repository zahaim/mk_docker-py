#!/usr/bin/python -d
# created by jan.szczyra@gmail.com

import docker
import requests
import sys

# config
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# global variables
status = '0'
data = ' Container-check '

def docker_check():
    # variables
    global status
    global data

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
    else:
        return version

def calculate_CPU_percent(stat):
    cpu_Delta = stat['cpu_stats']['cpu_usage']['total_usage'] - stat['precpu_stats']['cpu_usage']['total_usage']
    system_Delta = stat['cpu_stats']['system_cpu_usage'] - stat['precpu_stats']['system_cpu_usage']
    cpu_percent = float(cpu_Delta)/system_Delta * \
    len(stat['cpu_stats']['cpu_usage']['percpu_usage']) * 100

    return cpu_percent

def main():
    # variables
    global status
    global data
    # checking the version of docker installed (or not)
    version = str(docker_check())

    # build running container list
    containers = client.containers.list()

    # initialization of variables
    total_cpu_usage = 0
    total_mem_usage = 0
    total_mem_total = 0

    try:
        for container in containers:
            # getting statistics
            stat = container.stats(decode=False, stream=False)

            # calculating CPU usage
            try:
                cpu_usage = calculate_CPU_percent(stat)
            except KeyError:
                cpu_usage = 0

            total_cpu_usage += cpu_usage

            # getting MEMory stats
            try:
                mem_usage = stat['memory_stats']['usage']
                mem_total = stat['memory_stats']['limit']
            except KeyError:
                mem_usage = 0
                mem_total = 0

            total_mem_usage += mem_usage
            total_mem_total += mem_total

            # getting NETwork statistics
            try:
                net_total = str(stat['networks'].values()[0]['rx_bytes'] + \
                stat['networks'].values()[0]['tx_bytes'])
            except KeyError:
                net_total = '0'

            data = data + \
            'CPU_' + container.name + '=' + \
            str(cpu_usage) + ';;;0;100' + '|' + \
            'MEM_' + container.name + '=' + \
            str(mem_usage) + ';;;0;' + str(mem_total) + '|' \
            'NET_' + container.name + '=' + \
            net_total + ';;;0;|'

        total_cpu_usage = 'TOTAL_CPU_USAGE=' + str(total_cpu_usage) + ';;;0;100' + '|'
        total_mem_usage = 'TOTAL_MEM_USAGE=' + str(total_mem_usage) + \
        ';;;0;' + str(total_mem_total) + '|'
        running = 'RUNNING_CONTAINERS=' + str(len(containers))
        data = data + total_cpu_usage + total_mem_usage + running + ' ' + running
    except KeyError:
        status = '1'
        data = data + 'No running containers!'
    finally:
        message = status + data + ' Docker ver: ' + version
        print message

if __name__ == '__main__':
    main()
