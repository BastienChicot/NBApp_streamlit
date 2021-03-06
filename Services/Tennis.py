# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:57:40 2021

@author: basti
"""

import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from joblib import load

df=pd.read_csv("data/base_tennis_atp.csv",sep=";")
wta=pd.read_csv("data/base_tennis_wta.csv",sep=";")

base_win_atp=pd.read_csv("data/tennis_atp-master/base_atp_win.csv",sep=";")
base_win_wta=pd.read_csv("data/tennis_wta-master/base_wta_win.csv",sep=";")

liste_nom = list(np.unique(df["name"]))
djoko = liste_nom.index("Novak Djokovic")
rafa = liste_nom.index("Rafael Nadal")
liste_surface = pd.unique(df["surface"])
liste_tournoi = pd.unique(df["tourney_name"])
liste_level = pd.unique(df["tourney_level"])

liste_nom_wta = list(np.unique(wta["name"]))
barty = liste_nom_wta.index("Ashleigh Barty")
saba = liste_nom_wta.index("Aryna Sabalenka")
liste_surface_wta = pd.unique(wta["surface"])
liste_tournoi_wta = pd.unique(wta["tourney_name"])

liste_nom_predi_atp = list(np.unique(base_win_atp["name"]))
djoko2 = liste_nom_predi_atp.index("Novak Djokovic")
rafa2 = liste_nom_predi_atp.index("Rafael Nadal")
liste_nom_predi_wta = list(np.unique(base_win_wta["name"]))
barty2 = liste_nom_predi_wta.index("Ashleigh Barty")
saba2 = liste_nom_predi_wta.index("Aryna Sabalenka")

def page_tennis():
    select_nom = st.selectbox("Selectionner un joueur",liste_nom,index=djoko)
    if select_nom:
        st.header(select_nom)
        data=df.loc[df["name"]==select_nom]
        caract=data[["age","ht","hand","ioc"]]
        caract=caract.drop_duplicates()
        caract=caract.loc[caract["age"]==max(caract["age"])]
        st.text("Nationalit√© : " + str(*caract["ioc"]))
        col1, col2,col3 = st.columns(3)
        col1.text("Age : " + "\n" + str(int(caract["age"])))
        col2.text("Taille : " + "\n" + str(int(caract["ht"])))
        col3.text("Main forte : " + "\n" + str(*caract["hand"]))
        
        stat,carr=stat_base(data)        
        st.subheader("Statistiques par saison : ")
        st.dataframe(stat.style.format("{:.3}"))
        st.subheader("Statistiques en carri√®re : ")
        st.dataframe(carr.style.format("{:.3}"))
        
        type_rech=st.radio("Rechercher par : ",("Surface","Tournoi"))
        
        if type_rech == "Surface":
            col4, col5 = st.columns(2)
    
            surf=col4.selectbox("Choisir une surface : ",liste_surface)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom,index=rafa)
            affich=col5.button("Afficher les statistiques")
            
            if affich :
                graphic,vs,meten=stat_by_surface(data,surf,adv)
                st.header("Moyenne en carri√®re contre " +str(adv))
                st.text("par rapport √† la moyenne en carri√®re")
                col3,col4,col5,col6=st.columns(4)
                col3.metric("Set par match",str(round(float(*meten["nb_set"]),2)),
                          str(round(float(*meten["nb_set_diff_c"]),2)),delta_color="inverse")
                col4.metric("Aces par match",str(round(float(*meten["ace"]),2)),
                          str(round(float(*meten["ace_diff_c"]),2)))
                col5.metric("Doubles fautes par match",str(round(float(*meten["df"]),2)),
                          str(round(float(*meten["df_diff_c"]),2)),delta_color="inverse")
                col6.metric("Minutes par match",str(round(float(*meten["minutes"]),2)),
                            str(round(float(*meten["minutes_diff_c"]),2)),delta_color="inverse")
                
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur la surface s√©lection√©e")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" (surface = " +str(surf)+" )")
                st.dataframe(vs)
            
        if type_rech == "Tournoi":
            col4, col5 = st.columns(2)
    
            tour=col4.selectbox("Choisir un tournoi : ",liste_tournoi)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom,index=rafa)
            affich=col5.button("Afficher les statistiques")
            
            if affich:
                graphic,vs,meten=stat_by_tournoi(data,tour,adv)
                
                st.header("Moyenne en carri√®re contre " +str(adv))
                st.text("par rapport √† la moyenne en carri√®re")
                col3,col4,col5,col6=st.columns(4)
                col3.metric("Set par match",str(round(float(*meten["nb_set"]),2)),
                          str(round(float(*meten["nb_set_diff_c"]),2)),delta_color="inverse")
                col4.metric("Aces par match",str(round(float(*meten["ace"]),2)),
                          str(round(float(*meten["ace_diff_c"]),2)))
                col5.metric("Doubles fautes par match",str(round(float(*meten["df"]),2)),
                          str(round(float(*meten["df_diff_c"]),2)),delta_color="inverse")
                col6.metric("Minutes par match",str(round(float(*meten["minutes"]),2)),
                            str(round(float(*meten["minutes_diff_c"]),2)),delta_color="inverse")
                
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur le tournoi s√©lection√©")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" √† " +str(tour))
                st.dataframe(vs)

def page_wta():
    select_nom = st.selectbox("Selectionner un joueur",liste_nom_wta,index=barty)
    if select_nom:
        st.header(select_nom)
        data=wta.loc[wta["name"]==select_nom]
        caract=data[["age","ht","hand","ioc"]]
        caract=caract.drop_duplicates()
        caract=caract.loc[caract["age"]==max(caract["age"])]
        st.text("Nationalit√© : " + str(*caract["ioc"]))
        col1, col2,col3 = st.columns(3)
        col1.text("Age : " + "\n" + str(int(caract["age"])))
        col2.text("Taille : " + "\n" + str(int(caract["ht"])))
        col3.text("Main forte : " + "\n" + str(*caract["hand"]))
        
        stat,carr=stat_base(data)        
        st.subheader("Statistiques par saison : ")
        st.dataframe(stat.style.format("{:.3}"))
        st.subheader("Statistiques en carri√®re : ")
        st.dataframe(carr.style.format("{:.3}"))
        
        type_rech=st.radio("Rechercher par : ",("Surface","Tournoi"))
        
        if type_rech == "Surface":
            col4, col5 = st.columns(2)
    
            surf=col4.selectbox("Choisir une surface : ",liste_surface_wta)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom_wta,index=saba)
            affich=col5.button("Afficher les statistiques")
            
            if affich :
                graphic,vs,meten=stat_by_surface(data,surf,adv)
                
                st.header("Moyenne en carri√®re contre " +str(adv))
                st.text("par rapport √† la moyenne en carri√®re")
                col3,col4,col5,col6=st.columns(4)
                col3.metric("Set par match",str(round(float(*meten["nb_set"]),2)),
                          str(round(float(*meten["nb_set_diff_c"]),2)),delta_color="inverse")
                col4.metric("Aces par match",str(round(float(*meten["ace"]),2)),
                          str(round(float(*meten["ace_diff_c"]),2)))
                col5.metric("Doubles fautes par match",str(round(float(*meten["df"]),2)),
                          str(round(float(*meten["df_diff_c"]),2)),delta_color="inverse")
                col6.metric("Minutes par match",str(round(float(*meten["minutes"]),2)),
                            str(round(float(*meten["minutes_diff_c"]),2)),delta_color="inverse")
                
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur la surface s√©lection√©e")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" (surface = " +str(surf)+" )")
                st.dataframe(vs)
            
        if type_rech == "Tournoi":
            col4, col5 = st.columns(2)
    
            tour=col4.selectbox("Choisir un tournoi : ",liste_tournoi_wta)
            adv=col5.selectbox("Choisir un adversaire : ",liste_nom_wta,index=saba)
            affich=col5.button("Afficher les statistiques")
            
            if affich:
                graphic,vs,meten=stat_by_tournoi(data,tour,adv)
                
                st.header("Moyenne en carri√®re contre " +str(adv))
                st.text("par rapport √† la moyenne en carri√®re")
                col3,col4,col5,col6=st.columns(4)
                col3.metric("Set par match",str(round(float(*meten["nb_set"]),2)),
                          str(round(float(*meten["nb_set_diff_c"]),2)),delta_color="inverse")
                col4.metric("Aces par match",str(round(float(*meten["ace"]),2)),
                          str(round(float(*meten["ace_diff_c"]),2)))
                col5.metric("Doubles fautes par match",str(round(float(*meten["df"]),2)),
                          str(round(float(*meten["df_diff_c"]),2)),delta_color="inverse")
                col6.metric("Minutes par match",str(round(float(*meten["minutes"]),2)),
                            str(round(float(*meten["minutes_diff_c"]),2)),delta_color="inverse")
                
                st.subheader("Pourcentage de victoires")
                st.text("pct_year = Pourcentage de victoires par an" + "\n" +
                        "pct = Pourcentage de victoires sur le tournoi s√©lection√©")
                st.altair_chart(graphic, use_container_width=True)
                
                st.subheader("Statistiques contre "+str(adv)+" √† " +str(tour))
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
    meten=vs.groupby(by="surface").mean()
    vs=vs.sort_values(by=['tourney_date'],ascending=False)
    vs=vs[["annee","tourney_name","surface","score","ace","df","result",
           "ace_diff_s","df_diff_s","minutes_diff_s","nb_set_diff_s"]]
    vs=vs.set_index("annee")
    vs=vs.rename(columns={"ace_diff_s":"Diff√©rence nb ace/moyenne en saison",
                          "df_diff_s":"Diff√©rence nb df/moyenne en saison",
                          "minutes_diff_s":"Diff√©rence minutes de match/moyenne saison",
                          "nb_set_diff_s":"Diff√©rence nb de set/moyenne saison"})
    return(graphic,vs,meten)

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
    meten=vs.groupby(by="surface").mean()
    vs=vs.sort_values(by=['tourney_date'],ascending=False)
    vs=vs[["annee","tourney_name","surface","score","ace","df","result",
           "ace_diff_s","df_diff_s","minutes_diff_s","nb_set_diff_s"]]
    vs=vs.set_index("annee")
    vs=vs.rename(columns={"ace_diff_s":"Diff√©rence nb ace/moyenne en saison",
                          "df_diff_s":"Diff√©rence nb df/moyenne en saison",
                          "minutes_diff_s":"Diff√©rence minutes de match/moyenne saison",
                          "nb_set_diff_s":"Diff√©rence nb de set/moyenne saison"})
    
    return(graphic,vs,meten)

def page_predi(cat):
    col1 , col2, col3 = st.columns(3)
    if cat=="atp":
        select_nom = col1.selectbox("Selectionner un joueur",liste_nom_predi_atp,index=djoko2)
        surf=col2.selectbox("Choisir une surface : ",liste_surface)
        adv=col3.selectbox("Choisir un adversaire : ",liste_nom_predi_atp,index=rafa2)
        lvl=col1.selectbox("Choisir le niveau du tournoi : ",liste_level)
    else:
        select_nom = col1.selectbox("Selectionner un joueur",liste_nom_predi_wta,index=barty2)
        surf=col2.selectbox("Choisir une surface : ",liste_surface)
        adv=col3.selectbox("Choisir un adversaire : ",liste_nom_predi_wta,index=saba2)
        lvl=col1.selectbox("Choisir le niveau du tournoi : ",liste_level)
        
    st.text("Level : "+"\n"+"A -> ATP"+"\n"+"D -> Davis"+"\n"+"G -> Grand chelem"+"\n"+"M -> Masters")
    
    slide = col2.slider("Nombre de simulations",min_value=1,max_value=50,step=1)
    
    launch=st.button("Lancer les pr√©dictions")
    invert=st.button("Inverser les joueurs et recommencer une pr√©diction")   
    
    if launch:
        my_bar = st.progress(0)
        if cat=="atp":
            df_pred=df.loc[df["name"]==select_nom]
        else:
            df_pred=wta.loc[wta["name"]==select_nom]
            
        df_min=df_pred.loc[df_pred["advers"]==str(adv)]
        
        df_pred=df_pred[["age","ht","name","seed"]]
        df_pred["advers"]=str(adv)
        
        minutes=np.mean(df_min["minutes"])
        df_pred["minutes"]=int(minutes)
        
        try:
            df_pred=df_pred.loc[df_pred["age"]==max(df_pred["age"])]
            df_pred=df_pred.drop_duplicates()
        except:
            df_pred["name"]=str(select_nom)
            df_pred["age"]=25
            df_pred["ht"]=175
            df_pred["seed"]=36
            df_pred["advers"]=str(adv)
            df_pred["minutes"]=96
            
        df_pred["surface"]=str(surf)
        df_pred["tourney_level"]=str(lvl)
        
        try :
            df_pred.loc[(df_pred['seed']<100),"classe"] = True
            df_pred.loc[(df_pred['seed']>=100),"classe"] = False
        except : 
            df_pred["classe"] = False
        
        X = df_pred[['age',
                'ht',
                'name',
                'surface',
                'tourney_level',
                'classe',
                'minutes',
                "advers"
                ]]
        
        finalset=[]
        finalace=[]
        finalwin=[]
        
        try:
                
            for i in range (slide):
                j=int(i/(slide/100))
                my_bar.progress(j)
                nb_set=simul_set(X,cat)
                ace=simul_ace(X,cat)  
                wins=simul_win(X,cat)
                finalset.append(nb_set)
                finalace.append(ace)
                finalwin.append(wins)
    
            meanset = round(np.mean(finalset),2)
            if meanset>7 :
                meanset=7
            
            meanace = round(np.mean(finalace),2)
            
            meanwin = round(np.mean(finalwin)*100,2)
            
            nb_set_m=str(meanset)
            nb_ace= str(meanace)
            vic = str(meanwin)
            
            st.text("Pr√©vision du nombre de set : " +nb_set_m)
            st.text("Pr√©vision d'aces de "+select_nom+" : " +nb_ace)
            st.text("Pr√©vision de victoire de "+select_nom+" : " +vic+" %")
        except TypeError:
            for i in range (slide):
                j=int(i/(slide/100))
                my_bar.progress(j) 
                wins=simul_win(X,cat)
                finalwin.append(wins)
            
            meanwin = round(np.mean(finalwin)*100,2)

            vic = str(meanwin)

            st.text("Pr√©vision de victoire de "+select_nom+" : " +vic+" %")
        
        except ValueError:
            st.text("L'une des valeurs est inconnue du mod√®le de pr√©diction")

    if invert:
        my_bar = st.progress(0)
        if cat=="atp":
            df_pred=df.loc[df["name"]==adv]
        else:
            df_pred=wta.loc[wta["name"]==adv]
        df_min=df_pred.loc[df_pred["advers"]==str(select_nom)]
        
        df_pred=df_pred[["age","ht","name","seed"]]
        df_pred["advers"]=str(select_nom)
        
        minutes=np.mean(df_min["minutes"])
        df_pred["minutes"]=minutes
        
        try:
            df_pred=df_pred.loc[df_pred["age"]==max(df_pred["age"])]
            df_pred=df_pred.drop_duplicates()
        except:
            df_pred["name"]=select_nom
            df_pred["age"]=25
            df_pred["ht"]=175
            df_pred["seed"]=36
            df_pred["advers"]=adv
            df_pred["minutes"]=96
        
        df_pred["surface"]=str(surf)
        df_pred["tourney_level"]=str(lvl)
        
        try :
            df_pred.loc[(df_pred['seed']<100),"classe"] = True
            df_pred.loc[(df_pred['seed']>=100),"classe"] = False
        except : 
            df_pred["classe"] = False
        
        X = df_pred[['age',
                'ht',
                'name',
                'surface',
                'tourney_level',
                'classe',
                'minutes',
                "advers"
                ]]
        
        finalset=[]
        finalace=[]
        finalwin=[]
        
        try:
            
            for i in range (slide):
                    j=int(i/(slide/100))
                    my_bar.progress(j)
                    nb_set=simul_set(X,cat)
                    ace=simul_ace(X,cat)  
                    wins=simul_win(X,cat)
                    finalset.append(nb_set)
                    finalace.append(ace)
                    finalwin.append(wins)
            
            meanset = round(np.mean(finalset),2)
            if meanset>7 :
                meanset=7
            
            meanace = round(np.mean(finalace),2)
            
            meanwin = round(np.mean(finalwin)*100,2)
            
            nb_set_m=str(meanset)
            nb_ace= str(meanace)
            vic = str(meanwin)
            
            st.text("Pr√©vision du nombre de set : " +nb_set_m)
            st.text("Pr√©vision d'aces de "+adv+" : " +nb_ace)
            st.text("Pr√©vision de victoire de "+adv+" : " +vic+" %")
        except TypeError:
            for i in range (slide):
                    j=int(i/(slide/100))
                    my_bar.progress(j)
  
                    wins=simul_win(X,cat)

                    finalwin.append(wins)
            
            meanwin = round(np.mean(finalwin)*100,2)

            vic = str(meanwin)

            st.text("Pr√©vision de victoire de "+adv+" : " +vic+" %")
        
        except ValueError:
            st.text("L'une des valeurs est inconnue du mod√®le de pr√©diction")
            
def simul_set(X,cat):
    pred_set=load("models/predi_set"+str(cat))

    B=X[['age',
        'ht',
        'name',
        'surface',
        'minutes',
        "advers"
        ]]
    B['minutes_var']=np.random.normal(0,10,len(B))
    B['minutes']=B['minutes']+B['minutes_var']
    del B['minutes_var']
    
    pred=pred_set.predict(B)
    prediction=float(*pred)
    return(prediction)
    
def simul_ace(X,cat):
    ace=load("models/predi_ace"+str(cat))

    Y=X[['age',
        'ht',
        'name',
        'surface',
        'minutes',
        "advers"
        ]]  
    Y['minutes_var']=np.random.normal(0,10,len(Y))
    Y['minutes']=Y['minutes']+Y['minutes_var']
    del Y['minutes_var']
    
    pred=ace.predict(Y)
    prediction=float(*pred)
    return(prediction)
    
def simul_win(X,cat):
    win=load("models/predi_win"+str(cat))
    
    try :
        A=X.copy()    
        A['minutes_var']=np.random.normal(0,10,len(A))
        A['minutes']=A['minutes']+A['minutes_var']
        del A['minutes_var']
        del A['classe']
        del A['tourney_level']
        
        pred=win.predict(A)
        prediction=float(*pred)
        return(prediction)
    except:
        pass