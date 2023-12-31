import pygame 
import random
import copy
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

score = 0

pygame.init()
I_max = 11
J_max = 21
app = QApplication([])
button = QPushButton("жмяк")
line = QVBoxLayout()

#window = QWidget()
#window.setLayout(line)
#window.setWindowTitle("Tetris Menu")
#window.resize(400,300)
#window.show()
#lb1 = QLabel("Вітаю! Це гра під назвую тетріс. Натисни на кнопку щоб розпочати гру")
#line.addWidget(lb1,alignment=Qt.AlignCenter)
#line.addWidget(button,alignment=Qt.AlignCenter)
#button.clicked.connect(button1)
font1 =pygame.font.SysFont("Arial",30)


pygame.mixer_music.load("Music.ogg")
pygame.mixer_music.play(-1)

screen_x = 300
screen_y = 600

display = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris.Lite")

dx = screen_x/(I_max - 1)
dy = screen_y/(J_max - 1)

fps = 60
grid = []

for i in range(0, I_max):
    grid.append([])
    for j in range(0, J_max):
        grid[i].append([1])

for i in range(0, I_max):
    for j in range(0, J_max):
        grid[i][j].append(pygame.Rect(i*dx, j*dy, dx, dy))
        grid[i][j].append(pygame.Color("Gray"))


details = [
    [[-2, 0], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [-1, 0], [0, 0], [1, 0]],
    [[1, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [-1, 0]],
    [[1, 0], [1, 1], [0, 0], [-1, 0]],
    [[0, 1], [-1, 0], [0, 0], [1, 0]],
    [[-1, 1], [0, 1], [0, 0], [1, 0]],
]

det = [[],[],[],[],[],[],[]]
for i in range(0, len(details)):
    for j in range(0, 4):
        det[i].append(pygame.Rect(details[i][j][0]*dx + dx*(I_max//2), details[i][j][1]*dy, dx, dy))


detail = pygame.Rect(0, 0, dx, dy)
det_choice = copy.deepcopy(random.choice(det))

count = 0
game = True
finish = False
rotate = False
blocks = []
menu = True


while game:
    if menu:
        display.fill(pygame.Color("Black"))
        name_lb = font1.render("Вітаю в Тетрис!",True, (255,255,255))
        name_lb1 = font1.render("Нажміть на кнопку ESC ",True, (255,255,255))
        name_lb2 = font1.render("щоб розпочати! ",True, (255,255,255))
        display.blit(name_lb,(0,0))
        display.blit(name_lb1,(0,25))
        display.blit(name_lb2,(0,50))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
    if not finish and not menu:
        cord_x = 0
        cord_y = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cord_x = -1
                elif event.key == pygame.K_RIGHT:
                    cord_x = 1
                elif event.key == pygame.K_UP:
                    rotate = True

        key = pygame.key.get_pressed()
        
        if key[pygame.K_DOWN]:
            count = 31 * fps

        display.fill(pygame.Color("Black"))
        #сетка
        for i in range(0, I_max):
            for j in range(0, J_max):
                pygame.draw.rect(display, grid[i][j][2], grid[i][j][1], grid[i][j][0])

        lose_lb = font1.render("Ви програли! ",True, (255,255,255))
        for i in range(4):
            if ((det_choice[i].x + cord_x * dx < 0) or (det_choice[i].x + cord_x * dx >= screen_x)):
                cord_x = 0
            if ((det_choice[i].y + dy >= screen_y) or (grid[int(det_choice[i].x//dx)][int(det_choice[i].y//dy) + 1][0] == 0)):
                cord_y = 0
                if detail.y == 0:
                    display.blit(lose_lb,(0,250))
                    finish = True
                for i in range(4):
                    x = int(det_choice[i].x // dx)
                    y = int(det_choice[i].y // dy)
                    grid[x][y][0] = 0 
                    grid[x][y][2] = pygame.Color("White")
                detail.x = 0
                detail.y = 0
                det_choice = copy.deepcopy(random.choice(det))
                for j in range(4):
                    blocks.append(det_choice[j])          
                    detail = pygame.Rect(0, 0, dx, dy)
                    det_choice = copy.deepcopy(random.choice(det))

                    
        score_lb = font1.render("Рахунок: " +str(score), True, (255,255,255))
        lose_lb = font1.render("Ви програли! ",True, (255,255,255))
        display.blit(score_lb,(0,0))
        #display.blit(lose_lb,(150,0))
        if detail.y <= 0:
            Finish = True


        for i in range(4):
            det_choice[i].x += cord_x*dx

        count += fps

        if count > 30 * fps:
            for i in range(4):
                det_choice[i].y += cord_y*dy
            count = 0

        for i in range(4):
            detail.x = det_choice[i].x
            detail.y = det_choice[i].y
            pygame.draw.rect(display, pygame.Color("White"), detail)
        
        C = det_choice[2] 
        if rotate == True:
            for i in range(4):
                x = det_choice[i].y - C.y
                y = det_choice[i].x - C.x

                det_choice[i].x = C.x - x
                det_choice[i].y = C.y + y
            rotate = False

        for j in range(J_max - 1, -1, -1): 
            count_cells = 0
            for i in range(0, I_max): 
                if grid[i][j][0] == 0:
                    count_cells += 1
                elif grid[i][j][0] == 1:
                    break
            if count_cells == (I_max - 1):
                for l in range(0, I_max):
                    grid[l][0][0] = 1 
                score += 1
                for k in range(j, -1, -1):
                    for l in range(0, I_max):
                        grid[l][k][0] = grid[l][k-1][0]
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    finish = False
                    blocks = []
    pygame.display.update()
    clock.tick(fps)
