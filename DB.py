#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Maker import Maker

import MySQLdb

class DB(Maker):

    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWD = "lf3Emd4R"
    DB_TYPE = "mysql"

    CREATION_TYPE = "database"


    def __init__(self, user, gitRepo):
        super().__init__()
        self.__initCursor()
        self.setUser(user)
        self.setGitRepo(gitRepo)
        self.__createDatabaseUser()

    def __del__(self):
        try:
            self.cur.close()
        except AttributeError:
            pass

    def execute(self, cmd):
        self.cur.execute(cmd)

    def getCreateName(self):
        return self.getDatabaseName()

    def getCmdToDo(self):
        return [
            self.__getCreateDatabaseCmd(),
            self.__getGrantUserCmd()
        ]

    def getDatabaseName(self):
        return "{:s}__{:s}".format(self.getDatabaseUser(), self.gitRepo.repoName)

    def getDatabaseUser(self):
        return self.user.username

    def getDatabaseUserPassword(self):
        return self.user.password

    def setUser(self, user):
        self.user = user

    def setGitRepo(self, gitRepo):
        self.gitRepo = gitRepo

    def __createDatabaseUser(self):
        if not self.__isDBUserExists():
            self.cur.execute(self.__getCreateUserCmd())

    def __isDBUserExists(self):
        self.cur.execute("SELECT user from mysql.user WHERE user={:s}".format(self.getDatabaseUser()))
        return self.cur.fetchone() == None

    def __getCreateDatabaseCmd(self):
        return "create database {:s}".format(self.getDatabaseName())

    def __getCreateUserCmd(self):
        return "create user '{:s}'@localhost identified by '{:s}'".format(self.getDatabaseUser(), )

    def __getGrantUserCmd(self):
        return "grant all on {:s}.* to '{:s}'@'localhost' identified by '{:s}'".format(self.getDatabaseName(), self.getDatabaseUser(), self.getDatabaseUserPassword())

    def __initCursor(self):
        db = MySQLdb.connect(host=self.DB_HOST, user=self.DB_USER, passwd=self.DB_PASSWD, db=self.DB_TYPE) 
        self.cur = db.cursor()

    def createChecker(self):
        self.cur.execute("SHOW DATABASES LIKE '"+ utilisateur +"';")
        return self.cur.fetchone() == None