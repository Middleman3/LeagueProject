from preproc import dataframes
import numpy as np
from collections import defaultdict
import math
import re
import sys
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import tree
from sklearn.naive_bayes import GaussianNB


# global variables
games = defaultdict(int) #the data fram for all the games chaaracters and the game outcome
cross_section = [] #This will hold the data that will be cross validated
cross_results = [] # Will hold the correct results from the cross section
training_data = [] #data to train the data
training_results = [] #the known results to train with
champ_list = defaultdict(int)

def read_in_list():
    global champ_list
    with open("champ_list.txt","r") as file:
        index = 0
        for x in file:
            x = x.strip()
            champ_list[x] = index
            index += 1
    #print(champ_list)

def set_up_cross_validation(begin,end):
    global games
    global cross_section
    global cross_results
    global training_data
    global training_results
    global champ_list
    index = 0
    #print(champ_list['Lulu'])
    for match in games:
        #print(games[match])
        if (index < int(begin)):
            temp = []
            t_in = 0
            for y in games[match]:
                #print(y)
                if (t_in <10):
                    temp.append(champ_list[y])
                #print(temp)
                t_in += 1
            training_data.append(temp)
            training_results.append(int(games[match][10]))
            index += 1
            continue
        elif ( index >= int(begin) and index <=int(end)):
            index += 1
            temp = []
            t_in = 0
            for y in games[match]:
                if (t_in <10):
                    temp.append(champ_list[y])
                t_in += 1
            cross_section.append(temp)
            cross_results.append(int(games[match][10]))
            continue
        else:
            temp = []
            t_in = 0
            for y in games[match]:
                if (t_in <10):
                    temp.append(champ_list[y])
                t_in+=1
            training_data.append(temp)
            training_results.append(int(games[match][10]))
            index += 1
            continue
    #print(training_data[0])

def load_in_games():
    global games
    temp = []
    match = 1
    for x in dataframes["champs"]:
        #print("this is x")
        #print(x)
        if x == 0:
            for y in dataframes["champs"][x]:
                temp = re.findall('\w+',y) 
                #print(type(temp))
                games[match] = temp
                match += 1
        if x == 1:
            match = 1
            for y in dataframes["champs"][x]:
                temp = re.findall('\w+',y) 
                #print(type(temp))
                games[match] = games[match] + temp                
                match += 1
        #print(games[1])
        if x == 2:
            #print(games[1])
            match = 1
            for y in dataframes["champs"][x]:
                temp = [y]
                #print(games[match])
                #print(type(games[match]))
                #print(temp)
                games[match] = games[match] + temp
                match += 1
    #print(games[1])
#print(dataframes["champs"])
    
def Network():
    global games
    global cross_section
    global cross_results
    global training_data
    global training_results
    scaler = StandardScaler()
    net = MLPClassifier(hidden_layer_sizes=(250,250,250,250,250,250), max_iter=500)
    training_data = np.array(training_data)
    cross_section = np.array(cross_section)
    training_results = np.array(training_results)
    #scaler.fit(training_data)
    #training_data = scaler.transform(training_data)
    #cross_section = scaler.transform(cross_section)
    print(training_data[1],training_results[1])
    net = net.fit(training_data,training_results)
    x = net.predict(cross_section)
    results = open("results.txt", "a")
    print("Neural Network",file = results)
    # MAKE SURE TO ALSO CHANGE THE BELOW WHEN CHANGING THE MLP CLASSIFIER THIS IS TO KEEP TRAK
    # OF WHAT WAS RAN AND ITS OUTCOME
    print(" MLPClassifier ( hidden_layer_sizes = ( 250 , 250 , 250 , 250 , 250 , 250 ) , max_iter=500)", file = results)
    print(classification_report(cross_results,x),file=results)
    np.savetxt('test_neural.dat',x,delimiter = ',',fmt='%s')

def Bayes():
    global games
    global cross_section
    global cross_results
    global training_data
    global training_results
    bay = GaussianNB()
    bay = bay.fit(training_data,training_results)
    x = bay.predict(cross_section)
    results = open("results.txt", "a")
    print("Naive Bay",file = results)
    # MAKE SURE TO ALSO CHANGE THE BELOW WHEN CHANGING THE GaussianNB  THIS IS TO KEEP TRAK
    # OF WHAT WAS RAN AND ITS OUTCOME
    print("GaussianNB()", file = results)
    print(classification_report(cross_results,x),file=results)
    np.savetxt('test_bay.dat',x,delimiter = ',',fmt='%s')
    
def Decision():
    global games
    global cross_section
    global cross_results
    global training_data
    global training_results
    World_tree = tree.DecisionTreeClassifier(random_state=None,criterion='gini',min_samples_split=5)
    World_tree = World_tree.fit(training_data,training_results)
    x = World_tree.predict(cross_section)
    results = open("results.txt", "a")
    print("Decision Tree",file = results)
    # MAKE SURE TO ALSO CHANGE THE BELOW WHEN CHANGING THE DECISION TREE CLASSIFIER THIS IS TO KEEP TRAK
    # OF WHAT WAS RAN AND ITS OUTCOME
    print("DecisionTreeClassifier ( random_state = None,criterion = 'gini',min_samples_split=5)", file = results)
    print(classification_report(cross_results,x),file=results)
    np.savetxt('test_tree.dat',x,delimiter = ',',fmt='%s')
def Baggage_Claim():
    global cross_results
    neural_file = open("test_neural.dat", "r")
    bay_file = open("test_bay.dat","r")
    tree_file = open("test_tree.dat","r")
    n_guess = []
    b_guess = []
    t_guess = []
    index = 0
    for x in neural_file:
        x = x.strip()
        n_guess.append(x)
        index += 1
    index = 0
    for y in bay_file:
        y.strip()
        b_guess.append(y)
        index += 1
    index = 0
    for z in tree_file:
        z.strip()
        t_guess.append(z)
        index += 1
    index = 0
    output = open("bagged_guess","w")
    bag_guess = []
    print(len(t_guess))
    for guesses in t_guess:
        total = 0
        total = int(t_guess[index]) + int(n_guess[index]) + int(b_guess[index])
        if (int(total) >= 2):
            output.write('1')
            bag_guess.append(1)
        else:
            output.write('0')
            bag_guess.append(0)
        index += 1 
    
    results = open("results.txt", "a")
    print("Bagging guess",file = results)
    print(classification_report(cross_results,bag_guess),file=results)
        
def main():
    read_in_list()
    load_in_games()
    set_up_cross_validation(sys.argv[1],sys.argv[2])
    Bayes()
    Decision()
    Network()
    Baggage_Claim()
    print(sys.argv)
if (__name__ == "__main__") :
    main()

