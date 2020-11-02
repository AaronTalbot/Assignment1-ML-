# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:18:24 2020

@author: aaron
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("movie_reviews.xlsx")


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
    
    return Test_data,Test_Labels,Train_Data,Train_Labels

def Task2(UncleanedData):
    Reviews = UncleanedData["Review"]
    for index in range(1,10):
        appendstring = ""
        for word in Reviews.iloc[index]:
            for char in word:
                if char.isalnum() or char == ' ':
                    appendstring += char
        appendstring.lower()
        appendstring.split() # creates string into list of string using white space as a sperator 
        Reviews.iloc[index] = appendstring
    
    
    
Te_D, Te_L, Ta_D, Ta_L =  Task1()

Task2(Ta_D)

