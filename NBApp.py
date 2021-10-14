# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 10:05:11 2021

@author: basti
"""
import streamlit as st
from Fonctions import onglet_stat,onglet_prediction,onglet_simu
import pandas as pd
from PIL import Image

icon=Image.open("icone.ico")
st.set_page_config(
    page_title="NBApp pour parieur",
    page_icon=icon,
    layout="wide",
    )

name_team=pd.read_csv("data/correspondance_equipe.csv",sep=";")
del name_team["Unnamed: 0"]
del name_team["Unnamed: 0.1"]
name_team=name_team.set_index('Tm')

st.sidebar.header("Choisir un onglet")
menu_choice = st.sidebar.radio("Onglets",
                               ("Etudier les statistiques d'un joueur",
                                "Projections individuelles",
                                "Simuler un match"))
st.sidebar.text("Liste des codes d'équipes")
st.sidebar.dataframe(name_team)

if menu_choice == "Etudier les statistiques d'un joueur":
    onglet_stat()
if menu_choice=="Projections individuelles":
    onglet_prediction()
if menu_choice=="Simuler un match":
    onglet_simu()
