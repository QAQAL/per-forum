# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  # 虚拟机名字，不能改
  config.vm.box = "guavm"

  # 映射文件夹
  config.vm.synced_folder ".", "/root/per-forum"

  # 桥接网络
  config.vm.network "public_network"

  # 脚本
  # 为了方便测试下面脚本，把 bashrc 设置独立出来
  config.vm.provision "shell", inline: <<-SHELL
    # 默认 root
    echo "sudo su" >> /home/ubuntu/.bashrc
    # 换成 root 用户运行
    sudo su
    # /root/per-forum 是代码所在目录
    echo "cd /root/per-forum" >> /root/.bashrc
  SHELL
  # 环境设置
  config.vm.provision "shell", path: "configuration/setup_development.sh"
end
