# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant machine for testing purposes.

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.hostname = "ubitquity"
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.provider "virtualbox" do |v|
    v.name = "ubitquity"
    v.memory = 1024
    v.cpus = 1
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt update
    sudo apt install python3-pip
    sudo apt install build-essential libssl-dev
    sudo apt install autoconf
    sudo apt install libtool
    sudo apt install libffi-dev
    sudo apt install libgmp-dev
    sudo apt install libsecp256k1-dev
    sudo apt install pkg-config
    sudo pip3 install -r /vagrant/requirements.txt
  SHELL
end
