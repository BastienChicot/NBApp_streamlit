# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 13:21:46 2021

@author: basti
"""

import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import SGDRegressor
from joblib import dump

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import PolynomialFeatures

from sklearn.compose import make_column_transformer

# df_atp=pd.read_csv("../data/base_tennis_atp.csv",sep=";")
# df_wta=pd.read_csv("../data/base_tennis_wta.csv",sep=";")

#### PREDICTIONS
def maj_model_tennis(cat):
    df=pd.read_csv("../data/base_tennis_"+str(cat)+".csv",sep=";")
    df=df.loc[df["seed"]!="WC"]
    df=df.loc[df["seed"]!="Q"]
    df.loc[df['seed'].isna(),'seed'] = 100
    
    df_reg=df.copy()
    df_reg["seed"]=df_reg["seed"].astype(float)
    df_reg.loc[(df_reg['seed']<100),"classe"] = True
    df_reg.loc[(df_reg['seed']>=100),"classe"] = False
    
    df_reg = df_reg.dropna()
    
    df_reg.loc[(df_reg['result']=="win"),"win"] = 1
    df_reg.loc[(df_reg['result']=="lose"),"win"] = 0
    
    
    ### MODELE ACE
    # count = df_reg.groupby('name').count().reset_index()
    # count = count[['name',"tourney_id"]]
    # count = count.rename(columns={"tourney_id":"count"})
    # indexNames = count[ (count['count'] < 5)].index
    # count.drop(indexNames , inplace=True)
    
    # df_reg = pd.merge(df_reg, count, on=['name'])
       
    df_w=df_reg[["tourney_id","win","ace",'age',"nb_set",
            'ht',
            'name',
            'surface',
            'tourney_level',
            'classe',
            'minutes',
            "advers"]]
    
    count = df_w.groupby(['name',"advers"]).count().reset_index()
    count = count[['name',"advers","tourney_id"]]
    count = count.rename(columns={"tourney_id":"count"})
    indexNames = count[ (count['count'] < 7.5)].index
    count.drop(indexNames , inplace=True)
    
    df_w = pd.merge(df_w, count, on=['name',"advers"])
    
    df_w=df_w.dropna()
    
    df_w.to_csv("../data/tennis_"+str(cat)+"-master/base_"+str(cat)+"_win.csv",sep=";")

    y = df_w[['ace']]
    
    X = df_w[['age',
            'ht',
            'name',
            'surface',
            'minutes',
            "advers"
            ]]
    
    numeric_data = ['age',
                    'minutes',
                    'ht'
                    ]
    object_data = ['name',
                   'surface',
                   'advers'
                   ]
    
    #PIPELINE
       
    numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler())
    object_pipeline = make_pipeline(OneHotEncoder())
    
    preprocessor = make_column_transformer((numeric_pipeline, numeric_data),
                                           (object_pipeline, object_data))
    
    RFR = make_pipeline(preprocessor, RandomForestRegressor(n_estimators=20,max_depth=100,
                                                            min_samples_leaf=1))
    RFR.fit(X, y)
    
    dump(RFR,"../models/predi_ace"+str(cat))
    
    
    ### MODELE WIN
    
    
    b = df_w[['win']]
    
    A = df_w[['age',
            'ht',
            'name',
            'surface',
            'minutes',
            "advers"
            ]]
    
    numeric_data_w = ['age',
                    'minutes',
                    'ht'
                    ]
    object_data_w = ['name',
                   'surface',
                   "advers"
                   ]
        
    numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler())
    object_pipeline = make_pipeline(OneHotEncoder())
    
    preprocessor = make_column_transformer((numeric_pipeline, numeric_data_w),
                                           (object_pipeline, object_data_w))
    
    MLP = make_pipeline(preprocessor, MLPRegressor(solver="lbfgs",learning_rate="constant",
                                                   hidden_layer_sizes=(10,),alpha=0.001,
                                                   activation="tanh"))
    
    
    MLP.fit(A, b)
    
    dump(MLP,"../models/predi_win"+str(cat))
    
    ### MODELE NB SET
    d = df_w[['nb_set']]
    
    C = df_w[['age',
            'ht',
            'name',
            'surface',
            'minutes',
            "advers"
            ]]
    
    numeric_data_s = ['age',
                    'minutes',
                    'ht'
                    ]
    object_data_s = ['name',
                   'surface',
                   'advers'
                   ]
    
    #PIPELINE
        
    numeric_pipeline = make_pipeline(PolynomialFeatures(2),StandardScaler())
    object_pipeline = make_pipeline(OneHotEncoder())
    
    preprocessor = make_column_transformer((numeric_pipeline, numeric_data_s),
                                           (object_pipeline, object_data_s))
    
    SGD = make_pipeline(preprocessor, SGDRegressor())
    
    SGD.fit(C, d)
    
    dump(SGD,"../models/predi_set"+str(cat))



