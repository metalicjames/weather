import datetime
import forecast
import util
import urllib
import os

class ASOSDataset:

    def __init__(self, station, startDate, nDays):
        self.startDate = startDate
        self.periods = []

        self.checkRep()

        baseURL = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?data=tmpf&data=sknt&data=p01i&tz=Etc%2FUTC&format=onlycomma&latlon=no&missing=M&trace=T&direct=no&report_type=1&report_type=2'

        for i in range(nDays):
            forecastDate = startDate + datetime.timedelta(days=i)
            nextForecastDate = forecastDate + datetime.timedelta(days=2)
            url = baseURL + '&station=' + station + '&year1=' + str(forecastDate.year) + '&month1=' + str(forecastDate.month) + '&day1=' + str(forecastDate.day) + '&year2=' + str(nextForecastDate.year) + '&month2=' + str(nextForecastDate.month) + '&day2=' + str(nextForecastDate.day)

            f = util.getData(url)
            
            f.readline()

            y = 0

            maxTemp = -200
            minTemp = 200
            maxWind = 0
            precip = 0

            offset = 81

            for line in f:
                line = line.strip('\n')
                fields = line.split(',')
              
                fcDate = datetime.datetime.strptime(fields[1].split('+')[0], '%Y-%m-%d %H:%M')
        
                fcTemp = None
                if fields[2] != '' and fields[2] != 'M' and fields[2] != 'T':
                    fcTemp = int(round(float(fields[2])))
                
                fcWind = None
                if fields[3] != '' and fields[3] != 'M' and fields[3] != 'T':
                    fcWind = float(fields[3])
                
                fcPrecip = None
                if fields[4] != '' and fields[4] != 'M' and fields[4] != 'T':
                    fcPrecip = float(fields[4])

                y += 1
                if y > offset + 314:
                    self.periods.append(forecast.Forecast(maxTemp, minTemp, float(maxWind), float(precip)))
                    break
                if y > offset:
                    if fcDate.minute % 53 == 0:
                        if fcPrecip != None:
                            precip += fcPrecip

                        if fcTemp != None:
                            if fcTemp > maxTemp:
                                maxTemp = fcTemp

                            if fcTemp < minTemp:
                                minTemp = fcTemp

                    if fcWind != None:
                        if fcWind > maxWind:
                            maxWind = fcWind
            
            f.close()

        return

    def checkRep(self):
        if not isinstance(self.startDate, datetime.date):
            raise TypeError('start date is not a date')

    def getDataForPeriod(self, forecastDate):
        offset = (forecastDate - self.startDate).days
         
        if offset < 0:
            raise ValueError('date is before start of dataset')
        if offset >= len(self.periods):
            raise ValueError('date is after end of dataset')
        
        return self.periods[offset]

        


