import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from random import shuffle
from math import sqrt
import warnings
from collections import Counter


def file_read(data, col):
    m = data[col].value_counts()
    val = str(m)
    file = open('/home/thedarkcoder/Desktop/Projects/51 days of ML/KNN/general_file.txt','w+')
    file.write(val)
    file.close()

def class_extraction():
    temp_list = []
    file_new = open('/home/thedarkcoder/Desktop/Projects/51 days of ML/KNN/general_file.txt','r')
    for i in file_new:
        temp_list.append(i[0])
    temp_list.pop(len(temp_list) - 1)
    return sorted(temp_list)

def prepare_class():
    data = {}
    feature_list = class_extraction()
    for i in feature_list:
        a = float(i)
        data[a] = []
    return data

def clear(data, l):
    for i in l:
        data.drop([i], 1, inplace = True)
    return data

def classify_raw_data(data, dict_class):
    for i in data:
        dict_class[i[-1]].append(i[:-1])
    return dict_class

def train_test_split(data, dict_class):
    test_split = 0.15
    shuffle(data)
    train_data = data[:-int((test_split)*len(data))]
    test_data = data[-int((test_split)*len(data)):]
    print(len(test_data), len(train_data))
    # print(test_data)
    return classify_raw_data(train_data,dict_class), test_data


def KNN(data, predict, k = 20):
    if k <= len(data):
        warnings.warn("k is set to value less than total number of groups")
    else:
        distances = []
        for i in data:
            for j in data[i]:
                ecl_dist = np.linalg.norm(np.array(j) - np.array(predict))
                distances.append([ecl_dist,i])
        votes = []
        for i in sorted(distances)[:k]:
            votes.append(i[-1])
        return Counter(votes).most_common(1)[0][0]


def accuracy(data, test, k = 20):
    counter = 0
    for i in test:
        flag = KNN(data, i[:-1], k)
        if flag == i[-1]:
            counter += 1
    acc = (counter * 100)/len(test)
    return acc

if __name__ == "__main__":
    data_set = input("Enter file name : ")
    data_set = pd.read_csv(data_set)
    column = str(input("Enter label column name : "))
    file_read(data_set, column)
    data_cat = prepare_class()
    c = input("Is there anything to replace? Y or N : ")
    if c == 'Y':
        print("Enter 'done' to stop.")
        replacement = input()
        while(replacement != "done"):
            replacement = input()
            data_set.replace('?', -99999, inplace = True)
        print("Enter rows to clear : (Separated by a comma)")
        string = input()
        if string != "":
            l = string.split(",")
            print(len(l))
            data_set = clear(data_set, l)
        test_data = []
        list_data = data_set.values.astype("float64").tolist()
        data_cat,test_data = train_test_split(list_data, data_cat)
        print(accuracy(data_cat, test_data, k = 10))
        l = input("enter a case : ")
        l = l.split(",")
        print(KNN(data_cat, list(map(float, l)), k = 10))
    elif c == 'N':
        print("Enter rows to clear : (Separated by a comma)")
        string = input()
        if string != "":
            l = string.split(",")
            print(len(l))
            data_set = clear(data_set, l)
        test_data = []
        list_data = data_set.values.tolist()
        data_cat,test_data = train_test_split(list_data, data_cat)
        print(accuracy(data_cat, test_data, k = 40))
        
