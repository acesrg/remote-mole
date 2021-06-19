PROJECT_NAME=remote_mole

PEP8_CONFIG_FILE=.flake8

DOCS_DOCKERFILE=.gci/Dockerfile.docs
DOCS_IMAGE=${PROJECT_NAME}_docs_image
DEV_DOCKERFILE=.gci/Dockerfile.dev
DEV_IMAGE=${PROJECT_NAME}_dev_image

PEP8_DOCKER_IMAGE=pipelinecomponents/flake8

DEV_CONTAINER=control_lab_client_dev

DOCKER=docker run -it --rm

pep8:
	${DOCKER} -v $(PWD):/project -w /project ${PEP8_DOCKER_IMAGE} flake8 --config $(PEP8_CONFIG_FILE) .

build_docs:
	docker build -f ${DOCS_DOCKERFILE} -t ${DOCS_IMAGE} .

docs: build_docs
	${DOCKER} -v $(PWD):/project -w /project/docs ${DOCS_IMAGE}

build_dev:
	docker build -f ${DEV_DOCKERFILE} -t ${DEV_IMAGE} .

run_dev: build_dev
	docker run -dit -v $(PWD):/project -w /project --name ${DEV_CONTAINER} ${DEV_IMAGE} bash

try: run_dev
	- docker exec -it ${DEV_CONTAINER} bash
	docker stop ${DEV_CONTAINER}
	docker rm ${DEV_CONTAINER}

test: run_dev
	docker exec ${DEV_CONTAINER} pip3 install .
	docker exec ${DEV_CONTAINER} pip3 install coverage
	- docker exec -it ${DEV_CONTAINER} coverage run --source=/usr/local/lib/python3.8/site-packages/nyquist -m unittest discover -v tests/
	- docker exec -it ${DEV_CONTAINER} coverage report 
	- docker exec -it ${DEV_CONTAINER} coverage html
	docker stop ${DEV_CONTAINER}
	docker rm ${DEV_CONTAINER}

stop:
	docker stop ${DEV_CONTAINER}

clean:
	docker rm ${DEV_CONTAINER}

.PHONY: pep8 build_docs docs build_dev run_dev try test stop clean
