import numpy as np
import random as rd
# import math

#Définition des fonctions




identifiantPersonne = ["Christophe", "Julie", "Cyprien", "Victor", "Fabien", "Jean Pierre", "Alice", "Bob", "Candice", "Damien"]

identifiantQuestion = ["Question 1", "Question 2", "Question 3", "Question 4"]

#Pour générer la matrice matriceOrganisation

n = len(identifiantPersonne)
m = len(identifiantQuestion)

matriceOrganisation = np.zeros((n,m)) #Cherchez pas à comprendre les doubles parenthèses...
matriceConfOrnagisee = np.zeros((m, 5))
#Remplissage de la matriceOrganisation

for i in range(n):
    for j in range(m):
        matriceOrganisation[i,j] = rd.randint(-1, 3) #pour tester

def ListerPersonnesInteressees(idQuestion):
    return [ j for j in range(n) if matriceOrganisation[j, idQuestion] > -1 ] #Parfois, j'aime python <3

def TirerPersonnesPourLaQuestion(idQuestion):
    listePersonne=ListerPersonnesInteressees(idQuestion)

    temp = [[listePersonne[i],matriceOrganisation[listePersonne[i], idQuestion]] for i in range(len(listePersonne))]
    temp = sorted(temp, key=lambda essai:essai[1]) #Trier en fonction du coefficient de participation

    for i in range(5):
        matriceOrganisation[temp[i][0],idQuestion] += 1

    # return [identifiantPersonne[temp[i][0]] for i in range(5)]
    return temp

for question in range(m):
    print(identifiantQuestion[question])
    print(TirerPersonnesPourLaQuestion(question))

print(matriceOrganisation)

print(TirerPersonnesPourLaQuestion(2))



