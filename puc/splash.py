import pygame, sys, time, random, math
pygame.init()

# --- Window ---
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CONSOLE BOOT")
clock = pygame.time.Clock()

# --- Colors ---
BLACK = (0,0,0)
GREEN = (0,255,70)
DARK_GREEN = (0,60,0)
GLITCH_GREEN = (0,200,50)

# --- Fonts ---
font = pygame.font.SysFont("Consolas", 22, bold=True)

# --- Sounds ---
beep_sound = pygame.mixer.Sound("sounds/beep.wav")
spark_sound = pygame.mixer.Sound("sounds/spark.wav")
boot_tone = pygame.mixer.Sound("sounds/boot_tone.wav")
# Optional CRT hum
crt_hum = pygame.mixer.Sound("sounds/crt_hum.wav")
crt_hum.play(-1)  # loop background hum

# --- ASCII logo ---
logo = [
    "  ___ _   _  ___    ___  ___ ",
    " | _ \\ | | |/ __|  / _ \\/ __|",
    " |  _/ |_| | (__  | (_) \\__ \\",
    " |_|  \\___/ \\___|  \\___/|___/",
    "                              "
]

# --- Functions ---
def draw_scanlines(offset=0):
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(screen, DARK_GREEN, (0, (y+offset)%HEIGHT), (WIDTH, (y+offset)%HEIGHT))

def glitch_logo(base_logo, x, y, jitter=True):
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for line in base_logo:
        text = ""
        for c in line:
            if random.random() < 0.05:
                text += random.choice("~!@#$%^&*()_+{}[]|;:<>,.?/")
            else:
                text += c
        render = font.render(text, True, GREEN)
        if jitter:
            surf.blit(render, (x + random.randint(-3,3), y + random.randint(-2,2)))
        else:
            surf.blit(render, (x, y))
        y += 28
        if random.random() < 0.2:
            beep_sound.play()
    return surf

def barrel_distort(surface, intensity=5):
    w, h = surface.get_size()
    distorted = pygame.Surface((w,h))
    for y in range(h):
        shift = int(math.sin(y / h * math.pi) * intensity)
        distorted.blit(surface, (shift, y), area=pygame.Rect(0, y, w, 1))
    return distorted

def retro_loading_bar(x, y, width, height):
    pygame.draw.rect(screen, DARK_GREEN, (x, y, width, height), 2)
    for i in range(width):
        pygame.draw.rect(screen, GREEN, (x+2, y+2, i, height-4))
        if random.random() < 0.05:
            pygame.draw.rect(screen, GLITCH_GREEN, (x+2+i, y+2, 2, height-4))
        if i % 20 == 0:
            spark_sound.play()
        pygame.display.flip()
        pygame.time.wait(random.randint(2,5))

# --- Splash sequence ---
def splash():
    screen.fill(BLACK)
    pygame.display.flip()
    ghost_frames = []

    # --- Camera fly-in + zoom + jitter ---
    for offset in range(-250,0,5):
        screen.fill(BLACK)
        draw_scanlines(offset//2)
        y = 200 + offset
        surf = glitch_logo(logo, 250, y)
        ghost_frames.append(surf.copy())
        if len(ghost_frames) > 6:
            ghost_frames.pop(0)
        # Draw ghost frames with fading alpha
        for idx, g in enumerate(ghost_frames):
            g_alpha = int(50 * (idx+1)/len(ghost_frames))
            temp = g.copy()
            temp.set_alpha(g_alpha)
            screen.blit(temp, (0,0))
        # barrel distortion + jitter
        distorted = barrel_distort(screen, intensity=4)
        screen.blit(distorted, (random.randint(-1,1), random.randint(-1,1)))
        # letterbox cinematic bars
        pygame.draw.rect(screen, BLACK, (0,0,WIDTH,50))
        pygame.draw.rect(screen, BLACK, (0,HEIGHT-50,WIDTH,50))
        pygame.display.flip()
        pygame.time.wait(12)

    # --- Loading bar cinematic ---
    retro_loading_bar(150, HEIGHT-180, 600, 20)

    # --- Glow + CRT wave + burn-in ghost + sparks ---
    for pulse in range(60):
        alpha = min(pulse*5,255)
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        glow.fill((0,255,0, alpha))
        screen.blit(glow, (0,0))
        draw_scanlines(pulse)
        surf = glitch_logo(logo, 250, 200)
        ghost_frames.append(surf.copy())
        if len(ghost_frames) > 8:
            ghost_frames.pop(0)
        for idx, g in enumerate(ghost_frames):
            g_alpha = int(50 * (idx+1)/len(ghost_frames))
            temp = g.copy()
            temp.set_alpha(g_alpha)
            screen.blit(temp, (0,0))
        distorted = barrel_distort(screen, intensity=4)
        screen.blit(distorted, (random.randint(-2,2), random.randint(-2,2)))
        # tiny flicker sparks
        if random.random() < 0.03:
            spark = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            spark.fill((0,random.randint(180,255),0,50))
            screen.blit(spark, (0,0))
        # letterbox bars
        pygame.draw.rect(screen, BLACK, (0,0,WIDTH,50))
        pygame.draw.rect(screen, BLACK, (0,HEIGHT-50,WIDTH,50))
        pygame.display.flip()
        pygame.time.wait(15)

    # --- Play final cinematic boot tone ---
    boot_tone.play()

    # --- Blinking "Press any key" cinematic ---
    prompt = font.render("Press any key to boot...", True, GREEN)
    blink = True
    last_blink = time.time()
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_scanlines(random.randint(0,3))
        for idx, g in enumerate(ghost_frames):
            g_alpha = int(50 * (idx+1)/len(ghost_frames))
            temp = g.copy()
            temp.set_alpha(g_alpha)
            screen.blit(temp, (0,0))
        glitch_logo(logo, 250, 200)
        # blinking prompt
        if blink:
            screen.blit(prompt, (230, HEIGHT-100))
        pygame.display.flip()
        if time.time() - last_blink > 0.5:
            blink = not blink
            last_blink = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crt_hum.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        clock.tick(30)

    crt_hum.stop()  # stop background hum after splash

splash()
