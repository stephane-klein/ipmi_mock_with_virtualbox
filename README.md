# Mock IPMI with Virtualbox

This project mock [ipmi](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface) power on/off/cycle in local Virtualbox/Vagrant environment.

## Prerequisite

On your host, you need:

* [Virtualbox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)


## How to use

Install *ipmi-server-mock* component:

```
$ curl -L https://github.com/harobed/ipmi_mock_with_virtualbox/releases/download/master/ipmi-mock-server_darwin-amd64 > ipmi-mock-server
$ chmod u+x ipmi-mock-server
```

Set IP / Vagrant server name relation in config file:

```
$ cat ipmi-config.txt
192.168.0.11 server1
192.168.0.12 server2
```

Start *ipmi-server-mock*:

```
$ CONFIG_FILE=ipmi-config.txt ./ipmi-mock-server
2018/06/05 10:09:47 Load ipmi-config.txt config file
2018/06/05 10:09:47 Listen on 0.0.0.0:41000
```


Execute *ipmitool* command in *pxe_server*:

```
$ vagrant up pxe_server
$ vagrant ssh pxe_server
$ curl -L https://github.com/harobed/ipmi_mock_with_virtualbox/releases/download/master/ipmitool_linux-amd64 > ipmitool
$ chmod u+x ./ipmitool
$ export IPMI_MOCK_CONFIG_ADDRESS=10.0.2.2:41000
$ ./ipmitool -H 192.168.0.11 power on
```


## How to hack ipmi_mock?

See [ipmi_mock/README.md](ipmi_mock/).
