import math


class Model:
    def __init__(self, setPoint, actualValue):
        self.setPoint = setPoint
        self.actualValue = actualValue
        self.k1 = 0.02
        self.k2 = 0.0001
    # input: current, actual value: rpm

    def update(self, input):
        if(self.actualValue > 0):
            self.actualValue = self.actualValue - self.k1 * math.sqrt(abs(self.actualValue)) + input * abs(input) * self.k2
        else:
            self.actualValue = self.actualValue + self.k1 * math.sqrt(abs(self.actualValue)) + input * abs(input) * self.k2
        return self.actualValue
