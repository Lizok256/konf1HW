import xml.etree.ElementTree as ET

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.root = ET.Element("log")

    def log_command(self, command):
        command_element = ET.SubElement(self.root, "command" )
        command_element.text = command


    def save_log(self):
        tree = ET.ElementTree(self.root)
        tree.write(self.log_file)