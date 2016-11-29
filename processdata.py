import re
from constants import *
from calcSalary import *

try:
    from bs4 import BeautifulSoup
except:
    sys.exit("\n\n\tCouln't import the BeautifulSoup4 library, shutting down\n\n")



def addToSchedule(response, salary, schedule = []):
    soup = BeautifulSoup(response, "html.parser")
    rawschedule = [re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9](.+)$', re.sub(r"(\w)([A-Z])", r"\1 \2", el.text)).group(0) for el in soup.find_all('tr', {'align': 'center'})]

    for el in rawschedule:
        shift = el[0:10], [el[10:15].replace("24", "00"), el[15:20].replace("24", "00")]
        pay = basePay(shift, salary)
        ob = calculateOB(shift)

        newPost = [shift, pay, ob]
        if not newPost in schedule:
            schedule.append(newPost)

            print shift, pay, ob

    return schedule

#date on format year-month-day "2016-08-01"
#true if date1 later than or same as date 2
def compareDates(date1, date2):
    date1 = [int(x) for x in date1.split("-")]
    date2 = [int(x) for x in date2.split("-")]

    if date1[0] > date2[0]:
        return True
    if date1[1] > date2[1]:
        return True
    if date1[2] >= date2[2]:
        return True
    return False
