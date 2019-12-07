"""
This script takes a text file from Schedule 360 data copied from the Pocket Monthly schedule saved as "PocketMonthly.txt" and
creates a csv file that is importable into Google calendar.
"""

import re
import csv
import datetime

headings = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Location']
sched = []
subject = 'Minute Clinic'
menaul = '9640 Menaul Blvd Ne, Albuquerque, NM'
montano = '4201 Montano Rd Nw, Albuquerque, NM'
rioRancho = '1001 New Mexico Hwy 528 Se, Rio Rancho, NM'
sanMateo = '4340 San Mateo Blvd Ne. Albuquerque, NM'
cordova = '511 W Cordova Rd, Santa Fe, NM'
cerrillos = '2907 Crerrillos Rd, Santa Fe, NM'
out = csv.writer(open("mySched.csv", "w"), delimiter=',')
out.writerow(headings)

with open("PocketMonthly.txt", "rt") as contents:
    for line in contents:
        cleanedLine = line.strip()
        if cleanedLine:
            cleanedLine = re.sub(r'[\(\[].*[\)\]]', '',
                                 cleanedLine)  # Deletes everything between parenthesis including parenthesis.
            f = re.findall(('[\w\.-]+/[\d\.-]+'), cleanedLine)  # Captures format Oct/04.
            for item in f:
                if item:
                    now = datetime.datetime.now()
                    year = now.strftime('%Y')  # Uses current year, careful when schedule is going into following year.
                    month = now.month
                    item = year + '/' + item
                    item = datetime.datetime.strptime(item, '%Y/%b/%d').date()
                    schMonth = item.month
                    if schMonth < month:
                        item = item + datetime.timedelta(days=365)
                    sched.append(subject)

            f = re.findall(r"\d{1,3}a\b", cleanedLine)
            for startTime in f:
                if startTime:
                    sched.append(item)
                    startTime = startTime.strip('a')
                    startTime = str(int(startTime) * 100)
                    startTime = startTime[0:1] + ':' + startTime[1:3]
                    sched.append(startTime)

            f = re.findall((r'\d{1,3}p\b'), cleanedLine)
            for endTime in f:
                if endTime:
                    sched.append(item)
                    endTime = endTime.strip('p')
                    if int(endTime) < 100:  # Catches and corrects single digit end times (eg 2p -> 200).
                        endTime = int(endTime) * 100
                    endTime = str(int(endTime) + 1200)
                    endTime = endTime[0:2] + ':' + endTime[2:4]
                    sched.append(endTime)

            f = re.findall((r'\d{5}'), cleanedLine)
            for location in f:
                if location == '07552':
                    sched.append(rioRancho)
                elif location == '07242':
                    sched.append(montano)
                elif location == '08915':
                    sched.append(menaul)
                elif location == '08918':
                    sched.append(sanMateo)
                elif location == '10227':
                    sched.append(cerrillos)
                elif location == '09263':
                    sched.append(cordova)

        out.writerow(sched)

        sched = []
