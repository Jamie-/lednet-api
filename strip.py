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
        output(self, r, g, b)
        
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
        output(self, r, g, b)
    
    def illuminate(self):
        self.mode = "illuminate"
        i = LEDnet.config["illuminate"]
        output(self, i["red"], i["green"], i["blue"])
    
    def standby(self):
        self.mode = "standby"
        output(self, 0, 0, 0)
        
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

# Output to strip over serial
def output(strip, r, g, b):
    strips = LEDnet.config["strips"]
    port = None
    number = None
    for s in strips:
        if (s["id"] == strip.getId()):
            port = s["device"]
            number = s["number"]
            break
    LEDnet.devices[port].write(bytearray([number, r, g, b]))
