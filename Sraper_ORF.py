#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 10:52:39 2018

@author: user
"""
from bs4 import BeautifulSoup
import requests
from textblob import TextBlob

def main():
  
  #start url
  url_ = 'http://www.orf.at/'
  
  #Get Article names
  page_ = requests.get(url_)
  soup_ = BeautifulSoup(page_.content, 'html5lib')
  
  soup_.find_all('article')
  
  stories_ = []
  
  count_ = 1
  for a in soup_.find_all('a', href=True):
    if ('orf.at/stories' in a['href']) and ('impressum' not in a['href']) and ('/app/' not in a['href']):
      title_ = a.text.replace('\n', '').strip()
      if TextBlob(title_).detect_language()  == 'de':
        title_ = TextBlob(title_).translate(to='en')
      stories_.append([a['href'],title_])
      #with open('articles/title-'+a['href'][-8:-1]+'.txt', 'w') as file_:
      with open('articles/title-'+str(count_)+'.txt', 'w') as file_:
        file_.write(str(title_))
        count_ += 1
      
  count_ = 1
  for b in stories_:
    subpage_ = requests.get(b[0])
    subsoup_ = BeautifulSoup(subpage_.content, 'html5lib')
    
    pall_ = subsoup_.find_all('p')
    context_ = ''
    
    for p_ in pall_:
      context_ += str(p_)
      
    if TextBlob(context_).detect_language()  == 'de':
      context_ = TextBlob(context_).translate(to='en')
      
    #with open('articles/article-'+b[0][-8:-1]+'.txt', 'w') as file_:
    with open('articles/article-'+str(count_)+'.txt', 'w') as file_:  
        file_.write(str(context_).replace('\n', '').strip())
        count_ += 1
  
if __name__ == '__main__':
    main()