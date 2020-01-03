#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO: Throw exceptions in users

from User import User
from GitRepo import GitRepo
from ARGVParser import ARGVParser

# import sys
# #utilisateur = input("Nom d'utilisateur:")
# #mot_de_passe = input("Mot de passe:")
# if len(sys.argv)<4:
#     sys.exit('Usage: stagiaire.py identifiant motdepasse repository' )

# utilisateur = sys.argv[1]
# mot_de_passe = sys.argv[2]
# repository = sys.argv[3]

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
elif p.hasActions("delete", "user"):
    user = User(options["username"], options["password"])
    user.delete()
elif p.hasActions("delete", "repo"):
    user = User(options["username"], "")
    repo = GitRepo(options["reponame"], user)
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

# user = User(utilisateur, mot_de_passe)
# user.create()
# user.createNewGitRepo(repository)
# user.createDBForGitRepo()