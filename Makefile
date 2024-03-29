PROJECT = gps
include ./envs/network.env

all: install lint test format

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	# NOTE: betterproto 1.x is not full-featured, but currently 2.x is not released.
	# so uninstall betterproto 1.x and reinstall 2.x
	python3 -m pip uninstall -y betterproto
	python3 -m pip install "betterproto[compiler]" --pre

uninstall:
	python3 -m pip install --upgrade pip
	python3 -m pip uninstall -r requirements.txt

lint:
	python3 -m pylint --rcfile=pylintrc ./${PROJECT}

test:
	python3 -m unittest discover -s ./${PROJECT} -p "*_test.py" -v
	python3 -m unittest discover -s ./${PROJECT} -p "test_*.py" -v

format:
	# NOTE: Source code auto generated by grpc tool (in this Makefile: 'proto') has "*_pb2*" pattern.
	python3 -m yapf -ir . --exclude "*_pb2*"

proto:
	python3 -m grpc_tools.protoc \
		--python_out=. \
		--grpc_python_out=. \
		--python_betterproto_out=gps/proto \
		--proto_path=. \
		gps/proto/gps.proto
	# NOTE: python_out, grpc_python_out: RAW official grpc output. Use betterproto instead.
	# NOTE: betterproto also has --python_betterproto_opt=pydantic_dataclasses option but currently not stable.

clean:
	rm ./gps/proto/*.py
	rm -r ./gps/proto/gps

prefect-server:
	prefect config set PREFECT_API_URL=${PREFECT_API_URL}
	prefect config view
	prefect server start --host ${PREFECT_HOST} --port ${PREFECT_SERVER_PORT}

prefect-server-clean:
	prefect server database reset -y
