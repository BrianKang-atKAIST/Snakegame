import pygame
import random

# 클래스 정의
class Map:
  def __init__(self, size, row, column, map_grid, food_num):
    self.size = size
    self.row = row
    self.column = column
    self.map_grid = map_grid
    self.food_num = food_num
    self.food = self.food_num
    self.foodlist = []
    self.spikelist = []
    self.score = 0
  
  def place_food(self, Snake):
    self.food = self.food_num
    food_location = [i for i in range(self.row * self.column)]
    for body in Snake.snakelist:
      food_location.remove(body[1]*self.row + body[0])
    for spike in self.spikelist:
      food_location.remove(spike[1]*self.row + spike[0])
    for food in range(self.food_num):
      food_xy = food_location[random.randint(0, len(food_location)-1)]
      food_y = food_xy // self.row
      food_x = food_xy % self.row
      self.foodlist.append((food_x, food_y))
      self.map_grid[food_y][food_x] = 1
      food_location.remove(food_xy)

  def draw_food(self):
    for food in self.foodlist:
      pygame.draw.rect(screen, color_dict['BLUE'], [food[0] * Map.size, food[1] * Map.size] + [Map.size, Map.size])

  def print_score(self):
    pass

  def init_spikes(self):
    spikelist = []
    for i in range(1, self.row):
      self.map_grid[0][i] = 4
      self.map_grid[self.column-1][i] = 4
      spikelist.append((0, i))
      spikelist.append((self.column-1, i))
    for j in range(1, self.column):
      self.map_grid[j][0] = 4
      self.map_grid[j][self.row-1] = 4
      spikelist.append((j, 0))
      spikelist.append((j, self.row-1))
    self.spikelist = sorted(list(set(spikelist)))
  
  def draw_spikes(self):
    for i in range(1, self.row-1):
      spike = [self.size*i, 0, self.size*(i+1), 0, self.size*i+self.size//2, self.size,
      self.size*i, screen_height, self.size*(i+1), screen_height, self.size*i+self.size//2, screen_height-self.size
      ]
      pygame.draw.polygon(screen, color_dict['WHITE'], [spike[:2], spike[2:4], spike[4:6]])
      pygame.draw.polygon(screen, color_dict['WHITE'], [spike[6:8], spike[8:10], spike[10:]])
    for i in range(1, self.column-1):
      spike = [0, self.size*i, 0, self.size*(i+1), self.size, self.size*i+self.size//2,
      screen_width, self.size*i, screen_width, self.size*(i+1), screen_width-self.size, self.size*i+self.size//2
      ]
      pygame.draw.polygon(screen, color_dict['WHITE'], [spike[:2], spike[2:4], spike[4:6]])
      pygame.draw.polygon(screen, color_dict['WHITE'], [spike[6:8], spike[8:10], spike[10:]])
    pygame.draw.polygon(screen, color_dict['WHITE'], [[0, self.size//4*3], [self.size//4*3, 0], [self.size, self.size]])
    pygame.draw.polygon(screen, color_dict['WHITE'], [[screen_width, self.size//4*3], [screen_width-self.size//4*3, 0], [screen_width-self.size, self.size]])
    pygame.draw.polygon(screen, color_dict['WHITE'], [[0, screen_height-self.size//4*3], [self.size//4*3, screen_height], [self.size, screen_height-self.size]])
    pygame.draw.polygon(screen, color_dict['WHITE'], [[screen_width, screen_height-self.size//4*3], [screen_width-self.size//4*3, screen_height], [screen_width-self.size, screen_height-self.size]])
  
class Snake:
  def __init__(self, head, heading, speed):
    self.head = head
    self.heading = heading
    self.speed = speed
    self.snakelist = [head, (head[0] + 1, head[1]), (head[0] + 2, head[1])]
    self.ate_food = False

  def draw_snake(self, Map):
    location = [self.snakelist[0][0] * Map.size, self.snakelist[0][1] * Map.size]
    # 머리 색을 빨갛게?
    # pygame.draw.rect(screen, color_dict['RED'], location + [Map.size, Map.size])
    # 몸통과 똑같이 ?
    pygame.draw.rect(screen, color_dict['GREEN'], location + [Map.size, Map.size])
    for body in self.snakelist[1:]:
      location = [body[0] * Map.size, body[1] * Map.size]
      pygame.draw.rect(screen, color_dict['GREEN'], location + [Map.size, Map.size])

  def move_snake(self, Map):
    # 뱀의 방향에 따라 뱀 몸 리스트를 바꿔준다.
    if self.heading == 'UP':
      if (self.head[0], self.head[1]-1) != self.snakelist[1]:
        self.snakelist.insert(0, (self.head[0], self.head[1]-1))
    elif self.heading == 'DOWN':
      if (self.head[0], self.head[1]+1) != self.snakelist[1]:
        self.snakelist.insert(0, (self.head[0], self.head[1]+1))
    elif self.heading == 'LEFT':
      if (self.head[0]-1, self.head[1]) != self.snakelist[1]:
        self.snakelist.insert(0, (self.head[0]-1, self.head[1]))
    else:
      if (self.head[0]+1, self.head[1]) != self.snakelist[1]:
        self.snakelist.insert(0, (self.head[0]+1, self.head[1]))

    self.head = self.snakelist[0]
    
    # 뱀이 길어지느냐 그대로인가
    if self.ate_food == False:
      self.snakelist.pop()
    else:
      self.ate_food = False
    
    # 이제 바뀐 뱀 리스트를 그리드에 올려준다.
    for index, body in enumerate(self.snakelist):
      if index == 0:
        Map.map_grid[body[1]][body[0]] = 2
      else:
        Map.map_grid[body[1]][body[0]] = 3

  def check_food(self, Map):
    foodlist = Map.foodlist
    for food in Map.foodlist:
      if food == self.head:
        foodlist.remove(food)
        Map.foodlist = foodlist
        Map.food -= 1
        self.ate_food = True
        break

  def get_direction(self, Map):
    nowheading = self.heading
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
      if nowheading == 'RIGHT':
        return
      self.heading = 'LEFT'
    elif key[pygame.K_RIGHT]:
      if nowheading == 'LEFT':
        return
      self.heading = 'RIGHT'
    elif key[pygame.K_DOWN]:
      if nowheading == 'UP':
        return
      self.heading = 'DOWN'
    elif key[pygame.K_UP]:
      if nowheading == 'DOWN':
        return
      self.heading = 'UP'
    
# 여러 함수 정의
def init_map(Map):
  global screen, screen_width, screen_height
  screen_width = Map.size * (Map.row)
  screen_height = Map.size * (Map.column)
  screen = pygame.display.set_mode((screen_width, screen_height + boardsize))

def draw_background():
  pygame.draw.rect(screen, color_dict['BLACK'], [0, 0, screen_width, screen_height])

def draw_grid(Map):
  for line in range(Map.row+1):
    pygame.draw.line(screen, color_dict['WHITE'], (0, line*Map.size), (screen_width, line*Map.size))
    pygame.draw.line(screen, color_dict['WHITE'], (line*Map.size, 0), (line*Map.size, screen_height))

# 주요 상수 정의
color_dict = {
  'RED' : (255, 0, 0),
  'BLACK' : (0, 0, 0),
  'YELLOW' : (255, 255, 0),
  'GREEN' : (0, 255, 0),
  'BLUE' : (0, 0, 255),
  'WHITE' : (255, 255, 255)
}
size = 30
boardsize = 100
row = 17
column = 17
map_grid = [[0] * row for i in range(column)]
food_num = 4
head = (5, 5)
heading = 'UP'
frame = 60
speed = 5 # 1초에 움직이는 픽셀 수
tock = 0 # tock이 frame 당 1씩 증가, tock이 frame/speed가 되면 한번 움직임
# 0: 빈 배경/1: 파란색 먹이/2: 빨간색 머리/3: 초록색 몸체/4: 테두리?

# pygame 시작, 객체 만들기
pygame.init()

Map = Map(size, row, column, map_grid, food_num)
Snake = Snake(head, heading, speed)

init_map(Map)
Map.init_spikes()
Map.place_food(Snake)
Map.draw_food()
pygame.display.set_caption('Snake game')

clock = pygame.time.Clock()

running = True
while running:
  clock.tick(frame)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # 배경으로 덮어씌운다.
  draw_background()
  
  # 만약 음식이 하나도 없다면 음식을 만든다.
  if Map.food == 0:
    Map.place_food(Snake)
  
  Map.draw_food()

  Snake.get_direction(Map)
  Snake.check_food(Map)
  if tock == frame/speed:
    tock = 0  
    Snake.move_snake(Map)
    print(Snake.snakelist)
    print(len(Snake.snakelist))
  tock += 1
  Snake.draw_snake(Map)

  # 만약 몸체에 중복이 생겼다면 바로 끝
  if sorted(list(set(Snake.snakelist))) != sorted(Snake.snakelist):
    running = False

  # 만약 가시에 박았다면 사망
  if Snake.head in Map.spikelist:
    running = False




  Map.draw_spikes()
  # draw_grid(Map)
  pygame.display.update()

pygame.quit()