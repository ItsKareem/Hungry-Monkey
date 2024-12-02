import pygame
import sys
import random

pygame.init()

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hungry Monkey')

platform_width = 128
platform_height = 10
platform_list = []
platform_img = pygame.image.load(f"hungry_monkey_sprites/7tree_top_sprite.png")
num_platforms = 8

floor = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)


monkey_x = int(SCREEN_WIDTH / 2)
monkey_y = SCREEN_HEIGHT - 100
gravity = 1
velocity_y = 0
monkey_size = 50
jump_power = -17
monkey = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)
is_jumping = False
monkey_img = pygame.image.load(f"hungry_monkey_sprites/2monkey_f1.png")

frame = 0
frames_left = 1000

score = 0
top_score = 0
banana_x, banana_y = int(SCREEN_WIDTH / 2), 50
banana = pygame.Rect(banana_x,banana_y, 50, 50)

DARK_GREEN = (0, 150, 0)
SKY_BLUE = (105, 186, 255)
WHITE = (255,255,255)

def draw_setting():
	pygame.draw.rect(screen, SKY_BLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

	for platform in platform_list:
		screen.blit(platform_img, platform)

	pygame.draw.rect(screen, DARK_GREEN, floor)

	if len(platform_list) == num_platforms:
		banana_img = pygame.image.load(f"hungry_monkey_sprites/1banana_sprite.png")
		screen.blit(banana_img, (banana_x,banana_y))

	score_txt = font.render(f"Banana Score: {score}", True, (255,255,255))
	screen.blit(score_txt, (10, 10))

def update_monkey():
	global monkey_x, monkey_y, velocity_y, monkey, monkey_img, platform_list,score

	velocity_y += gravity
	monkey_y += velocity_y

	key_pressed = pygame.key.get_pressed()
	if key_pressed[pygame.K_a]:
		monkey_x -= 5
	elif key_pressed[pygame.K_d]:
		monkey_x += 5
	monkey = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)

	for platform in platform_list:
		if monkey.colliderect(platform) and velocity_y > 0:
			monkey_y = platform[1] - monkey_size 
			velocity_y = 0
			if key_pressed[pygame.K_SPACE]: 
				velocity_y = jump_power
	if monkey.colliderect(floor):
		monkey_y = floor[1] - monkey_size
		velocity_y = 0
		if key_pressed[pygame.K_SPACE]:
			velocity_y = jump_power
		generate_platforms()

	sprite_frame = int((frame / 5) % 4) + 1
	if len(platform_list) == num_platforms:
		if sprite_frame == 1:
			current_sprite = f"hungry_monkey_sprites/2monkey_f1.png"
		elif sprite_frame == 2:
			current_sprite = f"hungry_monkey_sprites/0monkey_f2.png"
		elif sprite_frame == 3:
			current_sprite = f"hungry_monkey_sprites/3monkey_f3.png"
		else:
			current_sprite = f"hungry_monkey_sprites/4monkey_f4.png"
		monkey_img = pygame.image.load(current_sprite)
	if velocity_y < 0 and len(platform_list) == num_platforms:
		monkey_img = pygame.image.load(f"hungry_monkey_sprites/6monkey_jump_sprite.png")
	if monkey.colliderect(banana) and len(platform_list) == num_platforms:
		platform_list = []
		monkey_img = pygame.image.load(f"hungry_monkey_sprites/5monkey_happy.png")
		score += 1

	screen.blit(monkey_img, (monkey_x, monkey_y))

def game_over_display():
	global score

	screen.fill(SKY_BLUE)
	game_over_txt = font.render("Game Over", True, WHITE)
	score_txt = font.render(f"Your score was: {score}", True, WHITE)
	top_score_txt = font.render(f"The high score is: {top_score}",True,WHITE)
	restart_txt = font.render("Press R to restart, or Q to quit",True, WHITE)

	screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
	screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
	screen.blit(top_score_txt, (SCREEN_WIDTH // 2 - top_score_txt.get_width() // 2, SCREEN_HEIGHT // 2))
	screen.blit(restart_txt, (SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
	pygame.display.update()

	input_waiting = True
	while input_waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r: 
					input_waiting = False
					game_loop() 
				elif event.key == pygame.K_q:
					pygame.quit()
					sys.exit()

def advance_timer():
	global top_score, frames_left

	frames_left -= 1
	timer_txt = font.render(f"Time left: {frames_left}", True, (255, 255, 255))
	screen.blit(timer_txt, (10, 60))

	if frames_left <= 0:
		if score > top_score:
			top_score = score
		game_over_display()

def generate_platforms():
	current_platform_count = len(platform_list)
	while current_platform_count < num_platforms:
		platform_x = (random.randint(0, SCREEN_WIDTH - platform_width)) #random.randint(a,b) generate a random integer between a and b
		platform_y = (random.randint(80 + (current_platform_count * (SCREEN_HEIGHT - 80) // num_platforms),(80 + (current_platform_count + 1) * (SCREEN_HEIGHT - 80) // num_platforms)))
		#Create new rectangles for these platforms, and store them in platform_list
		platform_list.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))

		current_platform_count += 1

def reset_variables():
	global frames_left, score, platform_list, monkey_x, monkey_y

	frames_left = 3000
	score = 0
	platform_list = []
	generate_platforms()
	monkey_x = int(SCREEN_WIDTH / 2)
	monkey_y = SCREEN_HEIGHT - 100

def game_loop():
	global frame
  
	reset_variables()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()

		draw_setting() 
		update_monkey() 
		advance_timer() 

		pygame.display.update()
		clock.tick(30)
		frame += 1

game_loop()