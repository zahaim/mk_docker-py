# Check_mk plugin for checking docker
## Checks
* memory
* cpu
* network
of running containers.

## PIP Requirements
* docker
* pyinstaller

## Building it
As it requires additional pip packages it seemed that making it a executable file was the best solution. It was done with:
<br> `pyinstaller --onefile mk_docker.py` <br>
But any other tool for python would probably do the job. Handling pip with configuration management is also an option