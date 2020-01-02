#!/usr/bin/python3
# -*- coding: utf-8 -*-

# TODO: Throw exceptions in users

from User import User
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
if p.hasActions("new", "user"):
    options = p.getOptions()
    user = User(options["username"], options["password"])
elif p.hasActions("new", "repo"):
    pass
elif p.hasActions("delete", "user"):
    pass
elif p.hasActions("delete", "repo"):
    pass
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