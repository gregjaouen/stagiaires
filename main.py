# TODO: Throw exceptions in users

from User import User

import sys
import re

#utilisateur = input("Nom d'utilisateur:")
#mot_de_passe = input("Mot de passe:")
if len(sys.argv)<4:
    sys.exit('Usage: stagiaire.py identifiant motdepasse repository' )

utilisateur = sys.argv[1]
mot_de_passe = sys.argv[2]
repository = sys.argv[3]

prog = re.compile("^[a-z][a-z0-9]{2,8}$")
result = prog.match(utilisateur)

if result is None:
    sys.exit("L'identifiant ne peut contenir que des lettres minuscules, des chiffres et ne peut pas dépasser 8 caratères  [a-z][a-z0-9]{2,7} ")

user = User(utilisateur, mot_de_passe)
user.create()
user.createNewGitRepo(repository)
user.createDBForGitRepo()