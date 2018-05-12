# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
from mitie import *
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster

def MITIE_init():
  path_to_mitie_lib = '/home/user/Documents/Mit ProX DataScience/Case Study 1.2.2: Spectral Clustering: Grouping News Stories/MITIE-master/mitielib'
  sys.path.append(path_to_mitie_lib)

def ReadArticles(N):
  #N=100
  #topics_array=[]
  titles_array=[]
  corpus=[]
  
  for i in range(1,N):
    with open('articles/article-' + str(i) + '.txt','r') as myfile:
      d1 = myfile.read().replace('\n','')
      d1 = d1.lower()
      corpus.append(d1)
      
  for i in range(1,N):
    with open('articles/title-' + str(i) + '.txt','r') as myfile:
      t1 = myfile.read().replace('\n','')
      t1 = t1.lower()
      titles_array.append(t1)
      
  path_to_ner_model = '/home/user/Documents/Mit ProX DataScience/Case Study 1.2.2: Spectral Clustering: Grouping News Stories/MITIE-master/MITIE-models-v0.2/MITIE-models/english/'#german/'
  #entity subset array
  entity_text_array = []
  
  print("loading NER model...")
  ner = named_entity_extractor(path_to_ner_model + 'ner_model.dat')#'total_word_feature_extractor.dat')

  for i in range(1,N):
    #Load the article contents text file and convert it into a list of words
    tokens=tokenize(load_entire_file('articles/article-'+str(i)+'.txt'))
    
    #print(tokens)
    
    #extract all entities known to the ner model
    entities=ner.extract_entities(tokens)
    
    #print(entities)
    
    #extract the actual entitity words and append to the array
    entity_text_array=[]
    for e in entities:
      range_array=e[0]
      tag=e[1]
      score=e[2]
      score_text='{:0.3f}'.format(score)

      entity_text=''.join(str(tokens[j]) for j in range_array)
      entity_text_array.append(entity_text.lower())
      
  #remove duplicate entitites detected
  entity_text_array = np.unique(entity_text_array)
    
  vect = TfidfVectorizer(sublinear_tf=True,max_df=0.5,analyzer='word', stop_words='english',vocabulary=entity_text_array)
  
  corpus_tf_idf = vect.fit_transform(corpus)
  
  #change n_clusters to equal the number of clusters desired
  n_clusters = 5
  #n_components = n_clusters
  
  #cpectral clustering
  spectral = cluster.SpectralClustering(n_clusters=n_clusters,eigen_solver='arpack',affinity='nearest_neighbors',n_neighbors=10)
  spectral.fit(corpus_tf_idf)
  
  if hasattr(spectral,'labels_'):
    cluster_assignments = spectral.labels_.astype(np.int)
    
  for i in range(0,len(cluster_assignments)):
    print(i,cluster_assignments[i],titles_array[i])

N=35
ReadArticles(N)