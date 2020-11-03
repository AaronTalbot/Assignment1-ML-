# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:18:24 2020

@author: aaron
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("movie_reviews.xlsx")

def Clean_word(word):
    for char in word:
        if char.isalnum() or ' ':
            break
        else:
            word = word.replace(char,"")
    return word


def Task1():
    Test_data = data[data["Split"]=="test"][["Review"]]
    Test_Labels = data[data["Split"]=="test"][["Review","Sentiment"]]
    Train_Data = data[data["Split"]=="train"][["Review"]]
    Train_Labels = data[data["Split"]=="train"][["Review","Sentiment"]]
    
    Positive_Test_Data = Test_Labels[Test_Labels["Sentiment"]=="positive"]
    Negative_Test_Data = Test_Labels[Test_Labels["Sentiment"]=="negative"]
    Positive_Train_Data = Train_Labels[Train_Labels["Sentiment"]=="positive"]
    Negative_Train_Data = Train_Labels[Train_Labels["Sentiment"]=="negative"]

    print("Positive reviews in the test data are : " + str(Positive_Test_Data.shape[0]))
    print("Negative reviews in the test data are : " + str(Negative_Test_Data.shape[0]))
    print("Positive reviews in the train data are : " + str(Positive_Train_Data.shape[0]))
    print("Negative reviews in the train data are : " + str(Negative_Train_Data.shape[0]))
    
    return Test_data,Test_Labels,Train_Data,Train_Labels, Positive_Train_Data, Negative_Train_Data

def Task2(UncleanedData, MinOccurences, MinLength):
    Reviews = UncleanedData["Review"]
    Words = []
    WordOccurences = {}
    for index,value in Reviews.items():
        value = Clean_word(value)
        value = value.lower()
        value = value.split()
        for word in value:
            if len(word) >= MinLength:
                if word in WordOccurences:
                    WordOccurences[word] = WordOccurences[word] + 1
                else:
                    WordOccurences[word] = 1
                                  
    for key in list(WordOccurences.keys()): 
        if WordOccurences[key] >= MinOccurences:
            Words.append(key)
            
            
    return Words
            
    

            
                

def task3(Words, DataFrame, WordLen):
    WordDict = dict.fromkeys(Words,0)
    # print(DataFrame.head())
    ReviewDataFrame = DataFrame["Review"]
    # print("=============================================================")
    # print(ReviewDataFrame.head())
    for index,value in ReviewDataFrame.items():
        value = Clean_word(value)
        value = value.lower()
        value = value.split()
        for word in value:
            if len(word) >=WordLen:
                if word in WordDict:
                    WordDict[word] = WordDict[word] + 1
    
    print(WordDict)
    
    



def Main():
    MinimumLen = 4
    MinOccurences = 7500
    
    Test_Data, Test_Lables, Training_Data, Training_Lables, Positive_Train_Data, Negative_Train_Data =  Task1()
    
    Words = Task2(Training_Data,MinOccurences,MinimumLen)
    task3(Words,Positive_Train_Data,MinimumLen)
    task3(Words,Negative_Train_Data,MinimumLen)

        
            
            
Main()
            