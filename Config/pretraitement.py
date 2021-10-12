# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 15:57:05 2021

@author: basti
"""

#BASE SIMU ==> Qutodien, Hebdo ou mesuel peu importe ANNUEL DUR DUR MAIS A TESTER
#CLUSTER ==> Quotidien OK
#DATA ML ==> Quotidien  OK
#EVO CARRIERE ==> Annuel 
#INDICE TEAM==> Au cours de la saison mais ça peut être hebdo PAS OK A REFLECHIR
#NBA PLAYERS donc ROSTER ==> Une fois par an pour les rookies et les codes OK
#NBA PLAYERS STATS SAISON ==> Quotidien pour les 20 derniers matchs OK
#RANKING TEAM ==> Qutodien  OK
#TEAM STATS dans team_config. Mettre à jour les années une fois par an

#0. TEAMSTATS via config_team.py Nécessaire pour data_ml
#1. DATA_ML / STATS SAISON / CLUSTER / COACHS via le code data_ml.py
#2. RANKING TEAM et ROSTER via team_config.py
#3. BASE SIMU via base_simu.py
#4. INDICE TEAM via calcul_indice_team.csv
#5. EVO CARRIERE quand j'ai le temps via NBA/old/Maj BDD/3.carriere.py
#6. NBA PLAYERS 1 fois par an pour ajouter les rookies directement dans l'ancien fichier 
    ### NE JAMAIS OVERWRITE LE FICHIER NBA PLAYER!!!
import os

os.chdir("C:/Users/basti/OneDrive/Bureau/App web/Config")

from data_ml import maj_data_fun
from team_config import stat_teams, recup_roster,teamstats
from base_simu import base_simu_fun
from calcul_indice_team import calcul_indice

annee=2021

##0. Teamstats
print("Récupération des stats d'équipes")
teamstats()
print("Stats d'équipe à jour")

##1. DATA ML
print("Lancement du prétraitement")
print("Création de la base data_ml et des bases stats_saison, cluster et coach")
maj_data_fun(annee)
print("data_ml à jour")

#2. RANKING TEAM, TEAMSTATS et ROSTER
print("Téléchargement des ranking par équipe")
stat_teams()
print("Fichier ranking téléchargé")
print("Récupération des rosters")
recup_roster()
print("Rosters à jour dans le dossier config")

#3. BASE SIMU
print("Création de la base simu à partir de data_ml")
base_simu_fun(annee)
print("base_simu à jour")

#4. Calcul des indices des teams pour les prédictions
print("Mise à jour des indices")
calcul_indice(annee)
print("Traitement terminé")