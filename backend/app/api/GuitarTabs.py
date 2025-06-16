class GuitarTabs:
    def __init__(self, strings = None, tabs = None):
        self.strings = strings
        self.tabs = tabs
    def add_tab(self,tab):
        self.tabs.add(tab)

    def add_string(self,string):
        self.strings.add(string)

    def set_strings(self, strings):
        self.strings = strings
class Tab:
    def __init__(self, fret, position):
        self.fret = fret
        self.position = position

    def __hash__(self):
        return hash((self.fret, self.position))  # make it hashable