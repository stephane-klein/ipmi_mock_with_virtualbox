.PHONY: gen-proto
gen-proto:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ipmi.proto

.PHONY: build-server
build-server:
	docker build -t harobed/mock-ipmi-server -f Dockerfile.server .

.PHONY: build-client
build-client:
	docker build -t harobed/mock-ipmi-client -f Dockerfile.client .

.PHONY: build
build: build-server build-client

.PHONY: push-server
push-server:
	docker push harobed/mock-ipmi-server

.PHONY: push-client
push-client:
	docker push harobed/mock-ipmi-client

.PHONY: push
push: push-server push-client
