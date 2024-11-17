import  os
import shutil
import tarfile
import configparser
import xml.etree.ElementTree as ET
from commands import CommandHandler

from logger import Logger


class Emulator:
    def __init__(self, cfg_file):
        self.config = self.load_config(cfg_file)
        self.hostname = self.config['Settings']['hostname']
        self.vfs_path = self.config['Settings']['vfs_path']
        self.log_path = self.config['Settings']['log_path']
        self.startup_script = self.config['Settings']['startup_script']
        self.current_directory = '/tmp'
        self.command_handler = CommandHandler(self.log_path)
        self.lll = Logger(self.log_path)
        self.cur_pwd = os.getcwd()


        # Подгрузка виртуальной файловой системы
        self.load_virtual_file_system()

    def load_config(self, cfg_file):
        config = configparser.ConfigParser()
        config.read(cfg_file)
        return config

    def load_virtual_file_system(self):
        # Распаковка tar архаива
        try:
            os.mkdir("/tmp/35153", 0o700)
        except FileNotFoundError:
            print(f": Can not mkdir /tmp/35153")
        except FileExistsError:
            print('')
        with tarfile.open(self.vfs_path) as tar:
            tar.extractall(path="/tmp/35153", numeric_owner=True)



    def log_action(self, action):
       self.lll.log_command( action )

        # root = ET.Element("log")
        # action_element = ET.SubElement(root, "action")
        # action_element.text = action
        # tree = ET.ElementTree(root)
        # tree.write(self.log_path)

    def run(self):
        # Считываем команды из стартового скрипта
        try:
            with open(self.startup_script, 'r') as f:
                try:
                    os.chdir('/tmp/35153')
                except FileNotFoundError:
                    print('Can not chdir to /tmp/35153')
                for line in f:
                    self.execute_command(line.strip())

        except FileNotFoundError:
            print("No startup file found!!!\n")



        while True:
            command = input(f"{self.hostname}:{os.getcwd()} $ " )
            if command.strip().lower() == 'exit':
                break
            # comment add
            if command.strip().lower() != '':
                #self.lll.log_command(command.strip().lower() )
                self.execute_command(command.strip())
        # exit
        os.chdir(self.cur_pwd)
        self.log_action(command.strip().lower() )
        self.lll.save_log()
        try:
            os.chdir ('/tmp')
        except:
            print('Cant not chdir to tmp')
            return
        try:
            shutil.rmtree('./35153')
        except:
            print('Can not remove dir 35153/')



    def execute_command(self, command):
        self.command_handler.handle(command)
        self.log_action(command)

if __name__ == "__main__":
    emulator = Emulator('config.ini')
    emulator.run()