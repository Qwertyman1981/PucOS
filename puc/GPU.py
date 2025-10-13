import pygame

class GPU:
    def __init__(self, width=800, height=600):
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont("consolas", 18)
        self.bg_color = (0, 0, 0)
        self.text_color = (0, 255, 0)
        self.cursor_img = pygame.image.load("cur.png").convert_alpha()
        self.cursor_pos = (0, 0)

    def clear(self):
        self.screen.fill(self.bg_color)

    def draw_text(self, text, x, y):
        surf = self.font.render(text, True, self.text_color)
        self.screen.blit(surf, (x, y))

    def draw_cursor(self, x, y):
        self.screen.blit(self.cursor_img, (x, y))

    def update(self):
        pygame.display.flip()
