# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 13:59:52 2021

@author: basti
"""
## QUINTE pred lineaire = 0.625 == 75%  , 0.41 == 60 % ,0.2 == 50%, 0.85 == 90%, 0.7 == 80%
##/ pred log  0.18 == 50 %, 0.39 == 60% , 0.64 == 75%, 0.72 == 80%, 0.85 == 90 %
import streamlit as st
import pandas as pd

df=pd.read_csv("data/quinte.csv",sep=";")

def page_turf():

    table=df[["N°"," Chevaux","Jockey","S/A","Cotes","pred_gp_log","pred_gp_lin",
           "pred_qt_log","pred_qt_lin"]]
    
    table.loc[(table['pred_gp_log']>=0.65) & (table["pred_gp_lin"]>=0.57),'Gagnant placé'] = "> 75 %"
    table.loc[(table['pred_gp_log']<0.65) & (table["pred_gp_lin"]<0.57),'Gagnant placé'] = "< 75 %"
    table.loc[(table['pred_qt_log']>=0.85) & (table["pred_qt_lin"]>=0.85),'Dans les 5'] = "> 90 %"
    table.loc[(table['pred_qt_log']<0.85) & (table['pred_qt_log']>=0.72) | 
              (table["pred_qt_lin"]<0.85) & (table["pred_qt_lin"]>=0.7),'Dans les 5'] = "> 80 %"
    table.loc[(table['pred_qt_log']<0.72) & (table['pred_qt_log']>=0.64) | 
              (table["pred_qt_lin"]<0.7) & (table["pred_qt_lin"]>=0.625),'Dans les 5'] = "> 75 %"
    table.loc[(table['pred_qt_log']<0.64) & (table['pred_qt_log']>=0.39) | 
              (table["pred_qt_lin"]<0.625) & (table["pred_qt_lin"]>=0.41),'Dans les 5'] = "> 60 %"
    table.loc[(table['pred_qt_log']<0.39) & (table['pred_qt_log']>=0.18) | 
              (table["pred_qt_lin"]<0.41) & (table["pred_qt_lin"]>=0.2),'Dans les 5'] = "> 50 %"
    table.loc[(table['pred_qt_log']<0.18) & 
              (table["pred_qt_lin"]<0.2),'Dans les 5'] = "< 50 %"
    
    table=table[["N°"," Chevaux","Jockey","S/A","Cotes","Gagnant placé","Dans les 5","pred_qt_lin"]]
    table=table.sort_values(by="N°")
    
    def highlight_rows(s):
        return ['background-color: #689D71']*len(s) if s["Dans les 5"]=="> 75 %" else ['background-color: #696969']*len(s)
    
    st.dataframe(table.style.apply(highlight_rows, axis=1))