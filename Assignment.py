# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:18:24 2020

@author: aaron
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier 
from sklearn import metrics
data = pd.read_excel("movie_reviews.xlsx")


def Clean_word(word):
    for char in word:
        if char.isalnum() or char == ' ':
            pass
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

def task3_WordDict(Words, DataFrame, WordLen):
    NegativeData = DataFrame[DataFrame["Sentiment"]=="negative"]["Review"]
    PositiveData = DataFrame[DataFrame["Sentiment"]=="positive"]["Review"]
    
    NegativeDict = dict.fromkeys(Words,0)
    for index,value in NegativeData.items():
        value = Clean_word(value)
        value = value.lower()
        value = value.split()
        for word in value:
            if len(word) >=WordLen:
                if word in NegativeDict:
                    NegativeDict[word] = NegativeDict[word] + 1
   
    PositiveDict = dict.fromkeys(Words,0)
    for index,value in PositiveData.items():
        value = Clean_word(value)
        value = value.lower()
        value = value.split()
        for word in value:
            if len(word) >=WordLen:
                if word in NegativeDict:
                    PositiveDict[word] = PositiveDict[word] + 1
                    
    
    
    return NegativeDict,PositiveDict

    
def task4(PDict,NDict,PosRevTot,NegResTot,DataFrame):

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

    
    PositiveWordProb = dict.fromkeys(PDictCount,0)
    NegativeWordProb = dict.fromkeys(NDictCount,0)
    
    for key in list(PositiveWordProb.keys()):
        PositiveWordProb[key] = ((PDictCount[key] + alpha) / (PosRevTot + alpha*2))
        NegativeWordProb[key] = ((NDictCount[key] + alpha) / (NegResTot + alpha*2))
    

    
    PRevPos = PosRevTot / (PosRevTot+NegResTot)  
    PRevNeg = NegResTot / (PosRevTot+NegResTot)
    return NegativeWordProb, PositiveWordProb, PRevNeg, PRevPos
    
    
def task5(Review,PositivePrior,NegativePrior,NegativeDictProb,PositiveDictProb):
    Negative_Probability = 0
    Positive_Probability = 0
    
    
    Review = Clean_word(Review)
    Review = Review.lower()
    Review = Review.split()
    for word in Review:
        if word in list(NegativeDictProb.keys()):
            Positive_Probability = Positive_Probability + math.log(PositiveDictProb[word])
            Negative_Probability = Negative_Probability + math.log(NegativeDictProb[word])
   

    if Positive_Probability > Negative_Probability > math.log(NegativePrior) - math.log(PositivePrior):
        print("Positive")
    else:
        print("Negative")


def task5_MultipleReviews(Test_Set,PositivePrior,NegativePrior,NegativeDictProb,PositiveDictProb):

        

    Reviews = Test_Set["Review"]
    List = []
    for index,Review in Reviews.items():
        Negative_Probability = 0
        Positive_Probability = 0
        Review = Clean_word(Review)
        Review = Review.lower()
        Review = Review.split()
        for word in Review:
            if word in list(NegativeDictProb.keys()):
                Positive_Probability = Positive_Probability + math.log(PositiveDictProb[word])
                Negative_Probability = Negative_Probability + math.log(NegativeDictProb[word])
       
    
        if Positive_Probability - Negative_Probability > math.log(NegativePrior) - math.log(PositivePrior):
            List.append("positive")
        else:
            List.append("negative")
    
    return List
        

def Task6():
    allResults = []
    Means = []
    
    Test_Data, Test_Lables, Training_Data, Training_Lables, Positive_Train_Data, Negative_Train_Data =  Task1()
    


    kf = model_selection.KFold(n_splits=6, shuffle=True)
    for i in range(1,11):

        for train_index, test_index in kf.split(Training_Data):
            # print(train_index)
            # print("-"*50)
            # print(Training_Data.iloc[train_index]["Review"])
            Words = Task2(Training_Data.iloc[train_index], 4000, 4)
            NegativeDict = dict.fromkeys(Words,0)
            PositiveDict = dict.fromkeys(Words,0)
    
    
            NegativeDict, PositiveDict = task3_WordDict(Words, Training_Lables.iloc[train_index], 4)

            
            total_positive = Training_Lables[Training_Lables["Sentiment"]=="positive"].shape[0]
            total_negative = Training_Lables[Training_Lables["Sentiment"]=="negative"].shape[0]
            
            NegativeDictionaryProbabilty, PositiveDictionaryProbabilty, NegativePrior, PositivePrior = task4(PositiveDict,NegativeDict,total_positive,total_negative,Training_Lables)
            
            Predictions = task5_MultipleReviews(Training_Data.iloc[test_index],PositivePrior,NegativePrior,NegativeDictionaryProbabilty,PositiveDictionaryProbabilty)
            # print(Predictions)
            # print(Training_Lables["Sentiment"].iloc[test_index])
            allResults.append(metrics.accuracy_score(Predictions, Training_Lables["Sentiment"].iloc[test_index]))
        print("Accuracy for length " + str(i) + " : "  + str(np.mean(allResults)))
        Means.append(np.mean(allResults))
    
    for j in Means:
        print("Accuracy for length " + str(j) + " : "  + Means[j])


def Main():
    MinimumLen = 4
    MinOccurences = 10000
    
    Test_Data, Test_Lables, Training_Data, Training_Lables, Positive_Train_Data, Negative_Train_Data =  Task1()
    
    Words = Task2(Training_Data,MinOccurences,MinimumLen)
    print(Words)
    
    
    PositiveDict = task3(Words,Positive_Train_Data,MinimumLen)
    print(PositiveDict)
    NegativeDict = task3(Words,Negative_Train_Data,MinimumLen) 
    print(NegativeDict)

    
    total_positive = Positive_Train_Data.shape[0]
    total_negative = Negative_Train_Data.shape[0]
    
    NegativeDictionaryProbabilty, PositiveDictionaryProbabilty, NegativePrior, PositivePrior = task4(PositiveDict,NegativeDict,total_positive,total_negative,Training_Lables)
    
    Pos_Reviews = Training_Lables[Training_Lables["Sentiment"] == "positive"]
    Review = Pos_Reviews.iloc[1].values[0]
    
    task5(Review,PositivePrior,NegativePrior,NegativeDictionaryProbabilty,PositiveDictionaryProbabilty)
    
Task6()
            