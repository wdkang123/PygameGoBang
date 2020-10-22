import pygame
import socket
import _thread


class Server:
    def __init__(self):
        # 网络部分
        self.server = socket.socket()
        self.server.bind(("192.168.1.254", 8888))
        self.server.listen(1)
        # 等待连接
        self.client, self.address = self.server.accept()

        # 发送或接收的状态
        self.status = 0

        # 棋盘的状态
        self.status_list = {}
        for each in range(0, 15 * 18):
            self.status_list[each] = 0
        # 此时的 x y
        self.x = 5
        self.y = 5

        # 谁走
        # flag 0 Server
        # flag 1 Client
        self.flag = 0

        # 谁赢了
        # Server 1
        # Client 2
        self.win = 0

        print("Server 初始化完毕")

    def restart_game(self):
        # 发送或接收的状态
        self.status = 0

        # 棋盘的状态
        self.status_list = {}
        for each in range(0, 15 * 18):
            self.status_list[each] = 0
        # 此时的 x y
        self.x = 5
        self.y = 5

        # 谁走
        # flag 0 Server
        # flag 1 Client
        self.flag = 0

        # 谁赢了
        # Server 1
        # Client 2
        self.win = 0

    def send_data(self, name):
        while True:
            if self.status == 1:
                str_data = ""
                for each in range(0, 15 * 18):
                    str_data = str(self.status_list[each]) + str_data
                str_data = str(self.x) + \
                           "---" + str(self.y) + \
                           "---" + str(self.flag) + \
                           "---" + str(self.win) + \
                           "---" + str(str_data)
                self.client.send(str_data.encode("UTF-8"))
                self.status = 0

    def recevie_data(self, name):
        while True:
            data = self.client.recv(4096)
            data_list = data.decode("UTF-8").split("---")
            self.x = int(data_list[0])
            self.y = int(data_list[1])
            self.flag = int(data_list[2])
            self.win = int(data_list[3])

            data_ = data_list[4]
            n = 15 * 18 - 1
            for each_data in data_:
                self.status_list[n] = int(each_data)
                n = n - 1


server = Server()
_thread.start_new_thread(server.send_data, ("senddata",))
_thread.start_new_thread(server.recevie_data, ("receviedata",))

# 游戏启动
pygame.init()
screencaption = pygame.display.set_caption('↑ ↓ ← → space')
screen = pygame.display.set_mode([400, 285])
myfont = pygame.font.Font(None, 30)
textImage = myfont.render("↑ ↓ ← → space", True, [255, 255, 255])
screen.blit(textImage, (100, 100))
clock = pygame.time.Clock()
flag = 0

server.x = 1
server.y = 1

while True:
    clock.tick(30)
    # 绘制棋盘
    screen.fill([255, 255, 255])
    for i in range(0, 15):
        pygame.draw.line(screen, [0, 0, 0], [0, i * 20], [280, i * 20], 2)
    for i in range(0, 15):
        pygame.draw.line(screen, [0, 0, 0], [i * 20, 0], [i * 20, 280], 2)

    # 绘制棋子
    for x in range(0, 15):
        for y in range(0, 15):
            if server.status_list[x * 15 + y] == 1:
                pygame.draw.circle(screen, [255, 0, 0], [2 + y * 20, 2 + x * 20], 10)
            elif server.status_list[x * 15 + y] == 2:
                pygame.draw.circle(screen, [0, 0, 0], [2 + y * 20, 2 + x * 20], 10)
            # 判断是否获胜
            # X轴的判定
            if y < 11:
                # 白棋获胜
                if server.status_list[x * 15 + y] == 1 and server.status_list[x * 15 + y + 1] == 1 and \
                        server.status_list[
                            x * 15 + y + 2] == 1 and server.status_list[x * 15 + y + 3] == 1 and server.status_list[
                    x * 15 + y + 4] == 1:
                    # print("白棋胜利")
                    server.win = 1
                    # break

                # 黑棋获胜
                if server.status_list[x * 15 + y] == 2 and server.status_list[x * 15 + y + 1] == 2 and \
                        server.status_list[
                            x * 15 + y + 2] == 2 and server.status_list[x * 15 + y + 3] == 2 and server.status_list[
                    x * 15 + y + 4] == 2:
                    # print("黑棋胜利")
                    server.win = 2
                    # break

            # 判断是否获胜
            # Y轴的判定
            if x < 11:
                if server.status_list[x * 15 + y] == 1 and server.status_list[(x + 1) * 15 + y] == 1 and \
                        server.status_list[
                            (x + 2) * 15 + y] == 1 and server.status_list[(x + 3) * 15 + y] == 1 and server.status_list[
                    (x + 4) * 15 + y] == 1:
                    # print("白棋胜利")
                    server.win = 1
                    # break

                if server.status_list[x * 15 + y] == 2 and server.status_list[(x + 1) * 15 + y] == 2 and \
                        server.status_list[
                            (x + 2) * 15 + y] == 2 and server.status_list[(x + 3) * 15 + y] == 2 and server.status_list[
                    (x + 4) * 15 + y] == 2:
                    # print("黑棋胜利")
                    server.win = 2
                    # break

            # 判断是否获胜
            # 斜着判断 正对角线
            if server.status_list[x * 15 + y] == 1 and server.status_list[(x + 1) * 15 + (y + 1)] == 1 and \
                    server.status_list[
                        (x + 2) * 15 + (y + 2)] == 1 and server.status_list[(x + 3) * 15 + (y + 3)] == 1 and \
                    server.status_list[
                        (x + 4) * 15 + (y + 4)] == 1:
                # print("白棋胜利")
                server.win = 1
                # break
            if server.status_list[x * 15 + y] == 2 and server.status_list[(x + 1) * 15 + (y + 1)] == 2 and \
                    server.status_list[
                        (x + 2) * 15 + (y + 2)] == 2 and server.status_list[(x + 3) * 15 + (y + 3)] == 2 and \
                    server.status_list[
                        (x + 4) * 15 + (y + 4)] == 2:
                # print("黑棋胜利")
                server.win = 2
                # break
            # 判断是否获胜
            # 斜着判断 反对角线
            if server.status_list[x * 15 + y] == 1 and server.status_list[(x + 1) * 15 + (y - 1)] == 1 and \
                    server.status_list[
                        (x + 2) * 15 + (y - 2)] == 1 and server.status_list[(x + 3) * 15 + (y - 3)] == 1 and \
                    server.status_list[
                        (x + 4) * 15 + (y - 4)] == 1:
                # print("白棋胜利")
                server.win = 1
                # break
            if server.status_list[x * 15 + y] == 2 and server.status_list[(x + 1) * 15 + (y - 1)] == 2 and \
                    server.status_list[
                        (x + 2) * 15 + (y - 2)] == 2 and server.status_list[(x + 3) * 15 + (y - 3)] == 2 and \
                    server.status_list[
                        (x + 4) * 15 + (y - 4)] == 2:
                # print("黑棋胜利")
                server.win = 2
                # break
    # 绘制落棋位置
    pygame.draw.circle(screen, [0, 0, 0], [2 + server.x * 20, 2 + server.y * 20], 10, 3)

    # 绘制文字 显示到谁落棋子
    if server.flag == 0:
        textImage = myfont.render("White", True, [255, 0, 0])
    else:
        textImage = myfont.render("Black", True, [0, 0, 255])
    if server.win == 1:
        textImage = myfont.render("Server Win !!!", True, [255, 0, 0])
    elif server.win == 2:
        textImage = myfont.render("Client Win !!!", True, [0, 0, 255])
    screen.blit(textImage, (290, 10))

    # 判断事件
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # 键盘事件
        if event.type == pygame.KEYDOWN:
            if server.flag == 0:
                if event.key == pygame.K_LEFT:
                    if server.x > 0:
                        server.x = server.x - 1
                if event.key == pygame.K_RIGHT:
                    if server.x < 14:
                        server.x = server.x + 1
                if event.key == pygame.K_UP:
                    if server.y > 0:
                        server.y = server.y - 1
                if event.key == pygame.K_DOWN:
                    if server.y < 14:
                        server.y = server.y + 1
                if event.key == pygame.K_SPACE:
                    if server.status_list[server.y * 15 + server.x] == 0:
                        server.status_list[server.y * 15 + server.x] = 1
                        server.flag = 1
                    # 分出胜负 重新开始游戏
                    if server.win == 1 or server.win == 2:
                        server.restart_game()
                # 让它发送数据
                server.status = 1

    # 刷新页面
    pygame.display.flip()
