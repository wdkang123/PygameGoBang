# `Pygame` 五子棋 单机/联机

## 运行截图:

![pygame](https://github.com/wdkang123/PygameGoBang/blob/master/PygameGoBang/img-folder/window1.png)
![pygame](https://github.com/wdkang123/PygameGoBang/blob/master/PygameGoBang/img-folder/window2.png)



## 两个版本:

### 1 单机版(两个人一台电脑)

文件夹  `PygameGoBang` 下

直接启动即可



### 2 联机版(两台电脑两个人)

文件夹`PygameGoBang(LAN)` 下

#### 1 启动Server

确定自己的局域网IP地址

打开`server.py`

修改当中的`ip`和`port`为自己本机的IP 地址可以默认

 `self.server.bind(("192.168.1.254", 8888))`



#### 2 启动 Client

你需要和Server在一个服务器下

打开`Client.py`

修改当中的ip和port为Server的地址和端口

`self.client.connect(("192.168.1.254", 8888))`



#### 3 首先运行Server 再运行Client

即可开始游戏

当一方失败后 双方按下空格 即可重新开始一局