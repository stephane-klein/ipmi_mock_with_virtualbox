.PHONY: init
init:
	virtualenv . -p python3
	bin/pip install -U -r requirements-dev.txt
	make -C . gen-proto
	bin/pip install -e .

.PHONY: gen-proto
gen-proto:
	bin/python -m grpc_tools.protoc --proto_path=ipmi_mock --python_out=ipmi_mock --grpc_python_out=ipmi_mock ipmi.proto

.PHONY: build-wheel
build-wheel:
	bin/python setup.py bdist_wheel

.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf build/
	rm -rf dist/
	rm -rf ipmi_mock.egg-info
