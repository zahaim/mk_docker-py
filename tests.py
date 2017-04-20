# client.containers.run('alpine', 'echo hello world', detach=True)
# container = client.containers.run('bfirsh/reticulate-splines', detach=True)

# client.containers.prune()

# container = client.containers.run('bfirsh/reticulate-splines', detach=True)
# print container.logs()

# cont.restart()
# now = client.containers.get(cont.id)
# now.stop()
# now.remove()

# import sys
# import docker
#
# def start ( cli, event ):
#     """ handle 'start' events"""
#     print ( event )
#
# thismodule = sys.modules[__name__]
# # create a docker client object that talks to the local docker daemon
# cli = docker.DockerClient(base_url='unix://var/run/docker.sock')
# # start listening for new events
# events = cli.events(decode=True)
# # possible events are:
# #  attach, commit, copy, create, destroy, die, exec_create, exec_start, export,
# #  kill, oom, pause, rename, resize, restart, start, stop, top, unpause, update
# for event in events:
#     # if a handler for this event is defined, call it
#     if (hasattr( thismodule , event['Action'])):
#         getattr( thismodule , event['Action'])( cli, event )
