#!/usr/bin/python
#coding:utf-8
#author xkazer

import sys, platform


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

class XColor(object):
    BLACK       = 0x0
    BLUE        = 0x1
    GREEN       = 0x2
    RED         = 0x4
    YELLOW      = RED | GREEN
    PINK        = RED | BLUE
    CYAN        = GREEN | BLUE
    WHITE       = 0xf

    _is_windows = False

    def __init__(self):
        self._is_windows = ("Windows" in platform.system())
        if self._is_windows:
            self._mod_ctype = __import__("ctypes")
            self._std_out = self._mod_ctype.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def getWindowsForeColor(self, color):
        if self.BLACK == color:     return 0x00
        elif self.BLUE == color:    return 0x09
        elif self.GREEN == color:   return 0x0a
        elif self.RED == color:     return 0x0c
        elif self.YELLOW == color:  return 0x0e
        elif self.PINK == color:    return 0x0d
        elif self.CYAN == color:    return 0x0b
        else:                       return 0x0f

    def getWindowsBgColor(self, color):
        if self.WHITE == color:          return 0xf0
        elif self.BLUE == color:         return 0x10
        elif self.GREEN == color:        return 0x20
        elif self.RED == color:          return 0xc0
        elif self.YELLOW == color:       return 0xe0
        elif self.PINK == color:         return 0xd0
        elif self.CYAN == color:         return 0xb0
        else:                            return 0x00 

    def resetWindowsColor(self):
        self._mod_ctype.windll.kernel32.SetConsoleTextAttribute(self._std_out, Color.WHITE)

    def setWindowsColor(self, fore_color, bg_color=None):
        color = self.getWindowsForeColor(fore_color) | self.getWindowsBgColor(bg_color)
        self._mod_ctype.windll.kernel32.SetConsoleTextAttribute(self._std_out, color)


    def getLinuxForeColor(self, color):
        if self.BLACK == color:     return 40
        elif self.BLUE == color:    return 34
        elif self.GREEN == color:   return 32
        elif self.RED == color:     return 31
        elif self.YELLOW == color:  return 33
        elif self.PINK == color:    return 35
        elif self.CYAN == color:    return 36
        else:                       return 37

    def getLinuxBgColor(self, color):
        if self.WHITE == color:          return 47
        elif self.BLUE == color:         return 44
        elif self.GREEN == color:        return 42
        elif self.RED == color:          return 41
        elif self.YELLOW == color:       return 43
        elif self.PINK == color:         return 45
        elif self.CYAN == color:         return 46
        else:                            return 40 

    def setLinuxColor(self, fore_color, bg_color=None):
        if None == bg_color:
            color_attr="\033[0;"+str(self.getLinuxForeColor(fore_color))+"m"
        else:
            color_attr="\033[0;"+str(self.getLinuxForeColor(fore_color))+";"+str(self.getLinuxBgColor(bg_color))+"m"
        sys.stdout.write(color_attr)

    def resetLinuxColor(self):
        sys.stdout.write("\033[0m")

    def setColor(self, fore_color, bg_color=None):
        if self._is_windows:
            self.setWindowsColor(fore_color, bg_color)
        else:
            self.setLinuxColor(fore_color, bg_color)

    def resetColor(self):
        if self._is_windows:
            self.resetWindowsColor()
        else:
            self.resetLinuxColor()

    def println(self, msg):
        sys.stdout.write(msg)




Color = XColor()