# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:36:59 2021

@author: basti
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def recup_tab(url):
        
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table')
    tab_data = pd.read_html(str(table[0]))[0]
      
    tab=tab_data[1]
    tab.columns = tab.iloc[0] 
    
    t=pd.DataFrame(tab.str.split(',',expand=True))
    t.columns = t.iloc[0] 
    
    t=t.loc[t["tourney_id"]!="tourney_id"]
    return(t)

def create_fichier(year):
    
    url_atp="https://github.com/JeffSackmann/tennis_atp/blob/master/atp_matches_"+str(year)+".csv"
    url_wta="https://github.com/JeffSackmann/tennis_wta/blob/master/wta_matches_"+str(year)+".csv"
    
    wta=recup_tab(url_wta)
    
    atp=recup_tab(url_atp)
    
    wta.to_csv("../data/tennis_wta-master/wta_matches_"+str(year)+".csv")
    atp.to_csv("../data/tennis_atp-master/atp_matches_"+str(year)+".csv")

def nettoyage(cat):
    annees=[2006,2007,2008,2009,2010,2011,2012,2013,2014,
        2015,2016,2017,2018,2019,2020,2021]

    list_df=[]
    
    for annee in annees:
        
        test= pd.read_csv("../data/tennis_"+str(cat)+"-master/"+str(cat)+"_matches_"+str(annee)+".csv", sep=",")
        try:
            del test["Unnamed: 0"]
        except:
            pass
        
        w_table=test.iloc[:,[0,1,2,3,4,5,8,10,11,12,13,14,23,25,26,27,28,18]]
        
        l_table=test.iloc[:,[0,1,2,3,4,5,16,18,19,20,21,22,23,25,26,36,37,10]]
        
        w_table["result"]="win"
        l_table["result"]="lose"
        
        w_table=w_table.rename(columns={'winner_seed':"seed", 'winner_name':"name", 
                                        'winner_hand':"hand",'winner_ht':"ht",
                                        'winner_ioc':"ioc", 'winner_age':"age",
                                        "w_ace":"ace","w_df":"df","loser_name":"advers"})
        
        l_table=l_table.rename(columns={'loser_seed':"seed", 'loser_name':"name", 
                                        'loser_hand':"hand",'loser_ht':"ht",
                                        'loser_ioc':"ioc", 'loser_age':"age",
                                        "l_ace":"ace","l_df":"df","winner_name":"advers"})
        
        df=w_table.append(l_table)
        df["annee"]=annee
        df["nb_set"]=df["score"].str.count("-")
        
        season=df.groupby(['name',"annee"]).mean()
        season=season.reset_index()
        
        season=season[["name","annee","minutes","ace","df","nb_set"]]
        
        season=season.rename(columns={'minutes':"minutes_sea", 'ace':"ace_sea", 
                                        'df':"df_sea",'nb_set':"nb_set_sea"})
        
        df=df.merge(season,on=["name","annee"])
    
        list_df.append(df)
        
    df_final=pd.concat(list_df)
    
    career=df_final.groupby(['name']).mean()
    career=career.reset_index()
    career=career[["name","minutes","ace","df","nb_set"]]
    
    career=career.rename(columns={'minutes':"minutes_car", 'ace':"ace_car", 
                                    'df':"df_car",'nb_set':"nb_set_car"})
    df_final=df_final.merge(career,on="name")
    
    df_final["minutes_diff_c"]=df_final["minutes"]-df_final["minutes_car"]
    df_final["minutes_diff_s"]=df_final["minutes"]-df_final["minutes_sea"]
    df_final["ace_diff_c"]=df_final["ace"]-df_final["ace_car"]
    df_final["ace_diff_s"]=df_final["ace"]-df_final["ace_sea"]
    df_final["df_diff_c"]=df_final["df"]-df_final["df_car"]
    df_final["df_diff_s"]=df_final["df"]-df_final["df_sea"]
    df_final["nb_set_diff_c"]=df_final["nb_set"]-df_final["nb_set_car"]
    df_final["nb_set_diff_s"]=df_final["nb_set"]-df_final["nb_set_sea"]
        
    df_final.to_csv("../data/base_tennis_"+str(cat)+".csv",sep=";")

    