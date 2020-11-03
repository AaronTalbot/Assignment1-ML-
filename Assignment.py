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
    
    return WordDict
    
def task4(PDict,NDict,PosRevTot,NegResTot,DataFrame):
    PosRevTot = PosRevTot-1
    alpha = 1
    PDictCount = dict.fromkeys(PDict,0)
    NDictCount = dict.fromkeys(NDict,0)
    Positive_Train_Data = DataFrame[DataFrame["Sentiment"]=="positive"]
    Negative_Train_Data =  DataFrame[DataFrame["Sentiment"]=="negative"]
    
    Positive_Reviews = Positive_Train_Data["Review"]
    Negative_Reviews = Negative_Train_Data["Review"]
    for index,value in Positive_Reviews.items():
        value = Clean_word(value)
        value = value.lower()
        value = value.split()
        for key in list(PDict.keys()):
            if key in value:
                PDictCount[key] += 1
                
    for index,value in Negative_Reviews.items():
        value = Clean_word(value)
        value = value.lower()
        value = value.split()
        for key in list(NDict.keys()):
            if key in value:
                    NDictCount[key] += 1
    print(PDictCount)
    print("======================================")
    print(NDictCount)
    
    PositiveWordProb = dict.fromkeys(PDictCount,0)
    NegativeWordProb = dict.fromkeys(NDictCount,0)
    
    for key in list(PositiveWordProb.keys()):
        PositiveWordProb[key] = ((PDictCount[key] + alpha) / PosRevTot)
        NegativeWordProb[key] = ((NDictCount[key] + alpha) / NegResTot)
    
    print(PositiveWordProb)
    print("="*20)
    print(NegativeWordProb)
    
    PRevPos = PosRevTot / (PosRevTot+NegResTot)  
    PRevNeg = NegResTot / (PosRevTot+NegResTot)
    print(PRevPos)
    print(PRevNeg)
    
    



def Main():
    MinimumLen = 4
    MinOccurences = 7500
    
    Test_Data, Test_Lables, Training_Data, Training_Lables, Positive_Train_Data, Negative_Train_Data =  Task1()
    
    Words = Task2(Training_Data,MinOccurences,MinimumLen)
    PositiveDict = task3(Words,Positive_Train_Data,MinimumLen)
    NegativeDict = task3(Words,Negative_Train_Data,MinimumLen)
    
    total_positive = Positive_Train_Data.shape[0]
    total_negative = Negative_Train_Data.shape[0]
    
    task4(PositiveDict,NegativeDict,total_positive,total_negative,Training_Lables)
        
            
            
Main()
            