# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:54:44 2021

@author: basti
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def calcul_indice(annee):
    
    url="https://www.basketball-reference.com/leagues/NBA_"+str(annee)+".html"
    
    r = requests.get(url)
    r_html = r.text
    soup = BeautifulSoup(r_html,'html.parser')
    table_opp=soup.find_all('table',{"id":"per_game-opponent"})
    tab_data_opp = pd.read_html(str(table_opp[0]))[0]
    
    table_team=soup.find_all('table',{"id":"per_game-team"})
    tab_data_team = pd.read_html(str(table_team[0]))[0]
    
    table_adv=soup.find_all('table',{"id":"advanced-team"})
    tab_data_adv = pd.read_html(str(table_adv[0]),header=1)[0]
    
    adv = tab_data_adv[["Team","MOV","SRS","NRtg","eFG%","TOV%"]]
    opp = tab_data_opp[["Team","FG%","3P%","2P%","TRB","AST","STL","BLK","TOV","PTS"]]
    per = tab_data_team[["Team","MP","FG%","3P%","2P%","AST","STL","BLK","TOV","PF","PTS"]]
    
    opp=opp.rename(columns={"FG%":"FG%opp","3P%":"3P%opp","2P%":"2P%opp","TRB":"TRBopp",
                            "AST":"ASTopp","STL":"STLopp","BLK":"BLKopp","TOV":"TOVopp",
                            "PTS":'PTSopp'})
    
    del per["MP"]
    del per["PF"]
    
    import numpy as np
    
    croissant=adv[["Team","TOV%"]]
    del adv["TOV%"]
    adv['TOVopp']=opp["TOVopp"]
    del opp["TOVopp"]
    opp["TOV"]=per["TOV"]
    del per["TOV"]
    
    opp=opp.merge(croissant,on="Team")
    per=per.merge(adv,on="Team")
    
    for col in per.columns:
        new_col=str("score_")+col
        per[new_col]=per[col].rank()
    
    for col in opp.columns:
        new_col=str("score_")+col
        opp[new_col]=opp[col].rank(ascending=False)
        
    per=per.set_index("Team")
    opp=opp.set_index("Team")
    
    calc_per=per[per.columns[13:25]]    
    calc_opp=opp[opp.columns[11:21]]
    calc_per=calc_per.reset_index()
    calc_opp=calc_opp.reset_index()
    
    calc = pd.merge(calc_per,calc_opp,on="Team")
    calc=calc.set_index("Team")
    calc['total']=calc.sum(axis=1)
    calc=calc.reset_index()
    calc.drop(calc.loc[calc['Team']=='League Average'].index, inplace=True)
    
    np.mean(per["PTS"])
    np.std(calc['total'])
    np.var(per['PTS'])
    16/112
    
    ###14% de modif max
    calc["indice"]=(calc["total"]-min(calc['total']))/(max(calc['total'])-min(calc['total']))
    calc["test"]=calc["indice"].rank()
    calc["test"]=calc['test'].astype(int)
    l = list(np.arange(0.85,1.15,0.01))
    score=pd.DataFrame(l)
    score["test"]=score[0].rank()
    
    calc=calc.merge(score,on="test")
    
    calc=calc[["Team",0]]
    calc=calc.rename(columns={0:"indice"})
    
    calc['Team'] = calc['Team'].str.replace(u"*", "")
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
           'Utah Jazz', 'Washington Wizards'],"Tm": ["atl","bos","bkn","cha","chi","cle","dal","den","det","gs","hou","ind","lac","lal",
                                         "mem","mia","mil","min","no","ny","okc","orl","phi","pho","por","sac",
                                         "sa","tor","utah","wsh"]})
                                                       
    calc=calc.merge(Tm,on="Team")
    
    calc=calc[["Tm",'indice']]
    
    calc.to_csv("../data/indice_team.csv",sep=";")