import sys
sys.path.append('../../')
from robot import Robot

class Rob(Robot):
    def initialize(self):
        pass

    def respond(self):
        self.drive(45, 100)
        self.cannon(90, 200)
