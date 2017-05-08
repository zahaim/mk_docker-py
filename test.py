#!/usr/bin/python -d
# created by jan.szczyra@ista.com

import docker
import requests

# config
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# handling containers with dockerpy
for container in client.containers.list(all):
    container.start()
    container.stop()

    # for debuging
    # print repr(stat)
    # print container.name
