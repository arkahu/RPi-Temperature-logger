# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 21:51:24 2017

Raspberry Pi temperature data logger. This program creates image file
(line graph) from sensor data file.

Arttu Huttunen
Oulu, Finland, 2017
"""

imageFile = '/home/pi/www-server/Day_temperature.png'
#check inputFile path below


import matplotlib as mpl
#works without display
mpl.use('Agg')
import matplotlib.dates as dt
import matplotlib.pyplot as plt
import datetime

yesterday = datetime.date.today() - datetime.timedelta(days=1)
inputFile = yesterday.strftime('/home/pi/%y-%m-%d.txt')


#Data format example
'''
17-02-27 00:00:01 22.250 17.312
17-02-27 00:02:01 22.562 17.312
17-02-27 00:04:01 22.250 17.312
'''

with open(inputFile) as fi:
    colB = [] #time objects
    colC = [] #sensor1
    colD = [] #sensor2
    for line in fi:
        cont = line.split()
        time = datetime.datetime.strptime(cont[1],'%H:%M:%S')
        colB.append(dt.date2num(time))
        colC.append(cont[2])
        colD.append(cont[3])

plt.plot_date(colB, colC,'-.', label = 'Radiator')
plt.plot_date(colB, colD, fmt='-', label = 'Air' )

#Warning: will work only until year 2100
dateText = '20' + yesterday.strftime('%y-%m-%d')
plt.title(dateText)
plt.xlabel('Time of day')
plt.ylabel('Temperature [C]')
plt.grid(True)
plt.legend()

plt.savefig(imageFile)
#plt.show()
