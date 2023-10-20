import pygame 
import random
import copy

pygame.init()

I_max = 11
J_max = 21

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
rotate = False
blocks = []
while game:
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

    for i in range(0, I_max):
        for j in range(0, J_max):
            pygame.draw.rect(display, grid[i][j][2], grid[i][j][1], grid[i][j][0])


    for i in range(4):
        if ((det_choice[i].x + cord_x * dx < 0) or (det_choice[i].x + cord_x * dx >= screen_x)):
            cord_x = 0
        if ((det_choice[i].y + dy >= screen_y) or (grid[int(det_choice[i].x//dx)][int(det_choice[i].y//dy) + 1][0] == 0)):
            cord_y = 0
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

                


    #передвижение по x
    for i in range(4):
        det_choice[i].x += cord_x*dx

    count += fps
    #передвижение по y
    if count > 30 * fps:
        for i in range(4):
            det_choice[i].y += cord_y*dy
        count = 0

    for i in range(4):
        detail.x = det_choice[i].x
        detail.y = det_choice[i].y
        pygame.draw.rect(display, pygame.Color("White"), detail)

    C = det_choice[2] #центр СК
    if rotate == True:
        for i in range(4):
            x = det_choice[i].y - C.y
            y = det_choice[i].x - C.x

            det_choice[i].x = C.x - x
            det_choice[i].y = C.y + y
        rotate = False

    for j in range(J_max - 1, -1, -1): #цикл по рядам снизу вверх
        count_cells = 0
        for i in range(0, I_max): #цикл по столбцам справа налево
            if grid[i][j][0] == 0:
                count_cells += 1
            elif grid[i][j][0] == 1:
                break
        if count_cells == (I_max - 1):
            for l in range(0, I_max):
                grid[l][0][0] = 1 #все ячейки первого ряда
            for k in range(j, -1, -1):
                for l in range(0, I_max):
                    grid[l][k][0] = grid[l][k-1][0]


    pygame.display.update()
    clock.tick(fps)