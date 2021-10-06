# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 16:38:20 2021

@author: basti
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def stat_teams (player_team,Opp):

    url4 = "https://www.lineups.com/nba/team-rankings/defense"
    r = requests.get(url4)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table', {'class' : 'multi-row-data-table t-stripped'})
    tab_team = pd.read_html(str(table[0]))[0]
    tab_team.to_csv("ranking_team.csv",sep=";")

def recup_roster():

    liste_team = {"bos","bkn","atl","ny","phi","tor","gs","lac","lal","pho","sac",
                  "chi","cle","det","ind","mil","cha","mia","orl","wsh","den","min",
                  "okc","por","utah","dal","hou","mem","no","sa"}
    
    df=[]
    for team in liste_team :
        url = "https://www.espn.com/nba/team/roster/_/name/"+str(team)
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table=soup.find_all('table')
        tab_data = pd.read_html(str(table[0]))[0]
        tab_data['Tm']=team
        df.append(tab_data)
        
    final = pd.concat(df)
    
    final['nom']=final['Name'].astype('string')
    final_cleaned = []
    txt = list(final['nom'])
    for i  in txt:
        t = re.sub(r"[0-9]+", "", i)
        final_cleaned.append(re.sub(r'^RT[\s]+', '', t))
    final['full_name'] = final_cleaned
    final['full_name'] = final['full_name'].astype('string')
    
    def nettoyage(df):
        df['full_name'] = df['full_name'].str.replace(u" Jr.", "")
        df['full_name'] = df['full_name'].str.replace(u" Sr.", "")
        df['full_name'] = df['full_name'].str.replace(u" II", "")
        df['full_name'] = df['full_name'].str.replace(u" III", "")
        df['full_name'] = df['full_name'].str.replace(u" IV", "")
        df['full_name'] = df['full_name'].str.replace(u"D.J.", "DJ")
        df['full_name'] = df['full_name'].str.replace(u"P.J.", "PJ")
        df['full_name'] = df['full_name'].str.replace(u"'", "")
    
        df['name_lower'] = df['full_name'].str.lower()
        
    nettoyage(final)
    
    final=final[["full_name","Tm"]]
    
    final.to_csv("roster.csv",sep=";")

#def indice_team(tab_team):

# def maj_roster(full_name,new_team):
#     df=pd.read_csv("data/data_ML.csv",sep=";")
#     simu=pd.read_csv("data/Base_simu.csv",sep=";")
#     df = df.loc[(df['full_name'] == full_name),'Tm']=new_team
#     simu = simu.loc[(simu['full_name'] == full_name),'Tm']=new_team
#     df.to_csv("data/data_ML.csv",sep=";")
#     simu.to_csv("data/Base_simu.csv",sep=";")
    
    