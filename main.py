from mecbrowser import *
from processdata import *
from calcSalary import *
import re





def main(userName = None, passWord = None, startDate = None, endDate = None, salary = None):
    if not userName: userName = raw_input("Username: ")
    if not passWord: passWord = raw_input("Password: ")

    pattern = '^20[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
    while not startDate:
        startDate = re.search(pattern, raw_input("start date (YYYY-MM-DD): "))
    startDate = startDate.group(0)
    while not endDate:
        endDate = re.search(pattern, raw_input("end date (YYYY-MM-DD): "))
    endDate = endDate.group(0)

    while not salary:
        try:
            salary = float(raw_input("salary: "))
        except:
            print "invalid salary"

    br = mecbrowser()
    login(br, userName, passWord)
    schedule = getSchedule(br, startDate, endDate, salary)
    br.close()
    print totalPay(schedule)

if __name__ == '__main__':
    main()
    raw_input("press enter to exit")

