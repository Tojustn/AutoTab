class GuitarTabs:
    def __init__(self, strings = None, tabs = None):
        self.strings = strings
        self.tabs = set() 
    def add_tab(self,tab):
        self.tabs.add(tab)

    def add_string(self,string):
        self.strings.add(string)

    def set_strings(self, strings):
        self.strings = strings


class Tab:
    def __init__(self, fret, position, frame):
        self.fret = fret
        self.position = position
        self.frame = frame

    def __str__(self):
        return (f"Fret: {self.fret}, Position: {self.position}, Frame: {self.frame}")

