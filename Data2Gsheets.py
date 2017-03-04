# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 21:49:11 2017

Raspberry Pi temperature data logger. This program uploads sensor data
to Google spreadsheet.

Arttu Huttunen
Oulu, Finland, 2017
"""
#files
inputPath = '/home/pi/%y-%m-%d.txt'
GoogleToken = '/home/pi/Hom...json'

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

yesterday = datetime.date.today() - datetime.timedelta(days=1)
inputFile = yesterday.strftime(inputPath)


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name(GoogleToken, scope)

gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet
sh = gc.open('HomeTemperatures')
wks= sh.get_worksheet(0)

#Data format example
'''
17-02-27 00:00:01 22.250 17.312
17-02-27 00:02:01 22.562 17.312
17-02-27 00:04:01 22.250 17.312
'''

#depending on your Google sheets locale, replace . with ,
with open(inputFile) as fi:
    columns = []
    for line in fi:
        columns.append(line.replace('.',',').split())

#List cells, R1C1,R1C2,R1C3,R1C4,R2C1,...
cells = wks.range(2,1,725,4)
 
i = 0
for item in columns:   
    cells[i].value = item[0]
    i +=1
    cells[i].value = item[1]
    i +=1
    cells[i].value = item[2]
    i +=1
    cells[i].value = item[3]
    i +=1

#upload all values at once
wks.update_cells(cells)  

#END

