#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import cookielib
import re
import sys
from constants import *

try:
    import mechanize
except:
    sys.exit("\n\n\tCouln't import the mechanize library, shutting down\n\n")
mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT = 100

from processdata import *


def mecbrowser():
    br = mechanize.Browser()

    cookiejar = cookielib.LWPCookieJar() 
    br.set_cookiejar(cookiejar)

    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_gzip(False)
    br.set_handle_referer(True)
    br.set_handle_refresh(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    return br


def mecopner(br, url):
    while True:
        try:
            if True:
                print "\tAttemting to open '%s'" %url

            response = br.open(url)

            if True:
                print "\tSuccessfully opened page"

            return response

        except Exception, errormsg:
            if True:
                print repr(errormsg)

            print "something went wrong, reopening %s" %url
            time.sleep(1.5)


def login(br, username, password):
    response = mecopner(br, "http://www.tidsvar.se/TS30Bonzi/login.aspx")

    br.select_form(name="form1")
    br["txtAnvandare"] = username
    br["txtLösenord"] = password
    res = br.submit()


def getSchedule(br, startDate, stopDate, salary):
    response = mecopner(br, "http://www.tidsvar.se/TS30Bonzi/planeringegen.aspx")
    schedule = []
    
    while True:
        br.select_form(name="aspnetForm")
        br["ctl00$ContentPlaceHolder1$txtStartDatum"] = startDate
        br["ctl00$ContentPlaceHolder1$txtSlutDatum"] = stopDate
        res = br.submit()

        lenbefore = len(schedule)
        schedule = addToSchedule(res, salary, schedule)
        startDate = schedule[-1][0][0]

        if lenbefore == len(schedule):
            break
        else:
            time.sleep(1)

    return schedule

    









