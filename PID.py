class PID:
    output = 0
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
    def update(self, setPoint, actualValue, lastActualValue):
        # calculate output
        error = actualValue - setPoint
        pOutput = - self.p * error
        output = pOutput
        # add integral and differential terms
        return output