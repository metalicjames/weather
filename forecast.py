class Forecast:

    def __init__(self, high, low, wind, precip):
        self.high = high
        self.low = low
        self.wind = wind
        self.precip = precip

        self.checkRep()

    def checkRep(self):
        if not isinstance(self.high, int):
            raise TypeError('High is not an integer')
        if not isinstance(self.low, int):
            raise TypeError('Low is not an integer')
        if not isinstance(self.wind, float):
            raise TypeError('Wind is not a float')
        if not isinstance(self.precip, float):
            raise TypeError('Precip is not a float')
        if self.wind < 0:
            raise ValueError('Wind is less than zero')
        if self.precip < 0:
            raise ValueError('Precip is less than zero')
        if self.high < self.low:
            raise ValueError('High is less than low')

    def __str__(self):
        return str(self.high) + '/' + str(self.low) + '/' + str(self.wind) + '/' + str(self.precip)

    def rawVector(self):
        return [self.high, self.low, self.wind, self.precip]


