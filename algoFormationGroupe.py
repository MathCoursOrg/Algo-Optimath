# Voici la version actuelle du code de l'algorithme de formation des groupes de débats.
# Pour l'instant, l'algorithme fonctionne sans erreur.

# Listes des fonctionnalités implémentées:

# - On peut assigner 5 personnes différentes pour chaque questions

# - On sélectionne les personnes selon leur participation (globale) (les premières
# tirées sont celles qui ont le moins participé)

# -Marche quelque soit le  nombre de personne ou le nombre de question. (s'il n'y a pas assez de
# personne, la matrice contient des 0)

#TODO: Cet algorithme «prioritarise» d'une certaine façon la question 1,
# puisqu'il assigne les personnes d'abord pour la question 1 puis les marquent
# comme non disponible. Est-ce raisonnable ? => résolu, les questions sont tirées au sort

#TODO: On suppose dans le programme qu'il y a nombredepersonne > 5*nombredequestions, car l'algorithme formera
#des groupes de 5 personnes pour chaque question de façon indépendante

#TODO: il est possible qu'il y ait des groupes formés de moins de 5 personnes si la condition ci dessus n'est pas réalisée


import pickle

import numpy as np
import random as rd
import math


#OUVERTURE DE LA "BASE DE DONNÉE"
with open('bdd/personnes', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    identifiantPersonne =pp.load()

with open('bdd/questions', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    identifiantQuestion = pp.load()

with open('bdd/participation', 'rb') as fichier:
    pp = pickle.Unpickler(fichier)
    matriceOrganisation = pp.load()


#VARIABLES GLOBALES
n = len(identifiantPersonne)
m = len(identifiantQuestion)
matriceConfOrnagisee = np.zeros((m, 5)) - 1 #Le «-1» sert à initialiser la matrice matriceConfOrnagisee. C'est le code "personne n'est pas intéressé par cette question"
l = 0.5 # l pour lambda. C'est un paramètre à déterminer.


#DÉFINITIONS DES FONCTIONS
def AireProba(a):
    return math.exp(-l*(a-1) -1) #Une certaine fonction, pas besoin de normaliser.

def ListerPersonnesInteressees(idQuestion):
    return [ j for j in range(n) if matriceOrganisation[j, idQuestion] > -1 ] #Parfois, j'aime python <3

def AssocierPoidsACoefficient(tailleListeCoefficient):
    listePoids = [0 for _ in range(tailleListeCoefficient)]
    a = 0
    for i in range(tailleListeCoefficient):
        listePoids[i] = AireProba(a) #On prend l'aire de 0 à a
        a += 1/tailleListeCoefficient
    return listePoids

#Pour choisir un coefficient, on regarde les poids triées par ordre croissant
def dicho( tableauTrie, valeur ): #valeur se trouve entre le min et le max tu tableau trié
    n = len(tableauTrie)
    a = 0
    b = n
    while(b - a > 1):
        m = int((a+b)/2) # m comme moitié. Attention, c'est un entier !
        if (valeur >= tableauTrie[m] ):
            a = m
        else:
            b = m
    return a

def TirerCoefficient(listeCoefficient):
    m = len(listeCoefficient)
    listePoids = AssocierPoidsACoefficient(m) #Normalement triée par ordre croissant, puisque la fonction p décroit ( on prend l'aire de 0 à p )
    hasard = rd.uniform(0, max(listePoids)) #le maximun correspond à l'aire
    return listeCoefficient[dicho(listePoids, hasard)] # WTF MAIS N'IMP

def TirerUnePersonnePourLaQuestion(idQuestion):
    listePersonne=ListerPersonnesInteressees(idQuestion)

    temp = [[listePersonne[i],matriceOrganisation[listePersonne[i], idQuestion]] for i in range(len(listePersonne))]
    temp = sorted(temp, key=lambda essai:essai[1]) #Trier par ordre croissant de coefficient de participation

    listeCoefficientDifferentTries =list(set([temp[i][1] for i in range(len(temp))]))
    coefDeLaPersonneTiree = TirerCoefficient(listeCoefficientDifferentTries)

    listePersonneDeCoef = [temp[i][0] for i in range(len(listePersonne)) if temp[i][1] == coefDeLaPersonneTiree] # OH TA MÈRE
    personneTiree = listePersonneDeCoef[rd.randint(0, len(listePersonneDeCoef)-1)]

    return personneTiree

#Début du programme:

#Pour chaque question, on liste les personnes intéressées, et triées dans l'ordre de priorité de participation
#(ceux qui ont participé le moins à une question sont prioritaires.)

listePersonnesDisponibles = [True for i in range(n)] #Cette liste permettra de suivre les personnes qui participent déjà aux questions.
listeQuestionTraitees = [False for i in range(m)] #Pareil, on regarde les questions traitées

#ON Y VA EN MODE BOURRIN !
for question in range(m):
    #On prend une question au hasard:
    idQuestion = rd.randint(0, m-1)
    while listeQuestionTraitees[idQuestion] :
        idQuestion = (idQuestion + 1) % m #Si jamais elle est déjà traitées, on choisit la suivante modulo le nombre de questions
    listeQuestionTraitees[idQuestion] = True #On marque la question comme traitée.

    #Pour cette question, il nous reste plus qu'à tirer 5 personnes différentes.

    for compteur in range(5):
        personne = TirerUnePersonnePourLaQuestion(idQuestion)
        #En mode bourrin, si elle n'est pas dispo, on tire au hasard une autre personne
        #TODO: l'algorithme tourne en rond s'il n'y a pas assez de personne !!
        while (not listePersonnesDisponibles[personne]):
                personne = TirerUnePersonnePourLaQuestion(idQuestion)

        #Et une fois que c'est bon, on marque la personne comme plus disponible
        listePersonnesDisponibles[personne] = False

        #On l'ajoute au planning
        matriceConfOrnagisee[idQuestion,compteur] = personne

        #On incrémente son coefficient de participation
        matriceOrganisation[personne, idQuestion] += 1

#Affichage propre:

for question in range(m):
        textPersonne =""
        for personne in range(5):
            if matriceConfOrnagisee[question][personne] > -1:
                textPersonne += identifiantPersonne[int(matriceConfOrnagisee[question][personne])] + "#" + str(int(matriceConfOrnagisee[question][personne]))+", "
        print("Le groupe composée de " + textPersonne + "s'occupera la question : " + identifiantQuestion[question])

#Enregistrement de la matriceOrganisation qui stocke tous les coefficients de participation
with open('bdd/participation', 'wb') as fichier:
    mon_pickler = pickle.Pickler(fichier)
    mon_pickler.dump(matriceOrganisation)


#Affichage propre de la matriceOrganisation

print(matriceOrganisation)

for personne in range(n):
    nomPersonne = identifiantPersonne[personne]
    text = nomPersonne + ":"
    for question in range(m):
        nomQuestion = identifiantQuestion[question]
        text += nomQuestion + " " + str(matriceOrganisation[personne, question])
    print(text)
