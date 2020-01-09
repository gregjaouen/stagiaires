#!/usr/bin/python3
# -*- coding: utf-8 -*-

import colorama
import os

colorama.init()

class Maker:
    # Pseudo abstract class
    # Child class have to implement:
    #   GLOBAL
    #       def getActionPerformedTo(self):
    #       ACTION_TYPE
    #   CREATE
    #       def getCmdToCreate(self):
    #       def createChecker(self):
    #   DELETE
    #       def getCmdToDelete(self):
    #       def deleteChecker(self):

    def create(self):
        self.__crudAction(
            self.createChecker(),
            colorama.Fore.GREEN,
            "Create",
            self.getCmdToCreate()
        )

    def delete(self):
        self.__crudAction(
            self.deleteChecker(),
            colorama.Fore.RED,
            "Delete",
            self.getCmdToDelete()
        )
    
    def __crudAction(self, checker, color, actionName, cmds):
        if (checker):
            self.__printIn(color, "{:s} {:s} {:s}: ".format(actionName, self.ACTION_TYPE, self.getActionPerformedTo()))
            for cmd in cmds:
                self.__printIn(colorama.Fore.YELLOW, "{:s}".format(cmd))
                self.execute(cmd)

    def __printIn(self, color, text):
        print (color + text + colorama.Fore.WHITE, flush=True)
    
    def execute(self, cmd):
        os.system(cmd)
