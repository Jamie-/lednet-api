from flask import jsonify
from data import LEDnet

class Strip:
    
    def __init__(self, id, r=0, g=0, b=0):
        self.id = id
        self.r = r
        self.g = g
        self.b = b
        self.mode = "normal"
        
    def setRgb(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.mode = "normal"
        # output to strip
        
    def getId(self):
        return self.id
        
    def getR(self):
        return self.r
    
    def getG(self):
        return self.g
    
    def getB(self):
        return self.b
    
    def get_mode(self):
        return self.mode
    
    def resume(self):
        self.mode = "normal"
        # output to strip
    
    def illuminate(self):
        self.mode = "illuminate"
        # output to strip
    
    def standby(self):
        self.mode = "standby"
        # output to strip
        
    def get_data_as_json(self):
        return jsonify(
            {
                'strip':
             {
                 'id': self.getId(),
                 'red': self.getR(),
                 'green': self.getG(),
                 'blue': self.getB(),
                 'mode': self.get_mode()
             }
            }
        )
