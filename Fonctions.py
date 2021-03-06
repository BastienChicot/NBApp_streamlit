# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 17:02:37 2021

@author: basti
"""
# import sys
# sys.path.append("/data/")
# sys.path.append("/models/")
# sys.path.append("/Services/")

import pandas as pd
import numpy as np

import altair as alt
import streamlit as st
from Services.stats_joueurs import  stat_20matchs_splits,stat_Opp_team,stat_teams
from Services.predictions_joueur import calcul_predictions
from Services.pred_match import simul_game,create_df

proj_game=pd.read_csv("data/Base_simu.csv",sep=";")
df=pd.read_csv("data/data_ML.csv", sep=";")
players_base = pd.read_csv('data/nba_players.csv', sep=";")

liste_team=pd.unique(df["Tm"])
liste_team.sort()
evo = pd.read_csv("data/evo_carriere.csv",sep=";")
liste_name=np.unique(evo['full_name'])
name=pd.DataFrame(np.unique(evo['full_name']))
name=name.rename(columns={0:"Joueur"}) 
equipe_simulation=(proj_game['Tm']).dropna()
equipe_simulation=pd.unique(equipe_simulation)
equipe_simulation.sort()

mois =[i for i in range(1,13)]

def onglet_stat():
    
    st.title("Etudier les statistiques d'un joueur")
    col1, col2 = st.columns(2)
    a=col1.selectbox("Sélectionner un joueur", liste_name)
    tm_option=col1.selectbox('Player team',liste_team)
    opp_option=col1.selectbox('Opponent team',liste_team)
    button_stats = col1.button("Afficher les stats du joueur")
    col2.text("Liste des joueurs en activité."+"\n"+"Retrouver la bonne orthographe"+"\n"+"si votre requête ne fonctionne pas." )
        
    def affich_stats(a,opp_option,tm_option):
        try:
            ##Afficher le lien basketball reference
            full_name=str(a)
            code_base = players_base.loc[players_base['full_name'] == full_name].values[0]
            y = code_base[2:3]
            code = ''.join(y)
            annee = '2021'
            yeah=int(annee)
            url = 'https://www.basketball-reference.com/players/a/'+str(code)+'/gamelog/'+str(annee)
            col2.markdown(url, unsafe_allow_html=True)
        
            #sorties stats
            df1=evo.loc[evo["full_name"]==str(a)]
            df1=df1[["year","PRP","DEF","MIS","MP"]]
            df1.sort_values(by=['year'])
            df2=df1
            df2=df2.set_index("year")
            df2=df2.stack().reset_index()
            df2=df2.rename(columns={0:"mesure"})
            graph=alt.Chart(df2).transform_calculate().mark_line().encode(
                x="year",y=alt.Y("mesure",title="Mesures"),color="level_1")
            last20 = stat_20matchs_splits(str(a))
            last20=last20.set_index('Date')
            against = stat_Opp_team(str(a),str(opp_option))
            met=against.groupby(by="annee").mean()
            met=met.reset_index()
            met=met.loc[met["annee"]==yeah]
            against=against.set_index("Opp")
            team_rank=stat_teams(str(tm_option),str(opp_option))
            team_rank=team_rank.set_index("TEAM")
            col2.dataframe(name)
            
            st.header("Moyenne cette saison contre " +str(opp_option))
            col3,col4,col5,col6=st.columns(4)
            col3.metric("Points par match",str(*met["PTS"]),
                      str(*met["PTS_diff"]))
            col4.metric("Passes par match",str(*met["AST"]),
                      str(*met["AST_diff"]))
            col5.metric("Rebonds par match",str(*met["TRB"]),
                      str(*met["TRB_diff"]))
            col6.metric("Minutes par match",str(*met["minutes"]))
            
            st.header("Statistiques cumulées au cours de la carrière")
            st.text("DEF = contres + interception \nMIS = fautes + balles perdues" + "\n" + 
                    "MP = minutes \nPRP = points + rebonds + passes décisives")
            st.altair_chart(graph, use_container_width=True)
            st.header("Statistiques lors des 20 derniers matchs")
            st.dataframe(last20)
            #st.header("Statistiques splits")
            #st.dataframe(splits)
            st.header("Statistiques contre "+opp_option)
            st.text("Les différences sont calculées par rapport à la moyenne sur la saison au cours de \nlaquelle s'est déroulé le match")
            st.dataframe(against)
            st.header("Rankings des deux équipes")
            st.dataframe(team_rank)
        except:
            pass
    if button_stats :
        affich_stats(a,str(opp_option),str(tm_option))
    else:
        col2.dataframe(name)
        
def onglet_prediction():
    
    st.title("Projections individuelles")
    col1, col2 = st.columns(2)
    col2.text("Liste des joueurs en activité."+"\n"+"Retrouver la bonne orthographe"+"\n"+"si votre requête ne fonctionne pas." )
    col2.dataframe(name)
    a=col1.selectbox("Selectionner un joueur",liste_name)
    b=col1.selectbox("Selectionner un l'adversaire direct",liste_name)
    opp_option=col1.selectbox("Equipe adverse",liste_team)
    starter=col1.selectbox("Titulaire",(0,1))
    home=col1.selectbox("Domicile",(0,1))
    month=col1.selectbox("Mois",mois)
    m=col1.text_input("Minutes", autocomplete="on")
    button_pred=col1.button("Lancer la prediction")
    
    if button_pred:
        predp,predp_2,predf,preda,predr=calcul_predictions(str(a),str(opp_option),str(b),starter,home,month,int(m))
        st.text("Points marqués avec le modèle 1 : " + "  " +predp)
        st.empty()
        st.text("Points marqués avec le modèle 2 : " + "  " +predp_2)
        st.empty()
        st.text("Tirs tentés : " + "                      " + predf)
        st.empty()
        st.text("Passes décisives : " + "                 " +preda )
        st.empty()
        st.text("Rebonds : " + "                          " +predr)
    
def onglet_simu():
    st.title("Simuler un match")
    st.empty()
    col1, col2, col3 = st.columns(3)
    tm_dom=col1.selectbox("Equipe domicile",equipe_simulation)
    tm_road=col2.selectbox("Equipe visiteurs",equipe_simulation)
    month=col3.selectbox("Mois",mois)
    check_roster=st.checkbox("Afficher les effectifs, sélectionner les absents et choisir le nombre de simulations" + "\n" +
                             "(Obligatoire pour pouvoir lancer la simulation)")
    
    if check_roster:
        df_team=proj_game.loc[proj_game['Tm']==tm_dom]
        df_opp=proj_game.loc[proj_game['Tm']==tm_road]
        home_player=np.unique(df_team['full_name'])
        road_player=np.unique(df_opp['full_name'])
        home_select = col1.multiselect('Cliquer sur les joueurs absents à domicile', home_player) 
        road_select = col2.multiselect('Cliquer sur les joueurs visiteurs absents', road_player)
        slide = col3.slider("Nombre de simulations",min_value=10,max_value=500,step=1)
        
        if st.button("Lancer la prédiction"):
            my_bar = st.progress(0)
    
            mask_home = ~df_team['full_name'].isin(home_select)
            mask_road = ~df_opp['full_name'].isin(road_select)
            df_team = df_team[mask_home]
            df_opp = df_opp[mask_road]
    
            equipe=str(tm_dom)
            Opp=str(tm_road)
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

        