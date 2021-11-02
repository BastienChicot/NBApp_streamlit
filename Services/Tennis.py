# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:57:40 2021

@author: basti
"""

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

df=pd.read_csv("data/base_tennis.csv",sep=";")
wta=pd.read_csv("data/base_tennis_wta.csv",sep=";")

liste_nom = np.unique(df["name"])
liste_surface = pd.unique(df["surface"])
liste_tournoi = pd.unique(df["tourney_name"])

liste_nom_wta = np.unique(wta["name"])
liste_surface_wta = pd.unique(wta["surface"])
liste_tournoi_wta = pd.unique(wta["tourney_name"])

def page_tennis():
    select_nom = st.selectbox("Selectionner un joueur",liste_nom,index=1691)
    if select_nom:
        st.header(select_nom)
        data=df.loc[df["name"]==select_nom]
        caract=data[["age","ht","hand","ioc"]]
        caract=caract.drop_duplicates()
        caract=caract.loc[caract["age"]==max(caract["age"])]
        st.text("Nationalité : " + str(*caract["ioc"]))
        col1, col2,col3 = st.columns(3)
        col1.text("Age : " + "\n" + str(int(caract["age"])))
        col2.text("Taille : " + "\n" + str(int(caract["ht"])))
        col3.text("Main forte : " + "\n" + str(*caract["hand"]))
        
        stat,carr=stat_base(data)        
        st.subheader("Statistiques par saison : ")
        st.dataframe(stat.style.format("{:.3}"))
        st.subheader("Statistiques en carrière : ")
        st.dataframe(carr.style.format("{:.3}"))
        
        type_rech=st.radio("Rechercher par : ",("Surface","Tournoi"))
        
        if type_rech == "Surface":
            col4, col5 = st.columns(2)
    
            surf=col4.selectbox("Choisir une surface : ",liste_surface)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom,index=1846)
            affich=col5.button("Afficher les statistiques")
            
            if affich :
                graphic,vs=stat_by_surface(data,surf,adv)
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur la surface sélectionée")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" (surface = " +str(surf)+" )")
                st.dataframe(vs)
            
        if type_rech == "Tournoi":
            col4, col5 = st.columns(2)
    
            tour=col4.selectbox("Choisir un tournoi : ",liste_tournoi)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom,index=1846)
            affich=col5.button("Afficher les statistiques")
            
            if affich:
                graphic,vs=stat_by_tournoi(data,tour,adv)
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur le tournoi sélectioné")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" à " +str(tour))
                st.dataframe(vs)

def page_wta():
    select_nom = st.selectbox("Selectionner un joueur",liste_nom_wta,index=293)
    if select_nom:
        st.header(select_nom)
        data=wta.loc[wta["name"]==select_nom]
        caract=data[["age","ht","hand","ioc"]]
        caract=caract.drop_duplicates()
        caract=caract.loc[caract["age"]==max(caract["age"])]
        st.text("Nationalité : " + str(*caract["ioc"]))
        col1, col2,col3 = st.columns(3)
        col1.text("Age : " + "\n" + str(int(caract["age"])))
        col2.text("Taille : " + "\n" + str(int(caract["ht"])))
        col3.text("Main forte : " + "\n" + str(*caract["hand"]))
        
        stat,carr=stat_base(data)        
        st.subheader("Statistiques par saison : ")
        st.dataframe(stat.style.format("{:.3}"))
        st.subheader("Statistiques en carrière : ")
        st.dataframe(carr.style.format("{:.3}"))
        
        type_rech=st.radio("Rechercher par : ",("Surface","Tournoi"))
        
        if type_rech == "Surface":
            col4, col5 = st.columns(2)
    
            surf=col4.selectbox("Choisir une surface : ",liste_surface_wta)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom_wta,index=288)
            affich=col5.button("Afficher les statistiques")
            
            if affich :
                graphic,vs=stat_by_surface(data,surf,adv)
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur la surface sélectionée")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" (surface = " +str(surf)+" )")
                st.dataframe(vs)
            
        if type_rech == "Tournoi":
            col4, col5 = st.columns(2)
    
            tour=col4.selectbox("Choisir un tournoi : ",liste_tournoi_wta)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom_wta,index=1846)
            affich=col5.button("Afficher les statistiques")
            
            if affich:
                graphic,vs=stat_by_tournoi(data,tour,adv)
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur le tournoi sélectioné")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" à " +str(tour))
                st.dataframe(vs)

def stat_base(data):
    data=data.sort_values(by=['tourney_date'],ascending=False)
    carr=data[["ace_car","df_car","nb_set_car"]]
    stat=data[["annee","seed","ace_sea","df_sea","nb_set_sea"]]
    stat=stat.rename(columns={"seed":"Classement",
                              "ace_sea":"Nb d'ace moyen/match","nb_set_sea":"Nb de set par match",
                              "df_sea":"Nb de doubles fautes moyen/match"})
    stat=stat.drop_duplicates(subset=["annee"],keep="last")
    stat=stat.set_index("annee")
    
    
    carr=carr.rename(columns={"ace_car":"Nb d'ace moyen/match",
                              "df_car":"Nb de doubles fautes moyen/match",
                              "nb_set_car":"Nb de set par match"})
    carr=carr.drop_duplicates(keep="last")
    
    return(stat,carr)

def stat_by_surface(data,surf,adv):
    surface=data.loc[data["surface"]==surf]
    tot_surf=surface.groupby(['annee']).size().reset_index(name='counts')
    results=surface.groupby(['annee',"result"]).size().reset_index(name='counts_result')
    
    ttt=tot_surf.merge(results,on=["annee"],how="outer")
    ttt=ttt.loc[ttt["result"]=="win"]
    ttt["pct"]=ttt["counts_result"]/ttt["counts"]*100
    
    year_stat=data.groupby(['annee']).size().reset_index(name='counts')
    year_results=data.groupby(['annee',"result"]).size().reset_index(name='counts_result')
    
    total=year_stat.merge(year_results,on=["annee"],how="outer")
    total=total.loc[total["result"]=="win"]
    total["pct_year"]=total["counts_result"]/total["counts"]*100
    
    final=total[["annee","pct_year"]]
    final=final.merge(ttt,on="annee")
    final=final[["annee","pct_year","pct"]]
    
    final=final.set_index("annee")
    final=final.stack().reset_index()
    final=final.rename(columns={0:"mesure"})
    
    domain = ['pct_year', 'pct']
    range_ = ["blue",'red']
    
    graphic=alt.Chart(final).transform_calculate().mark_line().encode(
                x="annee",y=alt.Y("mesure",title="Mesures"),color=alt.Color("level_1"
                                                                            , scale=alt.Scale(domain=domain, range=range_)
                                                                            , legend=alt.Legend(title="Pct de victoires")))

    vs = surface.loc[surface["advers"]==adv]
    vs=vs.sort_values(by=['tourney_date'],ascending=False)
    vs=vs[["annee","tourney_name","surface","score","ace","df","result",
           "ace_diff_s","df_diff_s","minutes_diff_s","nb_set_diff_s"]]
    vs=vs.set_index("annee")
    vs=vs.rename(columns={"ace_diff_s":"Différence nb ace/moyenne en saison",
                          "df_diff_s":"Différence nb df/moyenne en saison",
                          "minutes_diff_s":"Différence minutes de match/moyenne saison",
                          "nb_set_diff_s":"Différence nb de set/moyenne saison"})
    return(graphic,vs)

def stat_by_tournoi(data,tour,adv):
    surface=data.loc[data["tourney_name"]==tour]
    tot_surf=surface.groupby(['annee']).size().reset_index(name='counts')
    results=surface.groupby(['annee',"result"]).size().reset_index(name='counts_result')
    
    ttt=tot_surf.merge(results,on=["annee"],how="outer")
    ttt=ttt.loc[ttt["result"]=="win"]
    ttt["pct"]=ttt["counts_result"]/ttt["counts"]*100
    
    year_stat=data.groupby(['annee']).size().reset_index(name='counts')
    year_results=data.groupby(['annee',"result"]).size().reset_index(name='counts_result')
    
    total=year_stat.merge(year_results,on=["annee"],how="outer")
    total=total.loc[total["result"]=="win"]
    total["pct_year"]=total["counts_result"]/total["counts"]*100
    
    final=total[["annee","pct_year"]]
    final=final.merge(ttt,on="annee")
    final=final[["annee","pct_year","pct"]]
    
    final=final.set_index("annee")
    final=final.stack().reset_index()
    final=final.rename(columns={0:"mesure"})
    
    domain = ['pct_year', 'pct']
    range_ = ["blue",'red']
    
    graphic=alt.Chart(final).transform_calculate().mark_line().encode(
                x="annee",y=alt.Y("mesure",title="Mesures"),color=alt.Color("level_1"
                                                                            , scale=alt.Scale(domain=domain, range=range_)
                                                                            , legend=alt.Legend(title="Pct de victoires")))
    vs = surface.loc[surface["advers"]==adv]
    vs=vs.sort_values(by=['tourney_date'],ascending=False)
    vs=vs[["annee","tourney_name","surface","score","ace","df","result",
           "ace_diff_s","df_diff_s","minutes_diff_s","nb_set_diff_s"]]
    vs=vs.set_index("annee")
    vs=vs.rename(columns={"ace_diff_s":"Différence nb ace/moyenne en saison",
                          "df_diff_s":"Différence nb df/moyenne en saison",
                          "minutes_diff_s":"Différence minutes de match/moyenne saison",
                          "nb_set_diff_s":"Différence nb de set/moyenne saison"})
    
    return(graphic,vs)