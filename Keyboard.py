import pygame

class Keyboard:
    def __init__(self):
        self.text_buffer = ""
        self.command_ready = False
        self.last_key = None

    def handle_event(self, event):
        """Handles keyboard input from pygame events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Mark command as ready and store the current buffer
                self.command_ready = True
                self.last_key = "ENTER"
                return True

            elif event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.text_buffer = self.text_buffer[:-1]
                self.last_key = "BACKSPACE"

            elif event.key == pygame.K_SPACE:
                self.text_buffer += " "
                self.last_key = "SPACE"

            else:
                # Add normal character
                char = event.unicode
                if char != "":
                    self.text_buffer += char
                    self.last_key = char
        return False

    def get_command(self):
        """Returns the current command if ready, then resets"""
        if self.command_ready:
            command = self.text_buffer.strip()
            self.text_buffer = ""
            self.command_ready = False
            return command
        return None

    def get_text(self):
        """Returns the current text buffer (for rendering)"""
        return self.text_buffer
