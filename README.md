# per-forum
一个基于Flask框架的在线技术论坛

论坛地址：[http://45.76.214.245/](http://45.76.214.245/)

- 使用MongoDB存取数据；

- 前端使用Jinja2模板渲染网页，提高代码的复用；

- 对用户密码实现加盐加密，对于重要操作，插入随机数token进行验证，防范CSRF攻击，编写程序审查用户上传内容防范XSS攻击；

- 使用Nginx反向代理，压缩静态文件，设置缓存提高访问速度，配合gunicorn实现多进程负载均衡，利用supervisor自动监控程序运行状态；

- 使用国外VPS虚拟服务器部署；

- 使用Vagrant实现开发环境和部署环境的一致化；

- 编写Shell脚本实现一键部署，提高部署效率。

论坛分为游客，用户，管理员三个模式：
游客具有查看帖子，查看评论，查看作者信息等权限；

![image](https://github.com/QAQAL/per-forum/blob/master/demo/visit.gif)

注册登录后，用户除了具有游客的所有权限以外，还有发帖，评论，在评论中@用户，给用户发送私信，收看发给自己的私信和@，查看个人信息，更改个人用户名，个性签名，密码，头像等权限；

![image](https://github.com/QAQAL/per-forum/blob/master/demo/user.gif)

把固定id和用户名的用户设置为管理员（唯一不重复），管理员除了具有普通用户的所有权限以外，还具有添加板块，删除板块及其板块下的帖子和评论，更改其他普通用户的用户名，个性签名，密码，删除帖子及其下的评论，删除用户及其下的帖子和评论和被删除帖子下的评论。

![image](https://github.com/QAQAL/per-forum/blob/master/demo/admin.gif)
