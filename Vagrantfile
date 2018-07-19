# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.provider :virtualbox do |vb|
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ] # to disable ubuntu-*-cloudimg-console.log
  end

  config.vm.define :pxe_server do |pxe_server|

    # Use Ubuntu LTS version
    pxe_server.vm.box = "bento/ubuntu-18.04"
    pxe_server.vm.hostname = "pxe-server"
    pxe_server.vm.synced_folder '.', '/vagrant', disabled: true
    pxe_server.vm.network "private_network", ip: "192.168.0.254", virtualbox__intnet: "pxe_network"
    pxe_server.ssh.forward_agent = true

    pxe_server.vm.provider :virtualbox do |vb|
      vb.memory = '1024'
      vb.cpus = '1'
    end

$script = <<SCRIPT
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y python3-pip
sudo pip3 install -U pip3
sudo pip3 install https://github.com/harobed/ipmi_mock_with_virtualbox/releases/download/master/ipmi_mock-0.1.0-py3-none-any.whl
SCRIPT

    pxe_server.vm.provision "shell", inline: $script
  end

  config.vm.define :server1 do |server1|
    server1.vm.box = "ubuntu/xenial64"
    server1.vm.hostname = "server1"
    server1.vm.network "private_network", ip: "192.168.0.11", virtualbox__intnet: "pxe_network"
    server1.vm.synced_folder '.', '/vagrant', disabled: true
    server1.vm.provider "virtualbox" do |vb, override|
        vb.memory = '1024'
        vb.cpus = '1'
    end
  end
  config.vm.define :server2 do |server2|
    server2.vm.box = "ubuntu/xenial64"
    server2.vm.hostname = "server2"
    server2.vm.network "private_network", ip: "192.168.0.12", virtualbox__intnet: "pxe_network"
    server2.vm.synced_folder '.', '/vagrant', disabled: true
    server2.vm.provider "virtualbox" do |vb, override|
      vb.memory = '1024'
      vb.cpus = '1'
    end
  end
end
