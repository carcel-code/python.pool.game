#imports
import pygame
import math

#pygame is intiated
pygame.init()

#Visuals:

#basic settings
WIDTH, HEIGHT = 900, 500 # window size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Pool Game_ECE160") #title of game
clock = pygame.time.Clock() #creates a clocked controled by FPS
FPS = 60

#settings
LEFT, RIGHT = 70, WIDTH - 70
TOP, BOTTOM = 50, HEIGHT - 50
BALL_RADIUS = 12
FRICTION = 0.99
MIN_SPEED = 0.01

#colors im too lazy to pick colors rn sooooo
table_boarder = (50, 150, 50) #sets the boarder
#color of the balls
green =  (0, 150, 0)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 225)
black = (0,0,0)

#constants
ball_radius = 12 #balls radius
friction = 0.99 #slows down the ball
cue_power_multiplier = 0.12 #controls the strength of the shots
min_speed = 0.01 #stops the ball completely

#table boundaries
left_bound = 70
right_bound = width - 70 
top_bound = 50 
bottom = bound = height - 50

#pockets 

pocket_radius = 22 
POCKETS = [
    #3 pockets on top
    (LEFT_BOUND, TOP_BOUND),
    ((LEFT_BOUND + RIGHT_BOUND) // 2, TOP_BOUND),
    (RIGHT_BOUND, TOP_BOUND),
    #3 pockets on bottom
    (LEFT_BOUND, BOTTOM_BOUND),
    ((LEFT_BOUND + RIGHT_BOUND) // 2, BOTTOM_BOUND),
    (RIGHT_BOUND, BOTTOM_BOUND)
]

#the balls

#the ball itself 
class Ball: 
    def __init__(self, x, y, color, is_cue=False):
        self.x = x         #Balls X Position
        self.y = y         #Balls Y Position
        self.vx = 0        #Velocity in X direction
        self.vy = 0        #Velocity in Y direction
        self.color = color  #Color of ball
        self.is_cue = is_cue #cue ball
        self.alive = True #still in game

#the pool table
def draw_table():
    screen.fill(GREEN)

def draw_ball(b):
    pygame,draw.circle(screen, b.color, (int(b.x), int(b.y)), BALL_RADIUS)

def handle_input(cue_ball):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    # Vector from cue ball to mouse
    dx = mouse_x - cue_ball.x
    dy = mouse_y - cue_ball.y
    angle = math.atan2(dy, dx)  # direction of shot
    
    # Draw cue stick
    cue_length = 80
    cue_end_x = cue_ball.x - math.cos(angle) * cue_length
    cue_end_y = cue_ball.y - math.sin(angle) * cue_length
    pygame.draw.line(screen, white, (cue_ball.x, cue_ball.y), (cue_end_x, cue_end_y), 4)

if pygame.mouse.get_pressed()[0]:  # left click
        power = math.hypot(dx, dy) * cue_power_multiplier
        cue_ball.vx = math.cos(angle) * power
        cue_ball.vy = math.sin(angle) * power

def move_ball(b):
    b.x += b.vx
    b.y += b.vy
    b.vx *= FRICTION; b.vy *= FRICTION
    if abs(b.vx) < MIN_SPEED: b.vx = 0
    if abs(b.vy) < MIN_SPEED: b.vy = 0
    #bounce code
    if b.x-BALL_RADIUS<LEFT or b.x+BALL_RADIUS>RIGHT: b.vx*=-1
    if b.y-BALL_RADIUS<TOP or b.y+BALL_RADIUS>BOTTOM: b.vy*=-1

#ball collision
def ball_collision(b1,b2):
    dx, dy = b2.x-b1.x, b2.y-b1.y
    dist = math.hypot(dx,dy)
    if dist < 2*BALL_RADIUS:
        nx, ny = dx/dist, dy/dist
        rel_vel = (b1.vx-b2.vx)*nx + (b1.vy-b2.vy)*ny
        if rel_vel > 0: return
        impulse = 2*rel_vel/2
        b1.vx -= impulse*nx; b1.vy -= impulse*ny
        b2.vx += impulse*nx; b2.vy += impulse*ny
        overlap = 2*BALL_RADIUS - dist
        b1.x -= nx*overlap/2; b1.y -= ny*overlap/2
        b2.x += nx*overlap/2; b2.y += ny*overlap/2



