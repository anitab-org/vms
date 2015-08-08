# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box_url = "http://54.183.32.240/vagrant/box/systers-vms.box"
  config.vm.box = "systers-vms-dev"

  config.vm.provider "virtualbox" do |vb|
    vb.gui=true
  end

  config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true
  config.vm.network "forwarded_port", guest: 8000, host:8001
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.network "public_network"
end