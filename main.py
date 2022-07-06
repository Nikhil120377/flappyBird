import pygame
import sys
from random import random
import random

# functions

def draw_floor():
    game_screen.blit(floor, (floor_x_position, 400))
    game_screen.blit(floor, (floor_x_position + 535,400))

def create_pipe():
    random_pipe_location = random.choice(pipe_height)
    bottom_pipe = pipe.get_rect(midtop =(700,random_pipe_location ))
    top_pipe = pipe.get_rect(midbottom=(700, random_pipe_location - 100))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):

    for pipe_1 in pipes:
        if pipe_1.bottom >= 500:
            game_screen.blit(pipe,pipe_1)
        else:
            flip_pipe = pygame.transform.flip(pipe, False, True)
            game_screen.blit(flip_pipe,pipe_1)

def check_collisions(pipes):
    for pipe_1 in pipes:
        if bird_rect.colliderect(pipe_1):
            death_sound.play()
            return  False

    if bird_rect.top <= -100 or bird_rect.bottom >= 400 :
        death_sound.play()
        return  False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def bird_animation():
    new_surface = bird_frames[bird_index]
    new_bird_rect = new_surface.get_rect(center = (100,bird_rect.centery))
    return new_surface,new_bird_rect

def score_display(game_state):
    if game_state== "main_game":
        score_surface = game_font.render(f'Score : {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,30))
        game_screen.blit(score_surface,score_rect)
    if game_state =="game_over":
        score_surface = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 30))
        game_screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score : {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288,370))
        game_screen.blit(high_score_surface,high_score_rect )

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

#main code
pygame.init()
pygame.font.init()
print(pygame.font.get_fonts())

game_font = pygame.font.SysFont('gillsansextcondensed',30)

game_active = True

game_screen_width = 576
game_screen_height = 512
game_screen = pygame.display.set_mode((game_screen_width,game_screen_height))
clock = pygame.time.Clock()

gravity = 0.25
bird_movement = 0
score = 0
high_score = 0

fps = 120
bg_surface = pygame.image.load("./images/background_resize.jpg").convert()
floor = pygame.image.load("./images/ground.png").convert()
floor_x_position = 0

#bird_surface = pygame.image.load("./images/yellowbird-midflap.png").convert_alpha()
#bird_rect = bird_surface.get_rect(center = (100,88))

bird_down_flap = pygame.image.load("./images/bird_wing_down.png").convert_alpha()
bird_up_flap = pygame.image.load("./images/bird_wing_up.png").convert_alpha()
bird_frames = [bird_down_flap,bird_up_flap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,88))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe = pygame.image.load("./images/pipe-green.png").convert()
pipe_height=[200,250,300]

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

game_over_surface = pygame.image.load('./images/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (288,195))
#main loop

flap_sound = pygame.mixer.Sound("./sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("./sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("./sound/sfx_point.wav")
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active==True:
                bird_movement =  -5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active=True
                pipe_list.clear()
                bird_rect.center = (100,88)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 1:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()

    game_screen.blit(bg_surface,(0,0))
    if game_active:
        # bird
        bird_movement+=gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        game_screen.blit(rotated_bird,bird_rect)
        game_active = check_collisions(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score +=0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        game_screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')

    # floor
    floor_x_position -= 3
    draw_floor()

    if floor_x_position <=-576:
        floor_x_position=0

    pygame.display.update()
    clock.tick(fps)

