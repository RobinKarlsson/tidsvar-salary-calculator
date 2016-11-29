from constants import *
import calendar

def basePay(shift, salary):
    date = shift[0]
    startTime = shift[1][0]
    endTime = shift[1][1]

    startYear = int(date[0:4])
    startHour = int(startTime.split(":")[0])
    startMinute = int(startTime.split(":")[1])
    endHour = int(endTime.split(":")[0])
    endMinute = int(endTime.split(":")[1])

    if endHour < startHour:
        endHour += 24

    if startMinute == endMinute:
        minutesWorked = 0
    else:
        minutesWorked = endMinute - startMinute
        if minutesWorked >= 60:
            endHour += 1
            minutesWorked -= 60

    hoursWorked = endHour - startHour

    basepay = salary * float(hoursWorked) + float(minutesWorked) * salary / 60

    return basepay


def calculateOB(shift):
    ob = 0
    date = shift[0].split("-")
    weekday = calendar.weekday(int(date[0]), int(date[1]), int(date[2])) #monday = 0, sunday = 6

    date = shift[0]
    startTime = shift[1][0]
    endTime = shift[1][1]

    startHour = int(startTime.split(":")[0])
    startMinute = int(startTime.split(":")[1])
    endHour = int(endTime.split(":")[0])
    endMinute = int(endTime.split(":")[1])

    if startMinute == endMinute:
        minutesWorked = 0
    else:
        minutesWorked = endMinute - startMinute
        if minutesWorked >= 60:
            endHour += 1
            minutesWorked -= 60

    startYear = int(date[0:4])
    endYear = startYear
    startMonth = int(date[5:7])
    startDay = int(date[8:10])
    endDay = startDay
    endMonth = startMonth

    if endHour < startHour:
        endDay += 1

        if endDay > calendar.monthrange(startYear, startMonth)[1]:
            endDay = 1
            endMonth += 1

            if endMonth > 12:
                endMonth = 1
                endYear += 1

    if startMinute != 0:
        minutes = 60 - startMinute
        ob += float(minutes) * obPayHour(startYear, startMonth, startDay, startHour) / 60

    if endMinute != 0:
        ob += float(endMinute) * obPayHour(endYear, endMonth, endDay, endHour) / 60

    x = startHour
    while True:
        if x == endHour:
            break

        ob += obPayHour(startYear, startMonth, startDay, x)

        x += 1
        if x == 24:
            x = 0
            startDay += 1

            if startDay > calendar.monthrange(startYear, startMonth)[1]:
                startDay = 1
                startMonth += 1

                if startMonth > 12:
                    startMonth = 1
                    startYear += 1
    return ob

#ints year, month, day, start hour
def obPayHour(year, month, day, hour):
    weekday = calendar.weekday(year, month, day)
    ob = 0

    if weekday > 4:
        ob = obHelg
    elif weekday == 4 and hour >= helgStart[1]:
        ob = obHelg
    elif weekday == 0 and hour < helgEnd[1]:
        ob = obHelg
    else:
        if hour >= 19:
            ob = obKvall
        if hour in range(nattStart, 25) + range(nattEnd):
            ob = obNatt

    for date in annanhelgBetween:
        startDate = date[0]
        startTime = date[1]
        endDate = date[2]
        endTime = date[3]

        if month >= startDate[1] and month <= endDate[1]:
            if day > startDate[0] and day < endDate[0]:
                ob = obHelg
            elif day == startDate[0]:
                if hour >= startTime:
                    ob = obHelg
            elif day == endDate[0]:
                if hour < endTime:
                    ob = obHelg

    for date in storhelgBetween:
        startDate = date[0]
        startTime = date[1]
        endDate = date[2]
        endTime = date[3]

        if month >= startDate[1] and month <= endDate[1]:
            if day > startDate[0] and day < endDate[0]:
                ob = obStorhelg
            elif day == startDate[0]:
                if hour >= startTime:
                    ob = obStorhelg
            elif day == endDate[0]:
                if hour < endTime:
                    ob = obStorhelg

    return ob

def totalPay(schedule):
    pay = 0
    
    for el in schedule:
        pay += el[1] + el[2]

    return pay
