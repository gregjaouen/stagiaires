#!/usr/bin/python3
# -*- coding: utf-8 -*-

import colorama
import os

colorama.init()

class Maker:
    # Pseudo abstract class
    # Child class have to implement:
    #   def getCreateName(self):
    #   def getCmdToDo(self):
    #   def createChecker(self):
    #   CREATION_TYPE

    def create(self):
        if (self.createChecker()):
            self.__printIn(colorama.Fore.GREEN, "Create {:s} {:s}: ".format(self. CREATION_TYPE, self.getCreateName()))
            for cmd in self.getCmdToDo():
                self.__printIn(colorama.Fore.YELLOW, "{:s}".format(cmd))
                # self.execute(cmd)

    def __printIn(self, color, text):
        print (color + text + colorama.Fore.WHITE, flush=True)
    
    def execute(self, cmd):
        os.system(cmd)
