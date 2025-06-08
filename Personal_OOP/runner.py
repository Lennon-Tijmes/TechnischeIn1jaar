import pygame
import sys
import time
import random # My Favorite

from leg_problem import Leg_Problem

pygame.init()
size = WIDTH, HEIGHT = 650, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Leg Shocker")

normalFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0 , 0)
GREEN = (0, 200, 0)
GRAY = (220, 220, 220)

clock = pygame.time.Clock()

leg = Leg_Problem(sleep_time=30)
last_random_shock = time.time()

input_active = False
input_text = ''

ai_message = ''

buttons = {
    "sit": pygame.Rect(470, 60, 100, 40),
    "stand": pygame.Rect(75, 200, 150, 40),
    "shock": pygame.Rect(450, 200, 100, 40),
    "auto_shock": pygame.Rect(50, 260, 200, 40),
    "ai": pygame.Rect(450, 260, 100, 40)
}

def draw():
    screen.fill(WHITE)

    # Here is where you can input the time
    box_color = (0, 150, 255) if input_active else GRAY
    pygame.draw.rect(screen, box_color, (160, 60, 250, 40), 2)
    # Yes, the spaces after sit time is to make sure it looks nice.
    input_surf = normalFont.render(f"Sit Time:    {input_text}", True, BLACK)
    screen.blit(input_surf, (25, 60))

    # Displayin da timah
    status = "It do be numb" if leg.remaining_time <= 0 else f"{int(leg.remaining_time)}s left"
    status_color = RED if leg.remaining_time <= 0 else BLACK
    timer_surf = largeFont.render(status, True, status_color)
    screen.blit(timer_surf, (WIDTH // 2 - timer_surf.get_width() // 2, 120))

    # Clickity Clacks
    for label, rect in buttons.items():
        button_label = label
        if label == "stand":
            button_label = "SIT DOWN" if leg.standing else "STAND UP"
        if label == "auto_shock":
            color = (0, 150, 250)
        elif label == "ai":
            color = (200, 150, 255)
        else:
            color = GREEN
        pygame.draw.rect(screen, color, rect)

        txt = normalFont.render(button_label.upper(), True, BLACK)
        text_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, text_rect)

    # Auto Shcoker status
    auto_status = "Auto-shock: ON" if leg.auto_shocker else "Auto-shock: OFF"
    auto_surf = normalFont.render(auto_status, True, BLACK)
    screen.blit(auto_surf, (10, 10))

    # for the ai message
    if ai_message:
        msg_surf = normalFont.render(f"AI: {ai_message}", True, (100, 0, 200))
        screen.blit(msg_surf, (20, HEIGHT - 40))

    pygame.display.flip()


sit_time_set = False # otherwise it resets

# Now for the game
while True:
    if sit_time_set:
        leg.update_time()

    if leg.auto_shocker and leg.remaining_time <= 0:
        leg.shock()
    
    if leg.auto_shocker and time.time() - last_random_shock >= 1:
        if random.random() < 0.05:
            leg.shock()
        last_random_shock = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 150 <= event.pos[0] <= 350 and 50 <= event.pos[1] <= 90:
                input_active = True
            else: 
                input_active = False
        
            if buttons["sit"].collidepoint(event.pos):
                try:
                    seconds = int(input_text)
                    leg.sleep_time = seconds
                    leg.remaining_time = seconds
                    leg.start_time = time.time()
                    sit_time_set = True
                    leg.sit()
                except ValueError:
                    pass

            elif buttons["stand"].collidepoint(event.pos):
                if leg.standing:
                    leg.sit()
                else:
                    leg.stand()

            elif buttons["shock"].collidepoint(event.pos):
                leg.shock()

            elif buttons["auto_shock"].collidepoint(event.pos):
                leg.toggle_auto_shock()

            elif buttons["ai"].collidepoint(event.pos):
                print("[DEBUGERINO] AI button clicked")
                ai_message = leg.get_suggestion()
        
        elif event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                input_active = False
            else:
                if event.unicode.isdigit() and len(input_text) < 14:
                    input_text += event.unicode
    
    if leg.auto_shocker and leg.remaining_time <= 0:
        leg.shock()

    draw()
    clock.tick(10)