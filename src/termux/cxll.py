#!/usr/bin/python2
#-*- encoding: utf-8 -*-
import re
import os
import subprocess
import time

def getLlUnicom(s):
    res = re.findall("剩余(\S+?)MB", s)
    return res

if __name__ == "__main__":
    os.system("termux-sms-send -n 10010 CXLL")
    time.sleep(20)
    found = False
    limit = 1
    while not found and limit < 10:
        child = subprocess.Popen(["termux-sms-inbox", "-l", str(limit)], stdout=subprocess.PIPE)
        out = child.communicate()[0]
        res = getLlUnicom(out)
        limit += 1
        if len(res) > 0:
            found = True
            os.system("termux-notification -t \"联通卡剩余流量\" -c \"%sMB\"" % str(float(res[0]) + float(res[1])))
