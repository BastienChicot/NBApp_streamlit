# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 15:31:07 2021

@author: basti
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np

df=pd.read_csv("data/data_ML.csv", sep=";")
players_base = pd.read_csv('data/nba_players.csv', sep=";")

def stat_20matchs_splits(full_name):
    code_base = players_base.loc[players_base['full_name'] == full_name].values[0]
    y = code_base[2:3]
    code = ''.join(y)
    annee = '2021'
    
    #Stat 15 derniers matchs
    url = 'https://www.basketball-reference.com/players/a/'+str(code)+'/gamelog/'+str(annee)
    
    try :
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table', {'id' : 'pgl_basic'})
        tab_data = pd.read_html(str(table[0]))[0]
                
        tab_data['url'] = url
        tab_data['joueur'] = code
        tab_data['annee'] = annee
            
    except IndexError:        
        gotdata = 'null'
            
    if annee<"2022" :
        indexNames = tab_data[tab_data['Rk'] == 'Rk' ].index
            # Delete these row indexes from dataFrame
        tab_data.drop(indexNames , inplace=True)
            
    tab_data['Domicile'] = tab_data['Unnamed: 5'].apply(lambda x: '1' if x =="@" else '0')
    
    tab_data[['year','month', 'day']] = tab_data.Date.str.split("-",expand=True,)
    tab_data['year']=str(annee)
    
    tab_data = tab_data[['Date','Opp','PTS','AST','TRB','PF','MP','Domicile']]
    
    tab_data2 = tab_data.tail(20)
    
    url3 = 'https://www.basketball-reference.com/players/a/'+str(code)+'/splits/'
    df_splits_career=[]

    try :
        r = requests.get(url3)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        tab_career=soup.find_all('table', {'id' : 'splits'})
        df_splits_career = pd.read_html(str(tab_career[0]))[0]
        
    except IndexError:        
        gotdata = 'null'
   
    df_splits_career = df_splits_career.iloc[:, np.r_[1:4,29:33]]
           
    df_splits_career = df_splits_career.groupby(axis = 1, level = 1).sum()
    df_splits_career = df_splits_career.set_index(['Value'])
    df_splits_career = df_splits_career.loc[df_splits_career.index.isin(['Home','Road','Monday','Tuesday','Wednesday','Thursday','Friday',
                                                                             'Saturday','Sunday','0 Days','1 Day','2 Days','3+ Days','Eastern',
                                                                             'Western','Atlantic','Central','Northwest','Southeast','Southwest',
                                                                             'Pacific'])] 
    df_splits_career.reset_index(level=0, inplace=True)

    return(tab_data2,df_split_career)

def stat_Opp_team(full_name,Opp):

    A = df.loc[(df["full_name"] == full_name) & (df["Opp"] == Opp)]
    A["PTS_diff"] = round(A['PTS_diff'],2)
    A["AST_diff"] = round(A['AST_diff'],2)
    A["TRB_diff"] = round(A['TRB_diff'],2)
    A = A[['Opp',"Opp_name","Opp_Coach","minutes","Domicile","PTS","AST","TRB","FGA",
           'annee','PTS_diff','AST_diff','TRB_diff']]
    return(A)

def stat_teams (player_team,Opp):
    
    url4 = "https://www.lineups.com/nba/team-rankings/defense"
    r = requests.get(url4)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table', {'class' : 'multi-row-data-table t-stripped'})
    tab_team = pd.read_html(str(table[0]))[0]

    team_code=pd.read_csv('data/code_team.csv', sep=';')
    
    L = pd.merge(tab_team,team_code, on='TEAM')

    M = L.loc[L['Opp_team'] == player_team]
    N = L.loc[L['Opp_team'] == Opp]

    O = M.append(N)
    O = O[['TEAM','PTS ALLOW','REB ALLOW','AST ALLOW','FG ALLOW','3PT ALLOW',
           'OPP FG%','OPP 3PT%','DEF RTG']]
    return(O)