# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 17:02:21 2021

@author: basti
"""
import pandas as pd
import numpy as np
from joblib import load

proj_game=pd.read_csv("data/Base_simu.csv",sep=";")
indice=pd.read_csv("data/indice_team.csv",sep=";")
    
def create_df(data,month):
    data["Opp_code"]=data['POS'].map(str) + data['Opp'].map(str) + data['GS'].map(str)
    
    liste_code = data['Opp_code']
    Opp=(data['Opp'])
    Opp=pd.DataFrame(Opp)
    Opp=Opp.drop_duplicates(["Opp"])
    Opp=str(*Opp["Opp"])
    
    codes=[]
    for code in liste_code:
        df_code=proj_game.loc[proj_game['code']==code]
        df_code=df_code.drop_duplicates(['code'])
        codes.append(df_code)
    X = pd.concat(codes)
    X = X[["code","cluster_def"]]
    X= X.rename(columns={"code":"Opp_code","cluster_def":"cluster_player"})
    Y = proj_game.loc[proj_game['Tm']==Opp]
    Y=Y[["Tm","cluster_c"]]
    Y = Y.drop_duplicates(["cluster_c"])
    Y = Y.rename(columns={"Tm":"Opp","cluster_c":"cluster_coach"})

    data=pd.merge(data,X,on="Opp_code",how="left")
    data=pd.merge(data,Y,on="Opp",how="left")
    data = data.drop_duplicates(['full_name','Tm'],keep= 'last')
    data['cluster_player']=data['cluster_player'].fillna(0)
    
    data['month']=month
    data['bonus_malus']=0

    return(data)
    
def simulation_match(data):

    model=load("models/Ridge_PTS_simu.joblib")
    
    data['minutes_var']=np.random.normal(0,3,len(data))
    data['minutes']=data['minutes']+data['minutes_var']
    del data['minutes_var']
    
    data['score']=model.predict(data)
    data['bonus_malus']=np.random.normal(1, 5.2, len(data))
    data['ptspred']=np.exp(data['score'])
    data['pts_pred']=data['ptspred']+data['bonus_malus']
    data["score_tot"]=sum(data["pts_pred"])
    data["score_fin"]=(data['score_tot']/sum(data["minutes"]))*240
    return(data)

def simul_game(equipe,Opp,df_team,df_Opp, month):
    
    bilan=pd.DataFrame(columns={"Team","Opp","Victoire","Défaite","score_team",
             "score_opp"})
    
    try:
        month=month
        df_team = df_team[['full_name',
                            'Tm',
                            'GS','minutes',
                            'month',
                            'cluster_coach',
                            'cluster_player',
                            'age',
                            'FGA_moy','TOV_moy','PF_moy',
                            'Prod_mean_opp'
                            ]]
        df_Opp = df_Opp[['full_name',
                            'Tm',
                            'GS','minutes',
                            'month',
                            'cluster_coach',
                            'cluster_player',
                            'age',
                            'FGA_moy','TOV_moy','PF_moy',
                            'Prod_mean_opp'
                            ]]
        df_team=simulation_match(df_team)
        df_Opp=simulation_match(df_Opp) 
            
        score_t = df_team.drop_duplicates(['score_fin'],keep="last")
        score_O = df_Opp.drop_duplicates(['score_fin'],keep="last")
        
        ind_team=indice.loc[indice["Tm"]==equipe]
        ind_opp=indice.loc[indice["Tm"]==Opp]
   
        score_team=float(score_t['score_fin'])*float(ind_team['indice'])
        score_Opp=float(score_O['score_fin'])*float(ind_opp['indice'])
        
        if score_team>score_Opp:
            Victoire=1
            Defaite=0
        else:
            Defaite=1
            Victoire=0
        bilan=bilan.append({"Team":equipe,"Opp":Opp,"score_team":score_team,
                            "score_opp":score_Opp,"Victoire":Victoire,"Défaite":Defaite},ignore_index=True)
        return(bilan)

    except:
            pass
            

