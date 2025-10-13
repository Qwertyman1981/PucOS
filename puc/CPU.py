class CPU:
    def __init__(self, ram):
        self.ram = ram

    def execute(self, command_line, shell):
        parts = command_line.strip().split(" ", 1)
        if not parts or parts[0] == "":
            return
        cmd = parts[0].upper()
        arg = parts[1] if len(parts) > 1 else None

        if cmd == "DIR":
            shell.list_files()
        elif cmd == "TYPE" and arg:
            shell.show_file(arg)
        elif cmd == "EDIT" and arg:
            shell.edit_file(arg)
        elif cmd == "DEL" and arg:
            shell.delete_file(arg)
        elif cmd == "HELP":
            shell.show_help()
        elif cmd == "EXIT":
            shell.running = False
        else:
            shell.output.append(f"Bad command or file name: {cmd}")
