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

    return version

def calculate_CPU_percent(stat):
    cpu_Delta = stat['cpu_stats']['cpu_usage']['total_usage'] - stat['precpu_stats']['cpu_usage']['total_usage']
    system_Delta = stat['cpu_stats']['system_cpu_usage'] - stat['precpu_stats']['system_cpu_usage']
    cpu_percent = str(float(cpu_Delta)/system_Delta * \
    len(stat['cpu_stats']['cpu_usage']['percpu_usage']) * 100)

    return cpu_percent

def main():
    # variables
    global status
    global data
    # checking the version of docker installed (or not)
    # print version
    version = str(docker_check())

    # build running container list
    containers = client.containers.list()

    try:
        for container in containers:
            stat = container.stats(decode=False, stream=False)

            # calculating CPU usage
            cpu_usage = calculate_CPU_percent(stat)
            # getting MEM and NET data from stat
            mem_usage = str(stat['memory_stats']['usage'])
            mem_total = str(stat['memory_stats']['limit'])
            # handling containers using host=net
            try:
                net_total = str(stat['networks'].values()[0]['rx_bytes'] + \
                stat['networks'].values()[0]['tx_bytes'])
            except KeyError:
                net_total = '0'
            data = data + \
            'CPU_' + container.name + '=' + \
            cpu_usage + ';;;0;100' + '|' \
            'MEM_' + container.name + '=' + \
            mem_usage + ';;;0;' + mem_total + '|' \
            'NET_' + container.name + '=' + \
            net_total + ';;;0;|'
        running = 'RUNNING_CONTAINERS=' + str(len(containers))
        data = data + running + ' ' + running
    except KeyError:
        status = '1'
        data = data + 'No running containers!'
    finally:
        message = status + data + ' Docker ver: ' + version
        print message

if __name__ == '__main__':
    main()
