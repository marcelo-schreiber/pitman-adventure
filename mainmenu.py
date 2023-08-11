from cutscene import Cutscene

class MainMenu(Cutscene):
    def __init__(self):
        super().__init__()
        self.background("images/danites2.png")
        self.create_text("Press any key to start", 1000, 650, "white")
    
    def update(self):
        pass