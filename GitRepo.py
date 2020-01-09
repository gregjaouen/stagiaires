#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Maker import Maker

import os

class GitRepo(Maker):

    DEFAULT_GIT_ROOT = "/home"
    DEFAULT_GIT_DEPOSITE = "depots"
    DEFAULT_GIT_PUBLIC = "sites"
    DEFAULT_SERVER_USER = "www-data"

    POST_RECEIVE = "post-receive"

    ACTION_TYPE = "git repository"

    def __init__(self, repoName, user):
        super().__init__()
        self.setRepoName(repoName)
        self.setUser(user)

    def create(self):
        super().create()
        # self.__writePostReceiveHook()

    def getActionPerformedTo(self):
        return self.repoName
    
    def getCmdToCreate(self):
        return [
            self.__getGitInitCmd(),
            self.__getMkdirWebCmd(),
            self.__getChownReposCmd()
        ]

    def createChecker(self):
        return (not self.__isOneOfDirsExist())

    def setRepoName(self, repoName):
        self.repoName = repoName

    def setUser(self, user):
        self.user = user

    def getRepoPath(self):
        return self.__makePath(self.DEFAULT_GIT_DEPOSITE)

    def getWebPath(self):
        return self.__makePath(self.DEFAULT_GIT_PUBLIC)

    def getPostReceivePath(self):
        return "{:s}/hooks/{:s}".format(self.getRepoPath(), self.POST_RECEIVE)

    def __writePostReceiveHook(self):
        ## use try block
        with open(self.getPostReceivePath(), 'w+') as f:
            f.write(self.__generatePostReceiveHook())
        self.execute(self.__getChmodHookCmd())
        

    def __getChmodHookCmd(self):
        return "chmod +x {:s}".format(self.getPostReceivePath())

    def __getGitInitCmd(self):
        return "git init --bare {:s}".format(self.getRepoPath())

    def __getMkdirWebCmd(self):
        return "mkdir {:s}".format(self.getWebPath())


    def __getChownReposCmd(self):
        out = ""
        for repo in [self.getRepoPath(), self.getWebPath()]:
            out += "chown -R {user:s}:{user:s} {repo:s} && ".format(
                user=self.DEFAULT_SERVER_USER,
                repo=repo
            )
        return out[:-4] # :-4 for removing last ' && '

    # def __getCdWrapperCmd(self, dirTarget, cmd):
    #     return "old_dir=\"$PWD\" && cd {:s} && {:s}; cd \"$old_dir\"; old_dir=\"\"".format(dirTarget, cmd)

    def __isOneOfDirsExist(self):
        for pathToTest in [self.getRepoPath(), self.getWebPath()]:
            if os.path.exists(pathToTest):
                return True
        return False

    def __generatePostReceiveHook(self):
        out = """#!/bin/sh

function isSymfony() {{
    [ -f $1/bin/console ]
}}

function isComposer() {{
    [ -f $1/composer.json ]
}}

function addEnvLocal() {{
    if [ ! -f ".env.local" ]; then
        echo "APP_ENV=prod" >> ".env.local"
    fi
}}

function doComposer() {{
    if isComposer "$1"
    then
        old_dir="$PWD"
        cd "$1"
        addEnvLocal()
        composer install --no-dev --optimize-autoloader
        cd "$old_dir"
    fi
}}

function doSymfony() {{
    if isSymfony "$1"
    then
        old_dir="$PWD"
        cd "$1"
        APP_ENV=prod APP_DEBUG=0 php bin/console cache:clear
        cd "$old_dir"
    fi
}}

work_folder="{webPath:s}"

while read oldrev newrev ref
do
	branch=`echo $ref | cut -d/ -f3`
	if [ "$branch" == "master" ]
	then
		GIT_WORK_TREE="$work_folder" git checkout -f master
        doComposer "$work_folder"
        doSymfony "$work_folder"

		echo "   /==============================="
		echo "   | DEPLOYMENT COMPLETED"
		echo "   | Target branch: $branch"
		echo "   | project folder: {projectName:s}"
		echo "   \=============================="
	fi

done

""".format(webPath = self.getWebPath(), projectName = self.repoName)
        return out

    def __makePath(self, path):
        return "{source:s}/{path:s}/{user:s}/{project:s}".format(
            source=self.DEFAULT_GIT_ROOT, 
            path=path, 
            user=self.user.username, 
            project=self.repoName
        )

    def getCmdToDelete(self):
        return [
                self.__getRmdirGitCmd(),
                self.__getRmdirWebCmd(),
        ]

    def deleteChecker(self):
        return (self.__isOneOfDirsExist())

    def __getRmdirGitCmd(self):
        return "rm -Rf {:s}".format(self.getRepoPath())

    def __getRmdirWebCmd(self):
        return "rm -Rf {:s}".format(self.getWebPath())
