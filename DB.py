#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Maker import Maker

import MySQLdb

class DB(Maker):

    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWD = "lf3Emd4R"
    DB_TYPE = "mysql"

    ACTION_TYPE = "database"


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

    def getActionPerformedTo(self):
        return self.getDatabaseName()

    def getCmdToCreate(self):
        return [
            self.__getCreateDatabaseCmd(),
            self.__getGrantUserCmd()
        ]

    def createChecker(self):
        self.cur.execute("SHOW DATABASES LIKE '{:s}';".format(self.getDatabaseName()))
        return self.cur.fetchone() == None

    def getCmdToDelete(self):
        return [
            self.__getDeleteDatabaseCmd(),
        ]

    def deleteChecker(self):
        return not self.createChecker()

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
        self.cur.execute("SELECT `user` from mysql.user WHERE `user` = \"{:s}\";".format(self.getDatabaseUser()))
        return self.cur.fetchone() != None

    def __getCreateDatabaseCmd(self):
        return "create database {:s};".format(self.getDatabaseName())

    def __getDeleteDatabaseCmd(self):
        return "drop database {:s};".format(self.getDatabaseName())

    def __getCreateUserCmd(self):
        return "create user '{:s}'@localhost identified by '{:s}';".format(self.getDatabaseUser(), self.getDatabaseUserPassword())

    def __getGrantUserCmd(self):
        return "grant all on {:s}.* to '{:s}'@'localhost' identified by '{:s}';".format(self.getDatabaseName(), self.getDatabaseUser(), self.getDatabaseUserPassword())

    def __initCursor(self):
        self.cur = DB.getCursor()

    @staticmethod
    def createUser(cls, user):
        DB(user, "")

    @staticmethod
    def deleteUser(cls, user):
        cur = cls.getCursor()
        cur.execute("DROP USER '{:s}'@localhost;".format(user))

    @staticmethod
    def getCursor(cls):
        db = MySQLdb.connect(host=cls.DB_HOST, user=cls.DB_USER, passwd=cls.DB_PASSWD, db=cls.DB_TYPE) 
        return db.cursor()

    @staticmethod
    def deleteAllDBWithPrefix(cls, prefix):
        cur = cls.getCursor()
        if cur.execute("SHOW DATABASES LIKE '{:s}__%';".format(prefix)) != 0:
            dbs = cur.fetchall()
            for dbRow in dbs:
                cur.execute("DROP DATABASE '{:s}';".format(dbRow[0]))
