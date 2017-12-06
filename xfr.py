#!/usr/bin/python
#coding:utf-8

import sys, os, re
import platform
import logging, traceback
from optparse import OptionParser

OPTIONS={}
ARGS={}


# search in file
def searchfile(filepath):
    global OPTIONS, ARGS, gl_color

    if 0 == len(ARGS):
        if OPTIONS.color: gl_color.setColor(gl_color.BLUE)
        print filepath
        if OPTIONS.color: gl_color.resetColor()
        return
    else:
        if "Windows" in platform.system():
            ARGS[0] = ARGS[0].decode("gbk")
        else:
            ARGS[0] = ARGS[0].decode("utf-8")

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
                match_obj = re.search(ARGS[0], line)
                if None == match_obj: continue
                (pos, end) = match_obj.span()
            else:
                pos = line.find(ARGS[0])
                if -1 == pos: continue
                end = pos + len(ARGS[0])

            logging.debug("searchfile->result: ("+str(pos)+", "+str(end)+")")
            if OPTIONS.color:
                gl_color.setColor(gl_color.BLUE)
                gl_color.println(filepath)               
                print " line ("+str(linenum)+"):"
                gl_color.resetColor()
                gl_color.println(line[0:pos])                
                gl_color.setColor(gl_color.RED)
                gl_color.println(line[pos:end])
                gl_color.resetColor()
                print line[end:]
            else:
                print filepath, "line ("+str(linenum)+"):"
                print line
    except Exception, e:
        if OPTIONS.verbose:
            if OPTIONS.color:
                gl_color.setColor(gl_color.BLUE)
                print filepath
                gl_color.setColor(gl_color.RED)
                print str(e)
                gl_color.resetColor()
            else:
                print filepath
                print str(e)

# lookup path
def lookup():
    global OPTIONS, ARGS

    logging.debug("lookup->path:"+OPTIONS.path)
    for root, dirs, files in os.walk(OPTIONS.path):
        for filename in files:
            if re.compile(OPTIONS.filter).match(filename):
                filepath = os.path.join(root, filename)   
                searchfile(filepath)

def main():
    global OPTIONS, ARGS, gl_color

    logging.basicConfig(level=logging.WARN)
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

    try:
        (OPTIONS, ARGS) = parser.parse_args()
        logging.debug("enter->options:"+str(OPTIONS))
        logging.debug("enter->args:"+str(ARGS))
        if OPTIONS.color:
            try:
                color_mod = __import__("xcolor")
                gl_color = color_mod.Color
            except Exception,e:
                logging.warn("load xcolor failed:"+str(e))
                OPTIONS.color = False
        lookup()
    except Exception, e:
        parser.print_usage()
        logging.warn("parser->err:"+str(e))
        logging.warn("parser->"+traceback.format_exc())
        sys.exit(0)
    



if __name__ == '__main__':
    main()