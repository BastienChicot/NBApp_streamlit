# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 17:02:37 2021

@author: basti
"""

import pandas as pd
import numpy as np

import altair as alt
import streamlit as st
from Services.stats_joueurs import  stat_20matchs_splits,stat_Opp_team,stat_teams
from Services.predictions_joueur import calcul_predictions
from Services.pred_match import simul_game,create_df

df=pd.read_csv("data/data_ML.csv", sep=";")
players_base = pd.read_csv('data/nba_players.csv', sep=";")

proj_game=pd.read_csv("data/Base_simu.csv",sep=";")

liste_team=np.unique(df['Tm'])
evo = pd.read_csv("data/evo_carriere.csv",sep=";")
name=pd.DataFrame(np.unique(evo['full_name']))
equipe_simulation=np.unique(proj_game['Tm'])

mois =[i for i in range(1,13)]

def onglet_stat():
    a=st.text_input("Sélectionner un joueur", autocomplete="none")
    tm_option=st.selectbox('Player team',liste_team)
    opp_option=st.selectbox('Opponent team',liste_team)
    button_stats = st.button("Afficher les stats du joueur")
    
    def affich_stats(a,opp_option,tm_option):
        try:
            df1=evo.loc[evo["full_name"]==str(a)]
            df1=df1[["year","PRP","DEF","MIS","MP"]]
            df1.sort_values(by=['year'])
            df2=df1
            df2=df2.set_index("year")
            df2=df2.stack().reset_index()
            df2=df2.rename(columns={0:"mesure"})
            graph=alt.Chart(df2).transform_calculate().mark_line().encode(
                x="year",y=alt.Y("mesure",title="Mesures"),color="level_1")
            st.altair_chart(graph, use_container_width=True)
            last_twenty,splits = stat_20matchs_splits(str(a))
            against = stat_Opp_team(a,opp_option)
            team_rank=stat_teams(tm_option,opp_option)
            st.dataframe(name)
            st.dataframe(last_twenty)
            st.dataframe(splits)
            st.dataframe(against)
            st.dataframe(team_rank)
        except:
            pass
    if button_stats :
        affich_stats(a,opp_option,tm_option)
    else:
        st.dataframe(name)
        
def onglet_prediction():
    st.dataframe(name)
    a=st.text_input("Selectionner un joueur", autocomplete="none")
    b=st.text_input("Selectionner un l'adversaire direct", autocomplete="none")
    opp_option=st.selectbox("Equipe adverse",liste_team)
    starter=st.selectbox("Titulaire",(0,1))
    home=st.selectbox("Domicile",(0,1))
    month=st.selectbox("Mois",mois)
    m=st.text_input("Minutes", autocomplete="on")
    button_pred=st.button("Lancer la prediction")
    
    if button_pred:
        predp,predp_2,predf,preda,predr=calcul_predictions(a,opp_option,b,starter,home,month,m)
        st.text("Points marqués avec le modèle 1")
        st.text(predp)
        st.text("Points marqués avec le modèle 2")
        st.text(predp_2)
        st.text("Tirs tentés")
        st.text(predf)
        st.text("Passes décisives")
        st.text(preda)
        st.text("Rebonds")
        st.text(predr)
    
def onglet_simu():
    tm_dom=st.selectbox("Equipe domicile",equipe_simulation)
    tm_road=st.selectbox("Equipe visiteurs",equipe_simulation)
    month=st.selectbox("Mois",mois)
    check_roster=st.checkbox("Afficher les effectifs et sélectionner les absents")

    if check_roster:
        df_team=proj_game.loc[proj_game['Tm']==tm_dom]
        df_opp=proj_game.loc[proj_game['Tm']==tm_road]
        home_player=np.unique(df_team['full_name'])
        road_player=np.unique(df_opp['full_name'])
        home_select = st.multiselect('Cliquer sur les joueurs absents à domicile', home_player) 
        road_select = st.multiselect('Cliquer sur les joueurs visiteurs absents', road_player)
        slide = st.slider("Nombre de simulations",min_value=10,max_value=500,step=1)
        
    if st.button("Lancer la prédiction"):
        my_bar = st.progress(0)
        mask_home = ~df_team['full_name'].isin(home_select)
        mask_road = ~df_opp['full_name'].isin(road_select)
        equipe=str(tm_dom)
        Opp=str(tm_road)
        df_team = df_team[mask_home]
        df_opp = df_opp[mask_road]
        df_team['Opp']=Opp
        df_opp['Opp']=equipe
        df_team=create_df(df_team,month)
        df_opp=create_df(df_opp,month)
    
        final=[]
        
        for i in range (slide):
            j=int(i/(slide/100))
            my_bar.progress(j)
            bilan=simul_game(equipe,Opp,df_team,df_opp,month)  
            final.append(bilan)
            
        df_fin=pd.concat(final)
        df_fin['victoire']=df_fin.Victoire.astype(float)
        df_final= df_fin.groupby(df_fin['Team']).sum().reset_index()
        win = df_final['victoire']
        loss = slide-df_final['victoire']
        
        win=round(win/slide*100,2)
        loss=round(loss/slide*100,2)
        
        win = str(*win)
        loss = str(*loss)
        
        st.text("Pourcentage de victoire de "+tm_dom+" : " +win)
        st.text("Pourcentage de victoire de "+tm_road+" : " +loss)

        