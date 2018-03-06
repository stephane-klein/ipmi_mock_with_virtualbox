# Mock IPMI with Virtualbox

This project mock [ipmi](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface) power on/off/cycle in local Virtualbox/Vagrant environment.

## Prerequisite

On your host, you need:

* [Virtualbox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)
* [pipenv](https://github.com/pypa/pipenv) with Python3


## Test

Install and launch *ipmi-mock* server component:

```
$ pipenv install https://github.com/harobed/ipmi_mock_with_virtualbox/releases/download/master/ipmi_mock-0.1.0-py3-none-any.whl
$ pipenv shell
```

```
$ ipmimock-server
{'192.168.0.11': 'server1', '192.168.0.12': 'server2'}
Starting server. Listening on port 0.0.0.0:41000.
```


Execute *ipmitool* command in *pxe_server*:

```
$ vagrant up pxe_server
$ vagrant ssh pxe_server
$ export IPMI_MOCK_SERVER=10.0.2.2:41000
$ ipmitool -H 192.168.0.11 power on
```


## How to hack ipmi_mock?

See [ipmi_mock/README.md](ipmi_mock/).
