# feihu-web-server
# 后端搭建

> 环境
>
> ubuntu16.04 和 pipenv



## flask（python web框架）

相关文件说明

- Pipfile及Pipfile.lock用于pipenv下载管理包（自动更新）

- blueprints文件夹是蓝本，api.py用于注册接口，可拓展
- extensions.py 管理拓展，目前只有sqlite
- models.py 管理模型（数据库）
- settings.py管理设置（路径，环境等）
- __init\_\_.py 定义初始化方法供wsgi.py调用

- wsgi.py WSGI服务器调用程序

在蓝本中写好页面与接口，初始化中注册蓝本，与开发坏境不同的是需要将__init\_\_.py再封装一下，让wsgi服务器（gunicore）去承载wsgi.py中的app对象

上面的完成后在虚拟环境里执行

```shell
pipenv install gunicore
sudo ufw allow 8000
gunicore --workers=4 --bind=0.0.0.0:8000 wsgi:app
```

第一行安装wsgi服务器gunicore

第二行打开8000端口

第三行运行程序，workers=4即4个进程，绑定到本地地址8000端口，模块名wsgi，对象名app

## 域名申请

1.阿里云注册域名  [链接](https://wanwang.aliyun.com/domain/tld?spm=5176.22941746.J_2447957890.22.7c28a5f6oJAej8#.com)

这里只能注册到二级域名，如xxxx.xxx，子域名可注册成功后自行添加

添加dns解析（购买域名后可免费使用阿里云解析，不过需实名认证，1天）

![image-20210907090921568](D:\笔记\后端搭建\image-20210907090921568.png)

主机记录为三级域名，@表示主域名，A类记录指绑定到ipv4，txt一般用作设置说明，记录值为服务器ip地址

2.ICP备案 [链接](https://beian.aliyun.com/?spm=a2cmq.17629970.0.0.f0d079feqFxEYo)

现在阿里云提交备案申请，他们初审通过后会提交至工信部ICP备案系统，中间会有一个验证要填写二维码，具体看流程。

审核需要1-6天，可以在阿里云或者[工信部ICP系统](https://beian.miit.gov.cn/#/Integrated/index)查看进度

## 证书申请

小程序域名只支持https访问，所以还需要申请ssl证书

不建议购买（普遍很贵）

免费的CA组织有[letsencrypt](https://letsencrypt.org/)和[zero ssl](https://zerossl.com/)

以letsencrypt为例，acme客户端选择官方推荐的[certbot](https://certbot.eff.org/)

1. Ping 一下自己的域名，确定域名已经被解析

2. 执行命令 `apt-get install letsencrypt` 安装 letsencrypt

3. 执行命令`apt-get install snapd`安装snapd

4. 执行命令`sudo snap install core; sudo snap refresh core`确保snapd最新

5. 执行命令`sudo snap install --classic certbot`安装certbot

6. 执行命令`sudo ln -s /snap/bin/certbot /usr/bin/certbot`添加可执行命令

7. 执行命令 `certbot certonly --standalone --email xxx@xxx.xxx -d xxx.xxx -d xxx.xxx.xxx` 进行获取证书流程，根据提示，输入信息，域名，邮箱等

8. 获取证书流程结束后，会生成两个文件，在接下来的的 Nginx 配置中会用到
   `/etc/letsencrypt/live/xxx.xxx/fullchain.pem /etc/letsencrypt/live/xxx.xxx/privkey.pem`

   xxx.xxx即域名

如果`sudo certbot renew --dry-run`不报错说明已开启自动续期证书

## nginx配置

`apt-get install nginx`安装nginx

```shell
sudo rm /etc/nginx/sites-enabled/default
sudo nano /etc/nginx/sites-enabled/mp_feihu
```

先删除默认配置，然后新建mp_feihu配置文件，文件内容会自动插入全局配置（/etc/nginx/nginx.conf的http块中）

配置文件内容如下

```text
server {
    listen 80;
    listen [::]:80;
    server_name mpdfxjtu.top;
 	return 301 https://mpdfxjtu.top$request_uri;
}

server {
    listen 443 ssl;
    server_name mpdfxjtu.top;
    ssl on;
    ssl_certificate /etc/letsencrypt/live/mpdfxjtu.top/cert.pem;
    ssl_certificate_key /etc/letsencrypt/live/mpdfxjtu.top/privkey.pem;
 
    location / {
        proxy_pass https://127.0.0.1:8000;
        
        proxy_set_header	Host				$host;
        proxy_set_header	X-Real-Ip			$remote_addr;
        proxy_set_header	X-Forwarded-For		$proxy_add_x_forwarded_for;        
        proxy_set_header	X-Forwarded-Proto	$scheme;
    }
}
```

`service nginx start` 启动 Nginx

失败有可能是80和443被占用,杀掉进程再启动
