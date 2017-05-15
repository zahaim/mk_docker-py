# Check_mk plugin for docker containers local checks

### Just wanted to have a check for all containers on a host.

* Build it with `pyinstaller --onefile mk_docker.py`
* Put it to /usr/lib/check_mk/local
* Reinventory of check_mk host - and you should see new service (Container check)


## Checks
* memory
* cpu
* network
* number
of running containers.

## PIP Requirements
* `pip install docker`
* `pip install pyinstaller`

## Building it
As it requires additional pip packages it seemed that making it a executable file was the best solution. It was done with:
<br> `pyinstaller --onefile mk_docker.py` <br>

You can find a built file in *./dist/mk_docker* after the build.

But any other tool for python would probably do the job. Handling pip with configuration management on a target host is also an option.
