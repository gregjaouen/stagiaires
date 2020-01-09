#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO: Throw exceptions in users
# TODO: Add print cmd for static usage
# TODO: Throw exceptions in static DB
# TODO: Implement Edit and List
# TODO: Implement help command and man page

from User import User
from GitRepo import GitRepo
from DB import DB
from ARGVParser import ARGVParser

PATTERN = {
    "new" : {
        "user" : [
            "username", "password"
        ],
        "repo" : [
            "username", "reponame"
        ]
    },
    "delete": {
        "user": [
            "username"
        ],
        "repo": [
            "username",
            "reponame"
        ]
    },
    "edit": {
        "user" : {
            "username": ["username"],
            "password": ["password"],
        },
        "repo" : {
            "reponame": ["reponame"]
        }
    },
    "list" : {
        "user": [],
        "repo": [
            "username"
        ] ,
        "db" : [
            "username"
        ]
    }
}

p = ARGVParser(PATTERN)
options = p.getOptions()
if p.hasActions("new", "user"):
    user = User(options["username"], options["password"])
    user.create()
    user.createDBUser()
elif p.hasActions("new", "repo"):
    user = User(options["username"], "")
    user.createNewGitRepo(options["reponame"])
    user.createDBForGitRepo()
elif p.hasActions("delete", "user"):
    user = User(options["username"], "")
    user.delete()
    DB.deleteAllDBWithPrefix(options["username"])
    DB.deleteUser(options["username"])
elif p.hasActions("delete", "repo"):
    user = User(options["username"], "")
    repo = GitRepo(options["reponame"], user)
    db = DB(user, repo)
    db.delete()
    repo.delete()
elif p.hasActions("edit", "user"):
    pass
elif p.hasActions("edit", "user", "username"):
    pass
elif p.hasActions("edit", "user", "password"):
    pass
elif p.hasActions("edit", "repo", "reponame"):
    pass
elif p.hasActions("list", "user"):
    pass
elif p.hasActions("list", "repo"):
    pass
elif p.hasActions("list", "db"):
    pass
