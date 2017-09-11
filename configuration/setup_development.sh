#!/usr/bin/env bash

# 默认 root
echo "sudo su" >> /home/ubuntu/.bashrc

# /root/per-forum 是代码所在目录
echo "cd /root/per-forum" >> /root/.bashrc

# 换成中科大的源
ln -f -s /root/per-forum/configuration/sources.list /etc/apt/sources.list
mkdir /root/.pip
ln -f -s /root/per-forum/configuration /root/.pip/pip.conf

# 装依赖
apt-get update
apt-get install -y git python3 python3-pip zsh
apt-get install -y nginx mongodb supervisor

pip3 install -U pip setuptools wheel
pip3 install jinja2 flask pymongo gunicorn

sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"


# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default


# 建立一个软连接
ln -s -f /root/per-forum/per-forum.conf /etc/supervisor/conf.d/per-forum.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /root/per-forum/per-forum.nginx /etc/nginx/sites-enabled/per-forum

# 设置文件夹权限给nginx用
chmod o+xr /root
chmod -R o+xr /root/per-forum

service supervisor restart
service nginx restart

echo "setup development environment successfuly"

