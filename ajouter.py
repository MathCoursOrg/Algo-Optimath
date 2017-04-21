import pickle

with open('bdd/personnes', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    identifiantPersonne =pp.load()

with open('bdd/questions', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    identifiantQuestion = pp.load()

with open('bdd/participation', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    matriceOrganisation = pp.load()

personneAjout = []
questionAjout = []

identifiantQuestion += questionAjout
identifiantPersonne += personneAjout



