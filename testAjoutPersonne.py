import pickle
import numpy as np

with open('bdd/personnes', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    identifiantPersonne =pp.load()

with open('bdd/questions', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    identifiantQuestion = pp.load()

with open('bdd/participation', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    matriceOrganisation = pp.load()


n = input("Combien doit-on ajouter de personne ?")

n = int(n)

for i in range(n):
    identifiantPersonne.append("test"+str(i))

m = len(identifiantQuestion) # nombre de question

#Pour chaque personne on ajoute une participation nulle à chaque question

for n in range(n):
    matriceOrganisation = np.append(matriceOrganisation, np.zeros((1, m)), axis=0)

with open('bdd/personnes', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(identifiantPersonne)

with open('bdd/participation', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(matriceOrganisation)
