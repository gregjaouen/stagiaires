#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Maker import Maker

import os

class GitRepo(Maker):

    DEFAULT_GIT_DIRECTORIES = ["web", "git"]
    POST_RECEIVE = "post-receive"

    CREATION_TYPE = "git repository"

    def __init__(self, repoName, user):
        super().__init__()
        self.setRepoName(repoName)
        self.setUser(user)

    def create(self):
        super().create()
        self.__writePostReceiveHook()

    def getCreateName(self):
        return self.repoName
    
    def getCmdToDo(self):
        return [
            self.__getGitInitCmd(),
            self.__getGitCloneCmd(),
            self.__getChownReposCmd()
        ]

    def createChecker(self):
        return (not self.__isOneOfDirsExist())

    def setRepoName(self, repoName):
        self.repoName = repoName

    def setUser(self, user):
        self.user = user

    def getRepoPath(self):
        return self.__makeRepoPath(self.user.getGitPath())

    def getClonePath(self):
        return self.__makeRepoPath(self.user.getWebPath())

    def getPostReceivePath(self):
        return "{:s}/hooks/{:s}".format(self.getRepoPath(), self.POST_RECEIVE)

    def __writePostReceiveHook(self):
        ## use try block
        with open(self.getPostReceivePath(), 'w+') as f:
            f.write(self.__generatePostReceiveHook())

    def __getGitInitCmd(self):
        return self.__getCdWrapperCmd(
            self.user.getGitPath(),
            "git init --bare {:s}".format(self.getRepoPath())
        )

    def __getGitCloneCmd(self):
        return self.__getCdWrapperCmd(
            self.user.getWebPath(),
            "git clone file://{:s}".format(self.getRepoPath())
        )

    def __getChownReposCmd(self):
        out = ""
        for repo in [self.getRepoPath(), self.getClonePath()]:
            out += "chown -R {:s} {:s} && ".format(self.user.getUserAndGroup(), repo)
        return out[:-4]

    def __getCdWrapperCmd(self, dirTarget, cmd):
        return "old_dir=\"$PWD\" && cd {:s} && {:s}; cd \"$old_dir\"; old_dir=\"\"".format(dirTarget, cmd)

    def __isOneOfDirsExist(self):
        for pathToTest in [self.getRepoPath(), self.getClonePath()]:
            if os.path.exists(pathToTest):
                return True
        return False

    def __generatePostReceiveHook(self):
        out = """#!/bin/sh

while read oldrev newrev ref
do
	branch=`echo $ref | cut -d/ -f3`
	if [ "$branch" == "master" ]
	then
		GIT_WORK_TREE={:s} git checkout -f master
		echo "   /==============================="
		echo "   | DEPLOYMENT COMPLETED"
		echo "   | Target branch: $branch"
		echo "   | project folder: {:s}"
		echo "   \=============================="
	fi

done
""".format(self.getClonePath(), self.repoName)
        return out

    def __makeRepoPath(self, sourcePath):
        return "{:s}/{:s}".format(sourcePath, self.repoName)