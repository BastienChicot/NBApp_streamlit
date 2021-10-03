# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 15:55:46 2021

@author: basti
"""
import pandas as pd
import numpy as np
from joblib import load

df=pd.read_csv("data/data_ML.csv", sep=";")

corresp_equip = pd.read_csv("data/correspondance_equipe.csv",sep=";")

def calcul_predictions(full_name, Opp, Opp_player,game_start,domicile,month,
                         minutes):
        
    cluster = pd.read_csv("data/cluster.csv", sep=";")
    MLP = load('models/MLP_FGA_pred.joblib')
    Points1 = load('models/Ridge_PTS.joblib')
    Points2 = load('models/Ridge_PTS_simu.joblib')
    Rebounds = load('models/Lin_trb.joblib')
    Assists=load('models/Lin_ast.joblib')

    df1=df.copy()
    df1=df1.loc[df1['full_name']==full_name]
    df1 = df1.loc[df['Opp']==Opp]
    df1 = df1.drop_duplicates(['annee', 'count'],keep= 'last')
    df1=df1.nlargest(1, columns=['annee'])

    if df1.empty :
        df1=df.copy()
        df1=df1.loc[df1['full_name']==full_name]
        df1['Opp']=str(Opp)
        df1 = df1.drop_duplicates(['annee', 'count'],keep= 'last')
        df1=df1.nlargest(1, columns=['annee'])   
    else :
        pass
    
    df1=pd.merge(df1,corresp_equip, on="Tm")
    team_df = cluster.loc[cluster['Key']==Opp]
    team_df=team_df.nlargest(1, columns=['annee'])
    coach_df = cluster.loc[cluster['Key']==Opp]
    coach_df=coach_df.nlargest(1, columns=['annee'])
    player_df = cluster.loc[cluster['Key']==Opp_player]
    player_df=player_df.nlargest(1, columns=['annee'])
        
    df1['cluster_team']=team_df[['cluster']].values
    if df1['cluster_coach'].empty :
        df1['cluster_coach']=coach_df[['cluster']].values
    else :
        pass
    df1['cluster_player']=player_df[['cluster']].values
    
    df1['month']=month
    df1['minutes']=minutes
    df1['GS']=game_start
    df1['Domicile']=domicile
    df2=df1.copy()
    del df2['Tm']
    df2=df2.rename(columns={"Tm_2":"Tm"})
    
    PTS1 = df1[['full_name',
            'Tm',
            'GS','minutes',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'age',
            'FGA_moy','TOV_moy','PF_moy','DRtg',
            'Prod_mean_opp'
            ]]
    
    PTS2 = df2[['full_name',
        'Tm',
        'GS','minutes',
        'month',
        'cluster_coach',
        'cluster_player',
        'age',
        'FGA_moy','TOV_moy','PF_moy',
        'Prod_mean_opp'
        ]]
    
    TRB = df1[['full_name',
            'Tm',
            'GS',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'age',
            'minutes',
            'FGA','TOV','PF','DRtg',
            'Prod_mean_opp'
            ]]
    
    AST = df1[['full_name',
            'Tm',
            'GS',
            'Domicile',
            'month',
            'cluster_coach',
            'cluster_player',
            'age',
            'minutes',
            'FGA','TOV','PF','DRtg',
            'Prod_mean_opp'
            ]]
    
    FGA = df1[['full_name',
            'GS',
            'minutes',
            'count'
            ]]
    
    df1['FGA_pred'] = MLP.predict(FGA)
    df1['AST_pred'] = Assists.predict(AST)
    df1['AST_pred'] = np.exp(df1['AST_pred'])
    df1['TRB_pred'] = Rebounds.predict(TRB)
    df1['TRB_pred'] = np.exp(df1['TRB_pred'])
    df1['PTS_pred_1'] = Points1.predict(PTS1)
    df1['PTS_pred_1'] = np.exp(df1['PTS_pred_1'])
    df1['PTS_pred_2'] = Points2.predict(PTS2)
    df1['PTS_pred_2'] = np.exp(df1['PTS_pred_2'])
    
    prediction=pd.DataFrame(columns={"PTS model 1","PTS model 2",
                                     "FGA","AST","TRB"})
    
    pred_point = df1['PTS_pred_1'].values
    pred_point = pred_point.round(2)
    predp = str(*pred_point)
    
    pred_point_2 = df1['PTS_pred_2'].values
    pred_point_2 = pred_point_2.round(2)
    predp_2 = str(*pred_point_2)
    
    pred_fga = df1['FGA_pred'].values
    pred_fga = pred_fga.round(2)
    predf = str(*pred_fga)
    
    pred_ast = df1['AST_pred'].values
    pred_ast = pred_ast.round(2)
    preda = str(*pred_ast)
    
    pred_reb = df1['TRB_pred'].values
    pred_reb = pred_reb.round(2)
    predr = str(*pred_reb)

    prediction=prediction.append({"PTS model 1":predp,"PTS model 2":predp_2,
                                     "FGA":predf,"AST":preda,"TRB":predr}, ignore_index=True)
    return(predp,predp_2,predf,preda,predr)