# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 16:38:20 2021

@author: basti
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def stat_teams ():

    url4 = "https://www.lineups.com/nba/team-rankings/defense"
    r = requests.get(url4)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table', {'class' : 'multi-row-data-table t-stripped'})
    tab_team = pd.read_html(str(table[0]))[0]
    tab_team.to_csv("../data/ranking_team.csv",sep=";")

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
    
    url="http://www.espn.com/nba/depth"
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table=soup.find_all('table')
    tab_data = pd.read_html(str(table[0]))[0]
    t=tab_data.stack()
    
    tab = pd.DataFrame(t)
    tab=tab.rename(columns={0:"full_name"})
    nettoyage(tab)
    tab['name'] = tab['name_lower'].str[3:]
    tab['starter']=1
    
    final[['first','name']] = final['name_lower'].str.split(" ",expand=True)
    
    tab=tab[["name","starter"]]
    final = pd.merge(final,tab,on="name",how="outer")
    
    final=final.rename(columns={"starter":"GS"})
    final["GS"].fillna(0, inplace=True)
    final = final[final['POS'].notna()]
    final=final[["full_name","Tm","POS","GS"]]
    final.to_csv("roster.csv",sep=";")
    
def teamstats():
    years=[2017,2018,2019,2020,2021]
    
    final=[]
    for year in years :
        url="https://www.basketball-reference.com/leagues/NBA_"+str(year)+".html"
    
        r = requests.get(url)
        r_html = r.text
        soup = BeautifulSoup(r_html,'html.parser')
        table_adv=soup.find_all('table',{"id":"advanced-team"})
        tab_data_adv = pd.read_html(str(table_adv[0]),header=1)[0]
        tab_data_adv["annee"]=str(year)
        final.append(tab_data_adv)
    
    stats=pd.concat(final)
    stats['Team'] = stats['Team'].str.replace(u"*", "")
    stats = stats[["Team","annee","DRtg"]]
    Tm=pd.DataFrame({"Team":['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets',
           'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers',
           'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons',
           'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
           'Los Angeles Clippers', 'Los Angeles Lakers',
           'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks',
           'Minnesota Timberwolves', 'New Orleans Pelicans',
           'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic',
           'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
           'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
           'Utah Jazz', 'Washington Wizards'],"Opp": ["ATL","BOS","BRK","CHO","CHI","CLE","DAL","DEN","DET","GSW","HOU","IND","LAC","LAL",
                                         "MEM","MIA","MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHO","POR","SAC",
                                         "SAS","TOR","UTA","WAS"]})
                                                        
    stats = stats.merge(Tm, on="Team")
    stats.to_csv("../data/teamstats.csv",sep=";")
