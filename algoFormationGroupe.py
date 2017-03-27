# Voici la version actuelle du code de l'algorithme de formation des groupes de débats.
# Pour l'instant, l'algorithme fonctionne sans erreur.

# Listes des fonctionnalités implémentéées:

# - On peut assigner 5 personnes différentes pour chaques questions

# - On   séléctionne les personnes selon leur participation (globale) (les premières
# tirées sont celles qui ont le moins participé)

# -Marche quelque soit le  nombre de personne ou le nombre de question. (s'il n'y a pas assez de
# personne, la matrice contient des 0)

#TODO: Cet algorithme «prioritarise» d'une certaine façon la question 1,
# puisqu'il assigne les personnes d'abord pour la quesiton 1 puis les marquent
# comme non disponible. Est-ce raisonnable ?
#TODO:

import numpy as np
import random as rd

#Variables globales
identifiantPersonne = ["Christophe", "Julie", "Cyprien", "Victor", "Fabien", "Jean Pierre", "Alice", "Bob", "Candice", "Damien"]
identifiantQuestion = ["Question 1", "Question 2"]

n = len(identifiantPersonne)
m = len(identifiantQuestion)

matriceOrganisation = np.zeros((n,m)) #Cherchez pas à comprendre les doubles parenthèses...

#Le «-1» sert à initialiser la matrice matriceConfOrnagisee. C'est le code "personne n'est assigné à cette question"
matriceConfOrnagisee = np.zeros((m, 5))-1

#Fonctions
def ListerPersonnesInteressees(idQuestion):
    return [ j for j in range(n) if matriceOrganisation[j, idQuestion] > -1 ] #Parfois, j'aime python <3

def TirerPersonnesPourLaQuestion(idQuestion):
    listePersonne=ListerPersonnesInteressees(idQuestion)

    temp = [[listePersonne[i],matriceOrganisation[listePersonne[i], idQuestion]] for i in range(len(listePersonne))]
    temp = sorted(temp, key=lambda essai:essai[1]) #Trier en fonction du coefficient de participation

    for i in range(5):
        matriceOrganisation[temp[i][0],idQuestion] += 1

    return [temp[i][0] for i in range(len(temp))]

#Remplissage alétoire pour tester le programme:
for i in range(n):
    for j in range(m):
        matriceOrganisation[i,j] = rd.randint(0, 3)

#Début du programme:

#Pour chaque question, on liste les personnes intéressées, et triées dans l'ordre de priorité de participation
#(ceux qui ont participé le moins à une question sont prioritaires.)

listePersonneDisponibles = [True for i in range(n)] #Cette liste permettra de suivre les personnes qui participent déjà aux questions.

for question in range(m):
    liste = TirerPersonnesPourLaQuestion(question)
    compteur = 0
    for personne in liste:
        if listePersonneDisponibles[personne] and compteur < 5: #On remplit la matriceConfOrnagisee pour chaque question
                                                                #si les personnes sont dispo, et si on a mis moins de 5 personnes.
            matriceConfOrnagisee[question,compteur] = personne
            compteur +=1 # Ce compteur sert à compter le nombre de personne assignés à une question
            listePersonneDisponibles[personne] = False #la personne participe à une question, donc n'est plus dispo

#Affichage propre:

for question in range(m):
        textPersonne =""
        for personne in range(5):
            textPersonne += identifiantPersonne[int(matriceConfOrnagisee[question][personne])] +", "
        print("Le groupe composée de " + textPersonne + "s'occupera la question : " + identifiantQuestion[question])
