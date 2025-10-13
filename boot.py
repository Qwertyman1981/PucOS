import splash
import pygame, sys, time, random

pygame.init()
pygame.display.set_caption("PUC 2 CONSOLE - Boot")

# --- Screen setup ---
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Consolas", 20, bold=True)
small_font = pygame.font.SysFont("Consolas", 16)
clock = pygame.time.Clock()

# --- Colors ---
BLACK = (0, 0, 0)
GREEN = (0, 255, 70)
GRAY = (0, 100, 0)
WHITE = (200, 255, 200)

# --- Typing effect for logs ---
def type_text(text, x, y, delay=0.02):
    for i in range(len(text)):
        char = text[:i+1]
        rendered = font.render(char, True, GREEN)
        screen.blit(rendered, (x, y))
        pygame.display.flip()
        pygame.time.wait(int(delay*1000))

# --- Draw scanlines for CRT effect ---
def draw_scanlines():
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(screen, (0, 20, 0), (0, y), (WIDTH, y))

# --- Loading bar animation ---
def loading_bar(x, y, width, height):
    pygame.draw.rect(screen, GRAY, (x, y, width, height), 2)
    for i in range(width):
        pygame.draw.rect(screen, GREEN, (x+2, y+2, i, height-4))
        pygame.display.flip()
        pygame.time.wait(random.randint(2,4))

# --- Hardware checks ---
hardware_logs = [
    "POST START...",
    "Checking CPU...",
    "CPU: PUC 8086 @ 1.2MHz OK",
    "Checking RAM...",
    "RAM: 512KB OK",
    "Detecting Storage drives...",
    "Drive 0: Storage/0 OK",
    "Drive 1: Storage/1 OK",
    "Initializing Keyboard...",
    "Keyboard: OK",
    "Loading system modules...",
    "Graphics: Text-mode display OK",
    "Performing self-test...",
    "System boot successful!"
]

# --- ASCII PUC logo ---
logo = [
    "  ___ _   _  ___    ___  ___ ",
    " | _ \\ | | |/ __|  / _ \\/ __|",
    " |  _/ |_| | (__  | (_) \\__ \\",
    " |_|  \\___/ \\___|  \\___/|___/",
    "                              "
]

# --- Boot sequence ---
def boot_sequence():
    screen.fill(BLACK)
    pygame.display.flip()

    # Animated hardware logs
    y = 50
    for log in hardware_logs:
        type_text(log, 40, y, delay=0.03)
        y += 28
        draw_scanlines()
        # Optional flicker effect
        if random.random() < 0.05:
            pygame.time.wait(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Loading bar
    loading_bar(150, HEIGHT-180, 600, 20)

    # Clear screen for logo
    screen.fill(BLACK)
    y = 200
    for line in logo:
        text = font.render(line, True, GREEN)
        screen.blit(text, (250, y))
        y += 28

    # Press any key prompt with blink
    prompt = small_font.render("Press any key to enter PUC 2 CONSOLE...", True, GREEN)
    screen.blit(prompt, (230, HEIGHT-100))
    pygame.display.flip()

    blink = True
    waiting = True
    last_blink = time.time()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        # Blink effect
        if time.time() - last_blink > 0.5:
            blink = not blink
            last_blink = time.time()
            screen.fill(BLACK, (230, HEIGHT-100, 450, 30))
            if blink:
                screen.blit(prompt, (230, HEIGHT-100))
            pygame.display.flip()
        clock.tick(30)

boot_sequence()
