from flask import jsonify

class Strip:
    
    def __init__(self, name, r=0, g=0, b=0):
        self.name = name
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
        
    def getName(self):
        return self.name
        
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
        
    def get_data_as_json(self):
        return jsonify(
            {
                'strip':
             {
                 'name': self.getName(),
                 'red': self.getR(),
                 'green': self.getG(),
                 'blue': self.getB(),
                 'mode': self.get_mode()
             }
            }
        )
