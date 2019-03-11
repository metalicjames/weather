import datetime
import forecast
import util
import urllib
import os

class MOSDataset:

    def __init__(self, station, run, model, startDate, nDays):
        self.startDate = startDate
        self.run = run
        self.model = model
        self.periods = []

        self.checkRep()

        baseURL = 'https://mesonet.agron.iastate.edu/mos/csv.php'

        for i in range(nDays):
            forecastDate = startDate + datetime.timedelta(days=i)
            modelRun = datetime.datetime.combine(forecastDate - datetime.timedelta(days=1),
                                                 self.run)

            runText = modelRun.strftime('%Y-%m-%d %H:%M')
            url = baseURL + '?station=' + station + '&runtime=' + runText + '&model=' + model

            f = util.getData(url)
            
            f.readline()

            y = 0

            if self.run.hour == 0:
                offset = 8
            if self.run.hour == 6:
                offset = 6
            if self.run.hour == 12:
                offset = 4
            if self.run.hour == 18:
                offset = 2

            maxTemp = -200
            minTemp = 200
            maxWind = 0
            precip = 0

            for line in f:
                fields = line.split(',')
              
                fcDate = datetime.datetime.strptime(fields[3].split('+')[0], '%Y-%m-%d %H:%M:%S')
        
                fcTemp = None
                if fields[5] != '':
                    fcTemp = int(fields[5])
                
                fcWind = 0
                if fields[9] != '':
                    fcWind = float(fields[9])
                
                fcPrecip = 0
                if fields[12] != '':
                    fcPrecip = float(fields[12])

                y += 1
                if y > offset + 8:
                    self.periods.append(forecast.Forecast(maxTemp, minTemp, float(maxWind), float(precip)))
                    break
                if y > offset:
                    if fcDate.hour % 6 == 0:
                        precip += fcPrecip

                    if fcTemp != None:
                        if fcTemp > maxTemp:
                            maxTemp = fcTemp

                        if fcTemp < minTemp:
                            minTemp = fcTemp

                    if fcWind > maxWind:
                        maxWind = fcWind
            
            f.close()

        return

    def checkRep(self):
        if not isinstance(self.startDate, datetime.date):
            raise TypeError('start date is not a date')
        if not isinstance(self.run, datetime.time):
            raise TypeError('run is not a time')
        if self.model != "GFS" and self.model != "NAM":
            raise ValueError('model is not GFS or NAM')
        if self.run.hour != 0 and self.run.hour != 6 and self.run.hour != 12 and self.run.hour != 18:
            raise ValueError('models run at 0, 6, 12, or 18 hours')
        if self.run.minute != 0:
            raise ValueError('models run on the hour')

    def getDataForPeriod(self, forecastDate):
        offset = (forecastDate - self.startDate).days
         
        if offset < 0:
            raise ValueError('date is before start of dataset')
        if offset >= len(self.periods):
            raise ValueError('date is after end of dataset')
        
        return self.periods[offset]
