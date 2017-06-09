class Strip:
    
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
        self.mode = "day"
        
    def setRgb(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.mode = "day"
        # output to strip
        
    def getR(self):
        return self.r
    
    def getG(self):
        return self.g
    
    def getB(self):
        return self.b
    
    def get_mode(self):
        return self.mode
    
    def set_night(self):
        self.mode = "night"
        # output to strip