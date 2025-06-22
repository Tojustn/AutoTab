class GuitarTabs:
    def __init__(self, height = 640, width = 640, strings = None, tabs = None):
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
    def get_strings(self):
        return self.strings

    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    def set_height(self, height):
        self.height = height
    def set_width(self, width):
        self.width = width
    def get_tabs(self):
        return self.tabs

class Tab:
    def __init__(self, fret, position, frame):
        self.fret = fret
        self.position = position
        self.frame = frame

    def get_fret(self):
        return self.fret
    def get_position(self):
        return self.position
    def get_frame(self):
        return self.frame
    def __str__(self):
        return (f"Fret: {self.fret}, Position: {self.position}, Frame: {self.frame}")

