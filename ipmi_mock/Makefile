DOCKER_ENV=$(shell test ! -f /.dockerenv; echo "$$?")

assert_out_docker:
ifeq ($(DOCKER_ENV),1)
	echo "Should not be run under a container"; exit 1
endif

.PHONY: up
up:
ifeq ($(DOCKER_ENV),0)
	docker-compose build goworkspace
	docker-compose up -d
endif

.PHONY: enter
enter:
ifeq ($(DOCKER_ENV),0)
	docker-compose exec goworkspace bash
endif

.PHONY: build
build: build-server build-client

.PHONY: build-server
build-server:
ifeq ($(DOCKER_ENV),1)
	gox \
		-os="darwin linux" \
		-arch="amd64 386" \
		-osarch="!darwin/386" \
		-output "bin/{{.OS}}_{{.Arch}}/ipmi-mock-server" \
		server/
else
	docker-compose exec goworkspace make build-server
endif

.PHONY: build-client
build-client:
ifeq ($(DOCKER_ENV),1)
	gox \
		-os="darwin linux" \
		-arch="amd64 386" \
		-osarch="!darwin/386" \
		-output "bin/{{.OS}}_{{.Arch}}/ipmitool" \
		client/
else
	docker-compose exec goworkspace make build-client
endif

.PHONY: make-release
make-release: build
	mkdir -p dist/
	cp bin/darwin_amd64/ipmi-mock-server dist/ipmi-mock-server_darwin-amd64
	cp bin/darwin_amd64/ipmitool dist/ipmitool_darwin-amd64
	cp bin/linux_amd64/ipmi-mock-server dist/ipmi-mock-server_linux-amd64
	cp bin/linux_amd64/ipmitool dist/ipmitool_linux-amd64


.PHONY: clean
clean: assert_out_docker
	docker-compose stop
	docker-compose rm -f
