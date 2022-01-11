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
    
#7 MISE A JOUR DES BASES TENNIS AVEC LE FICHIER pretraitement_tennis.py
#8 MISE A JOUR DES MODELES DE PREDICTIONS DE TENNIS avec maj_modeles_tennis.py
import os

os.chdir("C:/Users/basti/OneDrive/Bureau/App web/Config")

from data_ml import maj_data_fun
from team_config import stat_teams, recup_roster,teamstats
from base_simu import base_simu_fun
from calcul_indice_team import calcul_indice
from Entrainement_modèles import train_model_ast,train_model_trb,train_model_pts,train_model_fga,train_model_simu
from pretraitement_tennis import create_fichier, nettoyage
from maj_modeles_tennis import maj_model_tennis

annee=2022
year=2022

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

#5. Entrainement des modèles
print("Entrainement des modèles de prédiction")
train_model_ast()
train_model_fga()
train_model_pts()
train_model_trb()
train_model_simu()
print("Fin de la mise à jour des modèles")

#7 Mise à jour des données tennis
print("Téléchargement des données tennis")
create_fichier(year)
print("fichiers téléchargés")
print("Création des bases wta et atp")
nettoyage("atp")
nettoyage("wta")
print("fichiers tennis à jour")

#8 Mise à jour des modèles de prédiction tennis
print("Mise à jour des modèles de prédiction tennis")
maj_model_tennis("atp")
maj_model_tennis("wta")
print("Modèles de prédictions à jour")
