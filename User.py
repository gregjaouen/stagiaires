#!/usr/bin/python3
# -*- coding: utf-8 -*-

#TODO: Handle username verification

from Maker import Maker
from GitRepo import GitRepo
from DB import DB

import os
import crypt
import re

class User(Maker):

    DEFAULT_HOME = "/home/stagiaires"
    DEFAULT_SHELL = "/usr/bin/git-shell"
    DEFAULT_GROUP = "git"
    DEFAULT_WEB_DIRECTORY = "web"
    DEFAULT_GIT_DIRECTORY = "git"
    DEFAULT_USER_DIRECTORIES = [DEFAULT_WEB_DIRECTORY, DEFAULT_GIT_DIRECTORY]

    CREATION_TYPE = "user"

    def __init__(self, username, password):
        super().__init__()
        self.setUsername(username)
        self.setPassword(password)

    def createNewGitRepo(self, repoName):
        self.gitRepo = GitRepo(repoName, self)
        self.gitRepo.create()

    def createDBForGitRepo(self):
        self.db = DB(self, self.gitRepo)
        self.db.create()

    def setUsername(self, username):
        prog = re.compile("^[a-z][a-z0-9]{2,8}$")
        result = prog.match(username)
        if result is None:
            raise Exception("L'identifiant ne peut contenir que des lettres minuscules, des chiffres et ne peut pas dépasser 8 caratères  [a-z][a-z0-9]{2,7} ")
        self.username = username

    def setPassword(self, password):
        self.password = password

    def getCreateName(self):
        return self.username
    
    def getCmdToDo(self):
        return [
                self.__getUseradd(),
                self.__getMkdirInUser(self.DEFAULT_USER_DIRECTORIES),
                self.__getChownUserHome(),
                # self.__getChownInUser(self.DEFAULT_USER_DIRECTORIES),
                # self.__getQuota()
        ]

    def createChecker(self):
        return (not self.isHomeDirectoryExists())

    def isHomeDirectoryExists(self):
        return os.path.exists(self.getHomePath())

    def getHomePath(self):
        return "{:s}/{:s}".format(self.DEFAULT_HOME, self.username)

    def getWebPath(self):
        return self.__getHomeDirsStr([self.DEFAULT_WEB_DIRECTORY]).strip()

    def getGitPath(self):
        return self.__getHomeDirsStr([self.DEFAULT_GIT_DIRECTORY]).strip()

    def getUserAndGroup(self):
        return "{:s}:{:s}".format(self.username, self.DEFAULT_GROUP)

    def __getUseradd(self):
        return "useradd -d {:s} -g {:s} -p {:s} -s {:s} {:s}".format(
            self.getHomePath(),
            self.DEFAULT_GROUP,
            crypt.crypt(self.password, self.password[:2]), 
            self.DEFAULT_SHELL, 
            self.username)
    
    def __getMkdirInUser(self, dirList):
        return "mkdir -p{:s}".format(self.__getHomeDirsStr(dirList))

    def __getChownUserHome(self):
        return "chown -R {:s} {:s}".format(self.getUserAndGroup(), self.getHomePath())

    # def __getChownInUser(self, dirList):
    #     return "chown -R {:s}:{:s}{:s}".format(self.username, self.DEFAULT_GROUP, self.__getHomeDirsStr(dirList))

    def __getChmodFor(self, dirList):
        return "chmod ug+rwX {:s}:{:s}{:s}".format(self.username, self.DEFAULT_GROUP, self.__getHomeDirsStr(dirList))

    def __getHomeDirsStr(self, dirList):
        dirs = ""
        for name in dirList:
            dirs += " {:s}/{:s}".format(self.getHomePath(), name)
        return dirs

    def __getQuota(self):
        return "quotatool -u {:s} -bq 800M -l '950 Mb' /home".format(self.username)