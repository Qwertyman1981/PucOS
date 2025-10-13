import pygame
from HDD import HDD

class Shell:
    def __init__(self, gpu, cpu):
        self.gpu = gpu
        self.cpu = cpu
        self.hdd = HDD("Storage")
        self.output = ["Puc 2.0 (C) 2025 Puc Systems", ""]
        self.prompt = "C:\\> "
        self.input_text = ""
        self.running = True
        self.editing = False
        self.editor_content = []
        self.edit_file_name = None

    # ---------- Command helpers ----------
    def list_files(self):
        files = self.hdd.list_files()
        self.output += files if files else ["No files found."]
    
    def show_file(self, filename):
        data = self.hdd.read(filename)
        self.output.append(f"--- {filename} ---")
        self.output += data.splitlines() if data else [f"{filename} not found."]

    def edit_file(self, filename):
        data = self.hdd.read(filename)
        self.editing = True
        self.edit_file_name = filename
        self.editor_content = data.splitlines() if data else [""]
        self.output.append(f"Editing {filename}. Press ESC to save & exit editor.")

    def delete_file(self, filename):
        self.hdd.delete(filename)
        self.output.append(f"Deleted {filename}")

    def show_help(self):
        self.output += [
            "DIR - List files",
            "TYPE <file> - View file contents",
            "EDIT <file> - Edit or create text file",
            "DEL <file> - Delete file",
            "HELP - Show this help",
            "EXIT - Quit Puc 2"
        ]

    # ---------- Update & Draw ----------
    def update(self, events):
        if self.editing:
            self._editor_update(events)
        else:
            self._shell_update(events)

    def _shell_update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    cmd = self.input_text
                    self.output.append(self.prompt + cmd)
                    self.input_text = ""
                    self.cpu.execute(cmd, self)
                elif e.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif e.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.input_text += e.unicode

    def _editor_update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    # Save and exit
                    text = "\n".join(self.editor_content)
                    self.hdd.write(self.edit_file_name, text)
                    self.output.append(f"Saved {self.edit_file_name}")
                    self.editing = False
                elif e.key == pygame.K_RETURN:
                    self.editor_content.append("")
                elif e.key == pygame.K_BACKSPACE:
                    if self.editor_content[-1]:
                        self.editor_content[-1] = self.editor_content[-1][:-1]
                else:
                    self.editor_content[-1] += e.unicode

    def draw(self):
        self.gpu.clear()
        y = 10
        lines = self.editor_content if self.editing else self.output[-25:]
        for line in lines:
            self.gpu.draw_text(line, 10, y)
            y += 20
        if not self.editing:
            self.gpu.draw_text(self.prompt + self.input_text + "_", 10, y)
        self.gpu.update()
