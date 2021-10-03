# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 10:05:11 2021

@author: basti
"""
import pandas as pd
import streamlit as st
from Fonctions import onglet_stat,onglet_prediction,onglet_simu
import numpy as np

menu_choice = st.sidebar.radio("Onglets",
                               ("Etudier les statistiques d'un joueur",
                                "Projections individuelles",
                                "Simuler un match"))

proj_game=pd.read_csv("data/Base_simu.csv",sep=";")



if menu_choice == "Etudier les statistiques d'un joueur":
    onglet_stat()
if menu_choice=="Projections individuelles":
    onglet_prediction()
if menu_choice=="Simuler un match":
    onglet_simu()
