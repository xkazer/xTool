#!/usr/bin/python
#coding:utf-8

import sys, os, re
import platform
from optparse import OptionParser

OPTIONS={}
ARGS={}


# search in file
def searchfile(filepath):
    global OPTIONS, ARGS

    try:
        f = open(filepath, 'r')
        data = f.read()
        try:
            udata = data.decode("gbk")
        except Exception, e:
            udata = data.decode("utf-8")
        linenum = 0
        for line in udata.splitlines():            
            linenum += 1
            if OPTIONS.regex:
                pass
            else:
                if ARGS[0] in line:
                    if OPTIONS.color:   
                        print("\033[34;1m%s\033[0m" % filepath+" line ("+str(linenum)+"):") 
                        print line.replace(ARGS[0], "\033[35;1m%s\033[0m"%ARGS[0])
                    else:
                        print filepath, "line ("+str(linenum)+"):"
                        print line
    except Exception, e:
        if OPTIONS.verbose:
            if OPTIONS.color:
                print("\033[34;1m%s\033[0m" % filepath)
                print("\033[0;31m%s\033[0m" % str(e))
            else:
                print filepath
                print str(e)

# lookup path
def lookup():
    global OPTIONS, ARGS

    for root, dirs, files in os.walk(OPTIONS.path):
        for filename in files:
            if re.compile(OPTIONS.filter).match(filename):
                filepath = os.path.join(root, filename)   
                searchfile(filepath)

def main():
    global OPTIONS, ARGS

    usage = "usage: %prog [options] str"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filter", dest="filter", default=".*",
        help="filter for filename(regex)")
    parser.add_option("-p", "--path", dest="path", default=".",
        help="set work path")
    parser.add_option("-r", "--regex", dest="regex", action="store_true")
    parser.add_option("-c", "--color", dest="color", action="store_true")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_option("-s", "--replace", dest="sstr", default="",
        help="set replace str")

    (OPTIONS, ARGS) = parser.parse_args()
    if "Windows" in platform.system():
        ARGS[0] = ARGS[0].decode("gbk")
    else:
        ARGS[0] = ARGS[0].decode("utf-8")
    lookup()



if __name__ == '__main__':
    main()