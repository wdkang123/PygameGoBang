import pygame

# 初始化
pygame.init()
# 设置窗口标题
screencaption=pygame.display.set_caption('Gobang')
# 设置大小
screen=pygame.display.set_mode([350,285])

# 初始化字体
myfont=pygame.font.Font(None,30)
textImage=myfont.render("Hello Pygame",True,[255,255,255])
screen.blit(textImage,(100,100))

# 棋子状态0为空 1为白色 2为黑色
status_list = {}
for i in range(0, 15*18):
    status_list[i] = 0  
#print(status_list)

clock = pygame.time.Clock()

# 0 是白棋走 1是黑棋走
flag = 0
# 将要绘制的棋子的位置
movex = 1
movey = 1
while True:
    clock.tick(30)
    
    # 绘制棋盘
    screen.fill([255,255,255])
    for i in range(0, 15):
        pygame.draw.line(screen,[0,0,0],[0,i*20],[280,i*20],2)
    for i in range(0, 15):
        pygame.draw.line(screen,[0,0,0],[i*20,0],[i*20,280],2)
    
    # 绘制棋子
    for x in range(0, 15):
        for y in range(0, 15):
            if status_list[x*15 + y] == 1:
                pygame.draw.circle(screen,[255,0,0],[ 2 + y * 20,2 + x*20],10)
            elif status_list[x*15 + y] == 2:
                pygame.draw.circle(screen,[0,0,0],[ 2 + y * 20, 2 + x*20],10)
            # 判断是否获胜
            # X轴的判定
            if y < 11:
                # 白棋获胜
                if status_list[x*15 + y] == 1 and status_list[x*15 + y + 1] == 1 and status_list[x*15 + y + 2] == 1 and status_list[x*15 + y + 3] == 1 and status_list[x*15 + y + 4] == 1:
                    print("白棋胜利")
                    # break
                    
                # 黑棋获胜
                if status_list[x*15 + y] == 2 and status_list[x*15 + y + 1] == 2 and status_list[x*15 + y + 2] == 2 and status_list[x*15 + y + 3] == 2 and status_list[x*15 + y + 4] == 2:
                    print("黑棋胜利")
                    # break

            # 判断是否获胜
            # Y轴的判定
            if x < 11:
                if status_list[x*15 + y] == 1 and status_list[(x+1)*15 + y] == 1 and status_list[(x+2)*15 + y] == 1 and status_list[(x+3)*15 + y] == 1 and status_list[(x+4)*15 + y] == 1:
                    print("白棋胜利")
                    # break
                    
                if status_list[x*15 + y] == 2 and status_list[(x+1)*15 + y] == 2 and status_list[(x+2)*15 + y] == 2 and status_list[(x+3)*15 + y] == 2 and status_list[(x+4)*15 + y] == 2:
                    print("黑棋胜利")
                    # break

            # 判断是否获胜
            # 斜着判断 正对角线
            if status_list[x*15 + y] == 1 and status_list[(x+1)*15 + (y+1)] == 1 and status_list[(x+2)*15 + (y+2)] == 1 and status_list[(x+3)*15 + (y+3)] == 1 and status_list[(x+4)*15 + (y+4)] == 1:
                print("白棋胜利")
                # break
            if status_list[x*15 + y] == 2 and status_list[(x+1)*15 + (y+1)] == 2 and status_list[(x+2)*15 + (y+2)] == 2 and status_list[(x+3)*15 + (y+3)] == 2 and status_list[(x+4)*15 + (y+4)] == 2:
                print("黑棋胜利")
                # break
            # 判断是否获胜
            # 斜着判断 反对角线
            if status_list[x*15 + y] == 1 and status_list[(x+1)*15 + (y-1)] == 1 and status_list[(x+2)*15 + (y-2)] == 1 and status_list[(x+3)*15 + (y-3)] == 1 and status_list[(x+4)*15 + (y-4)] == 1:
                print("白棋胜利")
                # break
            if status_list[x*15 + y] == 2 and status_list[(x+1)*15 + (y-1)] == 2 and status_list[(x+2)*15 + (y-2)] == 2 and status_list[(x+3)*15 + (y-3)] == 2 and status_list[(x+4)*15 + (y-4)] == 2:
                print("黑棋胜利")
                # break
    # 绘制落棋位置
    pygame.draw.circle(screen,[0,0,0],[ 2 + movex*20, 2 + movey*20],10,3)
    
    # 绘制文字 显示到谁落棋子
    if flag == 0: 
        textImage=myfont.render("White",True,[255,0,0])
    else:
        textImage=myfont.render("Black",True,[0,0,255])
    screen.blit(textImage,(290,10))
	
    # 判断事件
    for event in pygame.event.get():
        # 退出事件
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        # 键盘事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if movex > 0:
                    movex = movex - 1
            if event.key == pygame.K_RIGHT:
                if movex < 14:
                    movex = movex + 1
            if event.key == pygame.K_UP:
                if movey > 0:
                    movey = movey - 1
            if event.key == pygame.K_DOWN:
                if movey < 14:
                    movey = movey + 1
            if event.key == pygame.K_SPACE:
                if flag == 0:
                    if status_list[movey * 15 + movex] == 0:
                        status_list[movey * 15 + movex] = 1
                        flag = 1
                elif flag == 1:
                    if status_list[movey * 15 + movex] == 0:
                        status_list[movey * 15 + movex] = 2
                        flag = 0

    # 刷新页面
    pygame.display.flip()
print("Done!")

