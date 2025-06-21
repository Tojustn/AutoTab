class GuitarTabs:
    def __init__(self, height, width, strings = None, tabs = None):
        self.strings = strings
        self.tabs = set() 
        self.height = height
        self.width = width
    def add_tab(self,tab):
        self.tabs.add(tab)

    def add_string(self,string):
        self.strings.add(string)

    def set_strings(self, strings):
        self.strings = strings

    def set_height(self, height):
        self.height = height
    def set_width(self, width):
        self.width = width

class Tab:
    def __init__(self, fret, position, frame):
        self.fret = fret
        self.position = position
        self.frame = frame

    def __str__(self):
        return (f"Fret: {self.fret}, Position: {self.position}, Frame: {self.frame}")

