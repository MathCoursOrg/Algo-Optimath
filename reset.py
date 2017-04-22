import pickle
import numpy as np

personnes = ['Christophe', 'Julie', 'Cyprien','Nicolas', 'Fabien', 'Jean-Michel', 'Tarte', 'Poire', 'Banane', 'Anne', 'Norman']
questions = ['Comment on fait des enfants ?', 'Comment organiser les débats ?']

n = len(personnes)
m = len(questions)
participation = np.zeros((n,m)) #Tout le monde est intéressé par toutes les questions

with open('bdd/personnes', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(personnes)

with open('bdd/questions', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(questions)

with open('bdd/participation', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(participation)

