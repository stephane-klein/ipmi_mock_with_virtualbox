# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define :pxe_server do |pxe_server|

    # Use Ubuntu LTS version
    pxe_server.vm.box = "ubuntu/xenial64"
    pxe_server.vm.hostname = "pxe-server"
    pxe_server.vm.synced_folder '.', '/vagrant', disabled: true
    pxe_server.vm.network "private_network", ip: "192.168.0.254", virtualbox__intnet: "pxe_network"
    pxe_server.ssh.forward_agent = true

    pxe_server.vm.provider :virtualbox do |vb|
      vb.memory = '1024'
      vb.cpus = '1'
    end
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
