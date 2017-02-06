# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 16:01:09 2017

Raspberry Pi temperature data logger. DS18B20+ sensors and custom shell
script data are parsed with this program.

Arttu Huttunen
Oulu, Finland, 2017
"""

import datetime

inputFile  = '/mnt/ramdisk/tempreadings_old.txt'

yesterday = datetime.date.today() - datetime.timedelta(days=1)
outputFile = yesterday.strftime('/home/pi/%y-%m-%d.txt')


#data format reference:
'''
17-02-05 16:48:01
sensor: 28-000008a260c3
8d 01 4b 46 7f ff 03 10 03 : crc=03 YES
8d 01 4b 46 7f ff 03 10 03 t=24812
sensor: 28-000008a4a333
35 01 4b 46 7f ff 0b 10 31 : crc=31 YES
35 01 4b 46 7f ff 0b 10 31 t=19312
'''

def handle_readings(a):
    sensor1 = a[3][-1] #'t=24812'
    sensor1data = sensor1[2:4], '.', sensor1[4:]
    sensor2 = (a[6][-1])
    sensor2data = sensor2[2:4], '.', sensor2[4:]

    #timestamp and data
    output = a[0]
    output.append(''.join(sensor1data))
    output.append(''.join(sensor2data))
    
    return ' '.join(output)
    

TemperatureData = []

linecnt = 0
with open(inputFile) as fi:
    T_reading = []
    for line in fi:
        T_reading.append(line.split())
        linecnt +=1
        if linecnt == 7: 
            linecnt = 0
            TemperatureData.append(handle_readings(T_reading))
            T_reading = []


TemperatureData.append('\n')
outStr = '\n'.join(TemperatureData)

with open(outputFile, "w") as fo:
    fo.write(outStr)
    
