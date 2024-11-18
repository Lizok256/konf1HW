import os

class CommandHandler:
    def __init__(self, log_path):
        self.log_path = log_path

    def handle(self, command):
        cmd_parts = command.split()
        cmd = cmd_parts[0]
        ret = 0
        if cmd == 'ls':
            return (self.ls( cmd_parts[1] if len(cmd_parts) > 1 else '.'))

        if cmd == 'cd':
            self.cd(cmd_parts[1] if len(cmd_parts) > 1 else '.' )

        if cmd == 'exit':
            return

        if cmd == 'rmdir':
            if ( len(cmd_parts) > 1):
                self.rmdir(cmd_parts[1])

        if cmd == 'du':
            ret = self.du(cmd_parts[1] if len(cmd_parts) > 1 else '.')

        if cmd == 'clear':
            os.system('clear')  # или 'cls' для Windows

        if cmd =='':
            return
        return ret


    def ls(self, path):
        # Выводим список файлов в текущей директории
        ret =[]
        files = os.listdir(path)
        for f in files:
            print(f)
            ret.append(f)
        return ret

    def cd(self, path):
        # Меняем директорию
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"No such file or directory: {path}")
        return path

    def rmdir(self, dirname):
        # Удаляет директорию
        if ( dirname != ''):
            try:
                os.rmdir(dirname)
            except Exception as e:
                print(e)

    def du(self, path):
        # Возвращает размер директории
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                fp = os.path.join(dirpath, filename)
                total_size += os.path.getsize(fp)
        print(f"Size of '{path}': {total_size} bytes")
        return total_size