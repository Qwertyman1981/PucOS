import boot
import pygame, sys, os, time
from Keyboard import Keyboard  # make sure you have Keyboard.py

pygame.init()
pygame.display.set_caption("PUC 2 CONSOLE")

# --- Display setup ---
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Consolas", 18, bold=True)
clock = pygame.time.Clock()

# --- Colors ---
BLACK = (0, 0, 0)
GREEN = (0, 255, 70)
BORDER = (0, 50, 0)
GLOW = (0, 255, 0, 25)

# --- Keyboard ---
keyboard = Keyboard()

# --- File system ---
ROOT_PATH = "Storage"
os.makedirs(ROOT_PATH, exist_ok=True)
current_dir = ROOT_PATH

# --- Text lines ---
lines = [
    "PUC 2 CONSOLE [Build 002.5]",
    "© 2025 Puc Systems. All rights reserved.",
    "",
    "Type HELP for a list of available commands.",
    ""
]

# --- Cursor blink ---
cursor_visible = True
last_cursor_blink = time.time()

# --- Helpers ---
def get_prompt():
    relative = os.path.relpath(current_dir, ROOT_PATH)
    if relative == ".":
        relative = ""
    return f"PUC:\\{relative}>"

def draw_scanlines():
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(screen, (0, 20, 0), (0, y), (WIDTH, y))

def draw_screen():
    global cursor_visible, last_cursor_blink

    # Background and border
    screen.fill(BLACK)
    pygame.draw.rect(screen, BORDER, (0, 0, WIDTH, HEIGHT), 10, border_radius=12)

    # CRT glow
    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(glow_surface, GLOW, (0, 0, WIDTH, HEIGHT))
    screen.blit(glow_surface, (0, 0))

    # Cursor blink
    if time.time() - last_cursor_blink > 0.5:
        cursor_visible = not cursor_visible
        last_cursor_blink = time.time()

    # Render text lines
    y = 25
    for line in lines[-28:]:
        text = font.render(line, True, GREEN)
        screen.blit(text, (25, y))
        y += 22

    # Render current prompt
    input_text = f"{get_prompt()} {keyboard.get_text()}"
    text_surface = font.render(input_text, True, GREEN)
    screen.blit(text_surface, (25, y))

    if cursor_visible:
        cursor_x = text_surface.get_width() + 30
        pygame.draw.rect(screen, GREEN, (cursor_x, y + 3, 12, 18))

    draw_scanlines()
    pygame.display.flip()

def execute_command(cmd):
    global lines, current_dir
    args = cmd.split()

    if not args:
        lines.append("")
        return

    command = args[0].lower()

    if command == "help":
        lines += [
            "PUC 2 CONSOLE - COMMAND INDEX",
            "----------------------------------",
            "HELP             - Show this help list",
            "CLEAR            - Clear screen",
            "DIR              - List files/folders",
            "CD <folder>      - Change directory",
            "MKDIR <folder>   - Create a folder",
            "RMDIR <folder>   - Remove an empty folder",
            "TYPE <file>      - Display file contents",
            "WRITE <f> <txt>  - Append text to file",
            "DEL <file>       - Delete file",
            "SYSINFO          - Show system information",
            "TIME             - Display local time",
            "REBOOT           - Restart console",
            "EXIT             - Shutdown",
            "----------------------------------",
        ]

    elif command == "clear":
        lines = []

    elif command == "dir":
        try:
            files = os.listdir(current_dir)
            if not files:
                lines.append("No files or folders found.")
            else:
                lines.append(f" Directory of {os.path.relpath(current_dir, ROOT_PATH)}")
                for f in files:
                    full = os.path.join(current_dir, f)
                    if os.path.isdir(full):
                        lines.append(f" [DIR] {f}")
                    else:
                        size = os.path.getsize(full)
                        lines.append(f" {f} ({size} bytes)")
        except Exception as e:
            lines.append(f"Error: {e}")

    elif command == "cd":
        if len(args) < 2:
            lines.append("Usage: CD <folder>")
        else:
            new_path = args[1]
            if new_path == "..":
                parent = os.path.dirname(current_dir)
                if os.path.commonpath([ROOT_PATH, parent]) == ROOT_PATH:
                    current_dir = parent
                else:
                    lines.append("At root directory.")
            else:
                target = os.path.join(current_dir, new_path)
                if os.path.isdir(target):
                    current_dir = target
                else:
                    lines.append("Folder not found.")

    elif command == "mkdir":
        if len(args) < 2:
            lines.append("Usage: MKDIR <folder>")
        else:
            folder = os.path.join(current_dir, args[1])
            if not os.path.exists(folder):
                os.makedirs(folder)
                lines.append(f"Created folder '{args[1]}'")
            else:
                lines.append("Folder already exists.")

    elif command == "rmdir":
        if len(args) < 2:
            lines.append("Usage: RMDIR <folder>")
        else:
            folder = os.path.join(current_dir, args[1])
            try:
                os.rmdir(folder)
                lines.append(f"Removed folder '{args[1]}'")
            except Exception as e:
                lines.append(f"Error removing folder: {e}")

    elif command == "type":
        if len(args) < 2:
            lines.append("Usage: TYPE <filename>")
        else:
            filename = os.path.join(current_dir, args[1])
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    content = f.read().splitlines()
                    lines += content if content else ["(empty file)"]
            else:
                lines.append("File not found.")

    elif command == "write":
        if len(args) < 3:
            lines.append("Usage: WRITE <filename> <text>")
        else:
            filename = os.path.join(current_dir, args[1])
            text_to_write = " ".join(args[2:])
            with open(filename, "a") as f:
                f.write(text_to_write + "\n")
            lines.append(f"Written to {args[1]}")

    elif command == "del":
        if len(args) < 2:
            lines.append("Usage: DEL <filename>")
        else:
            filename = os.path.join(current_dir, args[1])
            if os.path.exists(filename):
                os.remove(filename)
                lines.append(f"Deleted '{args[1]}'")
            else:
                lines.append("File not found.")

    elif command == "time":
        lines.append("Local Time: " + time.strftime("%H:%M:%S"))

    elif command == "sysinfo":
        lines += [
            "PUC SYSTEM INFORMATION",
            "----------------------------------",
            "Model: PUC-2C Terminal",
            "CPU:  PUC 8086 Emulator @ 1.2MHz",
            "RAM:  512KB",
            "Firmware: Build 002.5 Stable",
            "Graphics: Text-mode display (Pygame v2.6)",
            "Storage: ./Storage/",
            "----------------------------------",
        ]

    elif command == "reboot":
        lines.clear()
        lines += [
            "PUC 2 CONSOLE [Build 002.5]",
            "© 2025 Puc Systems. All rights reserved.",
            "",
            "Reboot complete.",
            "",
        ]

    elif command == "exit":
        lines.append("System shutting down...")
        draw_screen()
        pygame.time.wait(1000)
        pygame.quit()
        sys.exit()

    else:
        lines.append(f"'{command}' is not a valid PUC 2 command.")


# --- Main loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keyboard.handle_event(event)

    cmd = keyboard.get_command()
    if cmd is not None:
        lines.append(f"{get_prompt()} {cmd}")
        execute_command(cmd)

    draw_screen()
    clock.tick(30)

pygame.quit()
sys.exit()
