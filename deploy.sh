# 代码更新
git pull

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default


# 建立一个软连接
ln -s -f /root/per-forum/per-forum.conf /etc/supervisor/conf.d/per-forum.conf
# 不要再 sites-available 里面放任何东西
ln -s -f /root/per-forum/per-forum.nginx /etc/nginx/sites-enabled/per-forum

# 设置文件夹权限给nginx用
chmod -R o+rx /
chmod -R o+xr /root/per-forum

# 重启服务器
service supervisor restart
service nginx restart


echo 'deploy success'

