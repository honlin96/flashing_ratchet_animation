# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 23:51:40 2020

@author: honlin
"""
import math
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

probA = 0.5
probB = 0.1
probC = 0.75
epsilon = 0.01

global gameA, gameB
initial_state = np.array([1,0,0])
gameA = np.array([[0,probA + epsilon, probA - epsilon],[probA - epsilon,0,probA + epsilon],[probA +epsilon,probA - epsilon,0]])
gameB = np.array([[0,1-probC + epsilon ,probC - epsilon],[probB - epsilon,0,1-probC+epsilon],[1-probB+epsilon,probC-epsilon,0]])

def random_newstate(state):
    state = np.transpose(state)
    newstate = 0.5*(gameA + gameB) @ state
    return np.transpose(newstate)

def periodic_newstate(state,period,cycle):
    state = np.transpose(state)
    if period % cycle == 0:
        newstate = gameA @ state
    else:
        newstate = gameB @ state
    return np.transpose(newstate)

def majority_newstate(state):
    state = np.transpose(state)
    if state[0] >=0.5:
        newstate = gameA @ state
        isgameA = True
    else:
        newstate = gameB @ state
        isgameA = False
    return newstate,isgameA

def avg_capital(old_avg_capital,state,isgameA):
    gameA_win_prob = probA - epsilon
    gameB_win_prob = probB*(state[0]) + probC*(1-state[0]) - epsilon
    if isgameA:
        new_avg_capital = old_avg_capital + 2*gameA_win_prob - 1
    else:
        new_avg_capital = old_avg_capital + 2*gameB_win_prob - 1
    return new_avg_capital

def whichgame():
    game = random.random()
    if game < 0.5:
        return True
    else:
        return False

def isgoingforward(isgameA,state,distance_travelled):
    #obtain the feedback once the potential has been executed, and compute the new state
    forwardA_mat = np.array([[0,0, probA - epsilon],[probA - epsilon,0,0],[0,probA - epsilon,0]])
    backwardA_mat = np.array([[0,probA + epsilon,0],[0,0,probA + epsilon],[probA +epsilon,0,0]])
    forwardB_mat = np.array([[0,0,probC - epsilon],[probB - epsilon,0,0],[0,probC-epsilon,0]])
    backwardB_mat = np.array([[0,1-probC + epsilon ,0],[0,0,1-probC+epsilon],[1-probB+epsilon,0,0]])
    
    state = np.transpose(state)
    forward = random.random()
    if isgameA:
        if forward < probA - epsilon:
            newstate = forwardA_mat @ state
            distance_travelled += 1
        else:
            newstate = backwardA_mat @ state
            distance_travelled -= 1
    else:
        if forward <  probB*(state[0]) + probC*(1-state[0]) - epsilon:
            newstate = forwardB_mat @ state
            distance_travelled += 1
        else:
            newstate = backwardB_mat @ state
            distance_travelled -= 1
    normalisation = np.ones(3) @ newstate
    newstate = (1/normalisation) * newstate
    return np.transpose(newstate), distance_travelled

def notconverge_newstate(state):
    state = np.transpose(state)
    if state[0] >= 5/13:
        newstate = gameA @ state
        isgameA = True
    else:
        newstate = gameB @ state
        isgameA = False
    return newstate,isgameA

def feedback_newstate(state,distance_travelled):
    if state[0] == 1:
        #gameA
        isgameA = True
        newstate,distance_travelled = isgoingforward(isgameA,state,distance_travelled)
    else:
        #gameB
        isgameA = False
        newstate,distance_travelled = isgoingforward(isgameA,state,distance_travelled)
    return newstate,isgameA,distance_travelled

def predict_newstate(state,distance_travelled):
    #play game B if pi_0 hasn't converge, else play game A
    if state[0] > 0.5:
        #gameA
        isgameA = True
        newstate,distance_travelled = isgoingforward(isgameA,state,distance_travelled)
    else:
        #gameB
        isgameA = False
        newstate,distance_travelled = isgoingforward(isgameA,state,distance_travelled)
    return newstate,isgameA,distance_travelled
        
random_avgcapital_mat = []
periodic_avgcapital_mat = []
majority_avgcapital_mat = []
converge_avgcapital_mat = []

isgameAmat = []
majorityisgameAmat = []
convergeisgameAmat = []  
feedbackisgameAmat = []
time = 50
cycle = 2
for i in range(time):
    if i == 0:
        random_state = random_newstate(initial_state)
        isgameA = whichgame()
        isgameAmat.append(isgameA)
        random_avgcapital = avg_capital(0,random_state,isgameA)
        random_avgcapital_mat.append(random_avgcapital)
        
        #periodic
        periodic_state = periodic_newstate(initial_state,i,cycle)
        periodic_avgcapital = avg_capital(0,periodic_state,True)
        periodic_avgcapital_mat.append(periodic_avgcapital)
        
        #majorityrules
        majority_state,isgameA = majority_newstate(initial_state)
        majorityisgameAmat.append(isgameA)
        majority_avgcapital = avg_capital(0,majority_state,isgameA)
        majority_avgcapital_mat.append(majority_avgcapital)
        
        #notconvergerule
        converge_state,isgameA = notconverge_newstate(initial_state)
        convergeisgameAmat.append(isgameA)
        converge_avgcapital = avg_capital(0,converge_state,isgameA)
        converge_avgcapital_mat.append(converge_avgcapital)
        
    else:
        random_state = random_newstate(random_state)
        isgameA = whichgame()
        isgameAmat.append(isgameA)
        random_avgcapital = avg_capital(random_avgcapital,random_state,isgameA)
        random_avgcapital_mat.append(random_avgcapital)
        
        #periodic
        periodic_state = periodic_newstate(periodic_state,i,cycle)
        if (i%cycle) == 0:
            periodic_avgcapital = avg_capital(periodic_avgcapital,periodic_state,True)
        else:
            periodic_avgcapital = avg_capital(periodic_avgcapital,periodic_state,False)
        periodic_avgcapital_mat.append(periodic_avgcapital)
        
        #majorityrules
        majority_state,isgameA = majority_newstate(majority_state)
        majorityisgameAmat.append(isgameA)
        majority_avgcapital = avg_capital(majority_avgcapital,majority_state,isgameA)
        majority_avgcapital_mat.append(majority_avgcapital)
        
        #notconvergerule
        converge_state,isgameA = notconverge_newstate(converge_state)
        convergeisgameAmat.append(isgameA)
        converge_avgcapital = avg_capital(converge_avgcapital,converge_state,isgameA)
        converge_avgcapital_mat.append(converge_avgcapital)
        
#calculate the average capital for feedback
sample_no = 10000
feedback_avgcapital_mat = np.zeros(time)
for sample in range(1,sample_no):
    feedback_actcapital_mat = []
    for i in range(time):
        if i == 0:
            #feedback
            feedback_state,isgameA,distance_travelled = feedback_newstate(initial_state,0)
            #feedbackisgameAmat.append(isgameA)
            feedback_actcapital_mat.append(distance_travelled)
        else:
            #feedback
            feedback_state,isgameA,distance_travelled = feedback_newstate(feedback_state,distance_travelled)
            #feedbackisgameAmat.append(isgameA)
            feedback_actcapital_mat.append(distance_travelled)
    feedback_avgcapital_mat += feedback_actcapital_mat 
    
feedback_avgcapital_mat = feedback_avgcapital_mat/sample_no 


predict_avgcapital_mat = np.zeros(time)
initial_predict_state = np.array([1/3,1/3,1/3])
for sample in range(1,sample_no):
    predict_actcapital_mat = []
    predict_gameA_mat = []
    predict_state_mat = []
    for i in range(time):
        if i == 0:
            #predict
            predict_state,isgameA,distance_travelled = predict_newstate(initial_predict_state,0)
            predict_actcapital_mat.append(distance_travelled)
            predict_gameA_mat.append(isgameA)
            predict_state_mat.append(predict_state)
        else:
            #predict
            predict_state,isgameA,distance_travelled = predict_newstate(predict_state,distance_travelled)
            predict_actcapital_mat.append(distance_travelled)
            predict_gameA_mat.append(isgameA)
            predict_state_mat.append(predict_state)
    predict_avgcapital_mat += predict_actcapital_mat 
predict_avgcapital_mat = predict_avgcapital_mat/sample_no

xaxis = range(1,time+1)
lowerbound = np.zeros(time)
plt.figure(1)
plt.grid()
plt.plot(xaxis, random_avgcapital_mat, 'r-x', label = 'Random')
plt.plot(xaxis,periodic_avgcapital_mat,'b-x', label = 'Periodic')
plt.plot(xaxis,majority_avgcapital_mat,'y-x', label = 'Majority')
#plt.plot(xaxis,converge_avgcapital_mat,'c-x',label = 'Converge')
plt.plot(xaxis,feedback_avgcapital_mat, 'g-x',label = 'Feedback')
plt.plot(xaxis,predict_avgcapital_mat, 'm-x',label = 'Predict')
#plt.plot(xaxis,Average_B,label = 'Game B only')
plt.title('Average distance travelled as a function of time')
plt.xlabel('Time,t')
plt.ylabel('Average distance travelled,<x(t)>')
plt.legend(prop = {'size':10})
plt.show()
    
def cartesian2trilinear(coords_arr):
    # k1 = ax/(ax+by+cz), k2 = by/(ax+by+cz) 
    # P = k1*vec{A} + k2 *vec{B} 
    a = 1
    b = 1
    c = b 
    
    k1 = a*coords_arr[1]/(a*coords_arr[0]+b*coords_arr[1]+c*coords_arr[2])
    k2 = b*coords_arr[2]/(a*coords_arr[0]+b*coords_arr[1]+c*coords_arr[2])
    
    x = 0.5*k1 + 1*k2
    y = (math.sqrt(3)/2)*k1 + 0*k2
    return x,y

xcood = []
ycood = []
for coords_arr in predict_state_mat:
    x,y = cartesian2trilinear(coords_arr)
    xcood.append(x)
    ycood.append(y)

# Create triangulation.
x = np.asarray([0, 1, 0.5])
y = np.asarray([0, 0, math.sqrt(3)/2])
triang = mtri.Triangulation(x, y)
xcood = np.concatenate(([0.5],xcood))
ycood = np.concatenate(([0.28867513459481287],ycood))
plt.figure(2)
plt.grid()
plt.title('Simplex')
plt.triplot(triang, 'ko-')
plt.plot(xcood,ycood,'xr-')
#plt.plot(0.5,0.28867513459481287,'x')
plt.annotate('[1 0 0]',(0,0), textcoords = 'offset points', xytext=(0,10),ha = 'right')
plt.annotate('[0 1 0]',(0.5,math.sqrt(3)/2), textcoords = 'offset points', xytext=(30,0),ha = 'center')
plt.annotate('[0 0 1]',(1,0), textcoords = 'offset points', xytext=(0,10),ha = 'left')
plt.annotate('[1/3 1/3 1/3]',(0.5,0.28867513459481287),textcoords = 'offset points', xytext=(0,10),ha = 'center')
# zip joins x and y coordinates in pairs
#counter = 0
#for x,y in zip(xcood,ycood):
#    label = str(predict_state_mat[counter])
#    plt.annotate(label, # this is the text
#                 (x,y), # this is the point to label
#                 textcoords="offset points", # how to position the text
#                 xytext=(0,10), # distance from text to points (x,y)
#                 ha='center') # horizontal alignment can be left, right or center
#    counter += 1

def entropy(probability_state):
    entropy = 0
    for p in probability_state:
        entropy += -1*p*math.log(p,2)
    return entropy

initial_entropy = entropy(initial_predict_state)
entropy_mat = [initial_entropy]
for prob_state in predict_state_mat:
    h = entropy(prob_state)
    entropy_mat.append(h)
xaxis2 = range(time+1)
plt.figure(3)
plt.grid()
plt.title('Shannon Entropy as a function of time')
plt.xlabel('Time,t')
plt.ylabel('Shannon entropy, H(\\rho)')
plt.plot(xaxis2,entropy_mat,'-x')