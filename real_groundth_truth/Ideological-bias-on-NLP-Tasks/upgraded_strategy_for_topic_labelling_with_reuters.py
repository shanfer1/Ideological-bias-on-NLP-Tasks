# -*- coding: utf-8 -*-
"""Upgraded Strategy for Topic Labelling_with_reuters.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1puVcD_ytjn9s1cYsZ95tuoH22hgkhCBW
"""

import tweepy
import pandas as pd

cols=['screenName','description','location','text']

"""#Topic Labeling into five categories"""

health=['depression','disease','Alzheimer', 'medication','medical', 'hospital', 'vaccine','covid',	'healthcare', 'drug','overdose', 'doctors','patients','consult','ebola', 'treatment', 'covid-19', 'sperm','doctor','recipe','fast food','genealogist','Genetic','gene', 'blood' ,'hospitalized' , 'mental health','prescriptions','hospitals','respitatory', 'smoking weed','tobbaco smocker','ebola', 'virus','bacteria']
politics=['lapd','supreme court','Democrat', 'Biden','trump', 'federal','election','democratic','white house','congress','crown prince','Bush','Obama','FBI','governor','government','senate','candidate', 'politicians', 'freedom', 'President', 'politics', 'governance', 'presidency','republicans','Democrats','legistative','prime minister','federal','world war','trial','lawsuit','attorney','missiles','sheriff','crime']
sports=['football','World cup','tournament', 'Raphael Warnock' ,'Herschel Walker','Olympics','game','postgame', 'game-winner','player','Bowlers','cricket','bowling','batsman','world cup 2022', 'Fiat 500e','race' ,'tom brady','Nick Saban','trophey', 'Messi', 'Ronaldo' ,'soccer','Premier League','FIFA', 'world champion','NBA' ,'sports car',"Shaquille O'Neal",'basketball']
filmandmusic=['filming','science-fiction','drama','web-series','taylor swift','musician','country music','music','artists','jessie james decker','Louis Tomlinson','one direction', 'harry style','filmmaking','film', 'movie','screenwriter', 'Academy Award-winning' ,'TV Special', 'nick jonas', 'jackie chan', 'tom hardy', 'avengers', 'marvel', 'nolan', 'superman', 'batman']
corporatenews=['Red Bull','AIR FORCE','companies','twitter','elon musk', 'Airbnb','amazon','CEO','company', 'Disney World','Walmart', 'HBO']
df_cnn_health= pd.DataFrame(columns=cols, dtype=object)
df_cnn_politics= pd.DataFrame(columns=cols, dtype=object)
df_cnn_sports= pd.DataFrame(columns=cols, dtype=object)
df_cnn_film=pd.DataFrame(columns=cols,dtype=object)
df_cnn_corporate=pd.DataFrame(columns=cols,dtype=object)
df_cnn_list=[df_cnn_corporate,df_cnn_film,df_cnn_health,df_cnn_sports,df_cnn_politics]
keywords=[corporatenews,filmandmusic,health,sports,politics]
topics_list=['corporatenews','film','health','sports','politics']

topicdict={}
for i in range(len(keywords)):
  topicdict[topics_list[i]]=[]
  for j in range(len(keywords[i])):
    topicdict[topics_list[i]].append(keywords[i][j].lower())
print(topicdict)

df_cnn=pd.read_csv('CNN_1000_data_with_dates2.csv')

print(len(keywords),len(df_cnn_list))

for _, row in df_cnn.iterrows():
    text=row['text'].lower()
    keywords_count={'0':0,'1':0,'2':0,'3':0,'4':0}
    for i in range(len(topicdict)):
      keywords=topicdict[topics_list[i]]
      for x in keywords:
        if x in text:
          keywords_count[str(i)]+=1
    key=max(keywords_count, key=keywords_count.get)
    if keywords_count[key]>0:
      print(key,topics_list[int(key)],keywords_count)
      df_cnn_list[int(key)]=df_cnn_list[int(key)].append(row,ignore_index=True)

for x in df_cnn_list:
  print(x.shape[0])

"""#Data Cleaning"""

for i in range(len(df_cnn_list)):
  df_cnn_list[i] = df_cnn_list[i].drop_duplicates('text')

for i  in range(len(df_cnn_list)):
  print("the number of tweets related to topic "+topics_list[i]+" is " + str(df_cnn_list[i].shape[0]))

"""#Adding Topic Column to the Dataframes"""

for i in range(len(df_cnn_list)):
  df_cnn_list[i]['topic']=topics_list[i]

"""#Combining all the topics to a single dataframe"""

df_cnn_topic_combined= pd.DataFrame(columns=cols, dtype=object)
for x in df_cnn_list:
  df_cnn_topic_combined=df_cnn_topic_combined.append(x,ignore_index=True)

print("the total number of rows after collecting all the topics into a single dataframe is "+str(df_cnn_topic_combined.shape[0]))

df_cnn_topic_combined.to_csv('nov_23_df_cnn_topic_combined.csv')

"""#  Topic Labeling of Fox news into 5 categories"""

df_fox=pd.read_csv('FOX_NEWS_1000_data_with_dates2.csv')

df_fox_health= pd.DataFrame(columns=cols, dtype=object)
df_fox_politics= pd.DataFrame(columns=cols, dtype=object)
df_fox_sports= pd.DataFrame(columns=cols, dtype=object)
df_fox_film=pd.DataFrame(columns=cols,dtype=object)
df_fox_corporate=pd.DataFrame(columns=cols,dtype=object)
df_fox_list=[df_fox_corporate,df_fox_film,df_fox_health,df_fox_sports,df_fox_politics]

for _, row in df_fox.iterrows():
    text=row['text'].lower()
    keywords_count={'0':0,'1':0,'2':0,'3':0,'4':0}
    for i in range(len(topicdict)):
      keywords=topicdict[topics_list[i]]
      for x in keywords:
        if x in text:
          keywords_count[str(i)]+=1
    key=max(keywords_count, key=keywords_count.get)
    if keywords_count[key]>0:
      print(key,topics_list[int(key)],keywords_count)
      df_fox_list[int(key)]=df_fox_list[int(key)].append(row,ignore_index=True)

for i  in range(len(df_fox_list)):
  print("the number of tweets from foxnews related to topic "+topics_list[i]+" is " + str(df_fox_list[i].shape[0]))

"""#Data Cleaning"""

for i in range(len(df_fox_list)):
  df_fox_list[i] = df_fox_list[i].drop_duplicates('text')

print("<---------------------- After Cleaning--------------------------")
for i  in range(len(df_fox_list)):
  print("the number of tweets from foxnews related to topic "+topics_list[i]+" is " + str(df_fox_list[i].shape[0]))

"""#Adding topic column to the dataframes"""

for i in range(len(df_fox_list)):
  df_fox_list[i]['topic']=topics_list[i]

"""# Topic Labeling of Reuters news into 5 categories"""

df_reuters=pd.read_csv('Reuters_1000_data_with_dates2.csv')

health = ['covid', 'covid variants', 'pfizer', 'pandemics', 'WHO', 'world health organization', 'infections', 'disease', 'healthcare', 'vaccinations']
politics = ['biden', 'US Government', 'Supreme Court', 'Trump', 'Republican', 'Democrat', 'administration', 'senators', 'Democratic', 'Vice President', 'foreign ministry']
sports = ['soccer', 'FIFAWorldCup', 'national team', 'World Cup', 'FIFA', 'Qatar World Cup', 'Football', 'Skaters', 'Champion']
filmandmusic = ['disney', 'movie', 'singer', 'GRAMMY', 'artist', 'dance', 'choreography', 'concerts', 'film', 'hollywood', 'premiere', 'actors']
corporatenews = ['google', 'apple', 'laid-off', 'tech', 'co-founder', 'companies', 'workforce', 'sales', 'lay-offs', 'tesla', 'wall st', 'e-commerce', 'metaverse', 'technologies', 'recession', 'twitter', 'amazon', 'elon musk']
df_reuters_health= pd.DataFrame(columns=cols, dtype=object)
df_reuters_politics= pd.DataFrame(columns=cols, dtype=object)
df_reuters_sports= pd.DataFrame(columns=cols, dtype=object)
df_reuters_film=pd.DataFrame(columns=cols,dtype=object)
df_reuters_corporate=pd.DataFrame(columns=cols,dtype=object)
df_reuters_list=[df_reuters_corporate,df_reuters_film,df_reuters_health,df_reuters_sports,df_reuters_politics]
keywords=[corporatenews,filmandmusic,health,sports,politics]
topics_list=['corporatenews','film','health','sports','politics']

topicdict={}
for i in range(len(keywords)):
  topicdict[topics_list[i]]=[]
  for j in range(len(keywords[i])):
    topicdict[topics_list[i]].append(keywords[i][j].lower())
print(topicdict)

for _, row in df_fox.iterrows():
    text=row['text'].lower()
    keywords_count={'0':0,'1':0,'2':0,'3':0,'4':0}
    for i in range(len(topicdict)):
      keywords=topicdict[topics_list[i]]
      for x in keywords:
        if x in text:
          keywords_count[str(i)]+=1
    key=max(keywords_count, key=keywords_count.get)
    if keywords_count[key]>0:
      print(key,topics_list[int(key)],keywords_count)
      df_reuters_list[int(key)]=df_reuters_list[int(key)].append(row,ignore_index=True)

"""#Data Cleaning"""

print("<---------------------- After Cleaning--------------------------")
for i  in range(len(df_reuters_list)):
  print("the number of tweets from reuters related to topic "+topics_list[i]+" is " + str(df_reuters_list[i].shape[0]))

"""#Adding topic column to the dataframes"""

for i in range(len(df_reuters_list)):
  df_reuters_list[i]['topic']=topics_list[i]

"""# Combining the Dataframes

#fox news
"""

df_fox_topic_combined= pd.DataFrame(columns=cols, dtype=object)
for x in df_fox_list:
  df_fox_topic_combined=df_fox_topic_combined.append(x,ignore_index=True)
print(df_fox_topic_combined.shape)

df_fox_topic_combined.to_csv('nov_23_df_fox_topic_combined.csv')

"""#reuters news"""

df_reuters_topic_combined= pd.DataFrame(columns=cols, dtype=object)
for x in df_reuters_list:
  df_reuter_topic_combined=df_reuters_topic_combined.append(x,ignore_index=True)
print(df_reuters_topic_combined.shape)

df_reuters_topic_combined.to_csv('nov_23_df_reuters_topic_combined.csv')

