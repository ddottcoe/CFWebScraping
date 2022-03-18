#import packages
from attr import attrs
import pandas as pd
import numpy as np
import random
from random import randint

import urllib
import urllib.request
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import chromedriver_binary
import requests
import warnings
import csv

from IPython.core.display import clear_output

import os

os.system("cls")

driver = webdriver.Chrome(executable_path=r"/Users/dott/Documents/Python Scripts/ELT Examples/chromedriver/chromedriver")
athletedatasaved=''
website_list = []
start_time = time.time()

print(start_time)
requests = 0

url = ('https://games.crossfit.com/leaderboard/open/2022?view=0&division=1&region=0&scaled=0&sort=0')
driver.get(url)
time.sleep(3+2*random.random())
soup=BeautifulSoup(driver.page_source,'lxml')
website_list.append(soup.text)

#monitor the request
requests += 1
elapsed_time = time.time() - start_time
print('Request:{}; Frequency:{} requests/s'.format(requests, requests/elapsed_time))
clear_output(wait=True)

# Break the loop if the number of requests is greater than expected
if requests > 1000:
    warnings.warn('Number of requests was greater than expected.')
    



""" Open CSV and Write Header Row """


athleteList = []
header = ''



""" retrieve header values """
for record in soup.find('thead').findAll('th'):
    children = record.findChildren('div')
    if children:        
        #print(children[0].get_text())
        if header == '':
            header = children[0].get_text()
        else:
            header = header + ',' + children[0].get_text()
    else:
        #print(record.text)
        if header == '':
            header = record.text
        else:
            header = header + ',' + record.text


headerlist = header.split(',')
finalHeaderList = []


for workout in headerlist:

    if '.' in workout:
        
        finalHeaderList.append(workout + ' Rank')
        finalHeaderList.append(workout + ' Result')


    elif workout == 'POINTS':
        
        otherheaders = 'COUNTRY,REGION,AFFILIATE,AGE,HEIGHT,WEIGHT'.split(',')
        finalHeaderList.extend(otherheaders)
        finalHeaderList.append(workout)
    else:
        
        finalHeaderList.append(workout)



header = ','.join(finalHeaderList)

     


file = open("athletedataKHeng.csv", "w", encoding="utf-8")
file.write(header+'\n')

'''retrieve name'''
for record in soup.find('tbody').findAll('tr'):   
    athletedata = record.find_all("div", attrs={"class":"cell-inner"})[0].text
    athletedata = athletedata + ',' + record.find_all("div", attrs={"class": "first-name"})[0].text + ' ' +  record.find_all("div", attrs={"class": "last-name"})[0].text
    data = record.find_all("li")
    counter = 0 #we need to handle unaffiliated athletes
    personDescription = []
    

    #Code below here is to parse the athlete data 
    #things like age, weight, height etc...
    #there is a lot of conditionals because the format of each person can differ
    #the unit of measure can also differ to so we convert from the metric system
    counter = 0
    for item in data:
        if 'Age' in item.text:
            if len(data) == 4 and counter == 2:
                personDescription.append('')
            agelist = item.text.split(' ')
            age = agelist[1]
            personDescription.append(age)
        if '|' in item.text:
            athleteDataList = item.text.split('|')
            heightList = athleteDataList[0].split(' ')
            if 'cm' in heightList[1]:
                height = float(heightList[0])/2.54
            else:
                height = heightList[0]
            weightList = athleteDataList[1].split(' ')
            if 'kg' in weightList[2]:
                weight = float(weightList[1])*2.2
            else:
                weight = weightList[1]
            personDescription.append(height)
            personDescription.append(weight)
        elif counter == 4:
            if item.text == '':
                personDescription.append('')
                personDescription.append('')
            elif 'cm' or 'in' in item.text:
                
                heightList = item.text.split(' ')
                if 'cm' in heightList[1]:
                    height = float(heightList[0])/2.54
                else: 
                    height = heightList[0]
                personDescription.append(height)
                personDescription.append('')
            elif 'kg' or 'lb' in item.text:
                weightList = item.text.split(' ')
                if 'kg' in weightList[2]:
                    weight = float(weightList[1])*2.2
                else: 
                    weight = weightList[1]
                personDescription.append('')
                personDescription.append(weight)

        else:
            if 'Age' not in item.text:
                personDescription.append(item.text)
        counter+=1
    

    print(personDescription)

    for person in personDescription:
        athletedata = athletedata + ',' + str(person)



    
    '''get total points, only one class in td, therefore loop is not needed'''
    totalpoints = record.find_all('td', attrs={'class': 'total-points'})[0].find('div').text
    
    '''retrieve rank and result across all workouts, score is the common class in all workouts'''
    athletedata = athletedata + ',' + totalpoints
    score = ''
    for points in record.find_all('td', attrs={'class': 'score'}):
        rank = points.find_all('span', attrs={'class': 'rank'})[0].text.strip()[:-2]
        result = points.find_all('span', attrs={'class': 'result'})[0].text
        result = result.strip().replace(')','').replace('(','')
        score = score + rank +','+ result + ','
    athletedata = athletedata + ',' + score[:-1]

    athleteList.append(athletedata)


    

with open("athletedata.csv", "a", encoding="utf-8") as file:
    for item in athleteList:
        file.write("%s\n" %item)