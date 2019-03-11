import datetime
import MOS
import ASOS

import matplotlib.pyplot as plt

startDate = datetime.date(2019, 2, 1)
days = (datetime.date.today() - startDate).days

g = MOS.MOSDataset('KBNA', datetime.time(hour=12), 'GFS', startDate, days)

y = ASOS.ASOSDataset('BNA', startDate, days)

xh = []
yhs = []

xl = []
yls = []

xw = []
yws = []

xp = []
yps = []

for i in range(days):
    day = startDate + datetime.timedelta(days=i)
    gh = g.getDataForPeriod(day).rawVector()[0]
    yh = y.getDataForPeriod(day).rawVector()[0]

    gl = g.getDataForPeriod(day).rawVector()[1]
    yl = y.getDataForPeriod(day).rawVector()[1]

    gw = g.getDataForPeriod(day).rawVector()[2]
    yw = y.getDataForPeriod(day).rawVector()[2]

    gp = g.getDataForPeriod(day).rawVector()[3]
    yp = y.getDataForPeriod(day).rawVector()[3]

    xh.append(yh)
    yhs.append(gh)

    xl.append(yl)
    yls.append(gl)

    xw.append(yw)
    yws.append(gw)

    xp.append(yp)
    yps.append(gp)

plt.plot(xh, yhs, 'ro') # red: high
plt.plot(xl, yls, 'bo') # blue: low
plt.plot(xw, yws, 'go') # green: wind
plt.plot(xp, yps, 'yo') # yellow: precip

plt.xlabel('actual')
plt.ylabel('prediction')

xx = range(60)

plt.plot(xx, xx) 
plt.axis([0,60,0,60])
plt.show()
