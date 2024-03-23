#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:18:19 2023

@author: marlombey
"""

import sys
import math
import random
from random import choice
from tqdm import tqdm
import matplotlib.pyplot as plt

rou = 5
pinfy = sys.maxsize
ninfy = -1 * sys.maxsize

def Fitness(vector):
    # f(vector) = sum(vector)
    f = sum(vector)
    return f
    
def QVInit(Pop, Dim):
    print('----- STARTING QUANTUM VECTOR INITIALIZATION -----')
    
    qv = []
    v = []
    
    for c in tqdm(range (0, Pop), colour = 'green'):
        v = []
        for d in range(0, Dim):
            x = random.randint(ninfy, pinfy)
            y = random.randint(ninfy, pinfy)
            alpha = round(x / math.sqrt(pow(x,2) + pow(y,2)), rou)
            beta = round(y / math.sqrt(pow(x,2) + pow(y,2)),rou)
            if random.uniform(-1, 1) > 0:
                beta = beta * (-1)
            v.append([alpha, beta])
        qv.append(v)
    return qv


def InitAngle(QVec, Pop, Dim):
    print('----- STARTING QUANTUM ANGLE INITIALIZATION -----')
    
    qa = []
    a = []
    
    for c in tqdm(range(0, Pop), colour = 'blue'): 
        a = []
        for d in range(0, Dim):
            alpha = QVec[c][d][0]
            beta = QVec[c][d][1]
            #theta = round(math.degrees(math.atan(beta/alpha)), r)
            theta = round(math.atan(beta/alpha), rou)
            a.append(theta)
        qa.append(a)
    return qa
 
def QMutation(Qp, Qq, Qr):
    
    qdv = []
    F = random.uniform(0.005, 0.01)
    
    qdv = [ round(p + F * (q - r), rou) for (p,q,r) in zip(Qp, Qq, Qr)]
    
    return qdv
        
def QCrossover(QAngle, QDV, Dim):
    
    CRate = 0.72
    tlv = []
    
    #print('Q ANgle:', QAngle)
    for d in range(Dim):
        if random.uniform(0,1) <= CRate:
            tlv.append(QDV[d])
        else:
            tlv.append(QAngle[d])
    
    return tlv

def QSelection(BTV, BVec, QTV, QVec):
    
    sqv = []
    sbv = []
    
    if Fitness(BTV) >= Fitness(BVec):
        #print('\n{} {} >= {} {}'.format(BTV, Fitness(BTV), BVec, Fitness(BVec)))
        #print('\nSelected: {}'.format(BTV))
        sqv = QTV
        sbv = BTV
    else:
        #print('\n{} {} <= {} {}'.format(BTV, Fitness(BTV), BVec, Fitness(BVec)))
        #print('\nSelected: {}'.format(BVec))
        sqv = QVec
        sbv = BVec
        
    return sqv, sbv

def Observation(QAngle, Dim):
    
    BVec = []
    
    for d in range(Dim):
        if random.uniform(0,1) <= pow(math.cos(QAngle[d]), 2):
            b = 0
        else:
            b = 1
        BVec.append(b)
    
    return BVec
    
########## MAIN ##########
if __name__ == '__main__':
    print('----- STARTING QDE -----')
    
    Pop = 50
    Dim = 100
    MaxG = 500
    g = 0
    bestFitness = []
    bestSolution = []
    print('Population Size: {}, Dimension: {}'.format(Pop, Dim))
    
    QVec = QVInit(Pop, Dim) # initial quantum population generation
    BPop = [] # stores binary population
    
    '''
    for i in range(5):
        print('\n{}. {}'.format(i, QVec[i]))
        print('-' * 50)
    '''
    
    QAngle = InitAngle(QVec, Pop, Dim) # calculating initial quantum angles
    
    #QAngleCopy = QAngle.copy()
    
    '''
    for i in range(5):
        print('\n{}. {}'.format(i, QAngle[i]))
        print('-' * 50)
    '''
    
    print('----- STARTING OBSERVATION  -----')
    for c in tqdm(range(Pop), colour = 'yellow'):
        BPop.append(Observation(QAngle[c], Dim)) # initial binary pop
    
    #BPopCopy = BPop.copy()
    
    '''print('----- FITNESS INITIAL POPULATION -----')
    for c in tqdm(range(Pop), colour = 'cyan'):
        print('Vector: {}. Fitness: {}'.format(BPop[c], Fitness(BPop[c])))'''
    
    '''
    for i in range(5):
        print('\n{}. {}'.format(i, BVec[i]))
        print('-' * 50)
    '''
    
    print('----- STARTING MAIN LOOP -----')
    for g in tqdm(range(MaxG), colour = 'red'):
        fValue = []
        for c in range(Pop):
            exclude = []
            #print('Generation: {} | Vector: {}'.format(g, c))
            exclude.append(c)
            p = choice([i for i in range(Pop) if i not in exclude])
            exclude.append(p)
            q = choice([i for i in range(Pop) if i not in exclude])
            exclude.append(q)
            r = choice([i for i in range(Pop) if i not in exclude])
            #print(p,q,r)
            
            #print('\n----- STARTING QUANTUM MUTATION  -----')
            QDV = QMutation(QAngle[p], QAngle[q], QAngle[r]) # generates donor vector
            #print('Donor Vector: ', QDv)
            
            #print('\n----- STARTING QUANTUM CROSSOVER  -----')
            QTV = QCrossover(QAngle[c], QDV, Dim) # generates trial vector
            #print('Trial Vector:', QTV)
            
            #print('\n----- STARTING OBSERVATION  -----')
            BTV = Observation(QTV, Dim) # generates binary trial vector
            #print('Binary Trial Vector:', BTV)
            
            #print('\n----- STARTING QUANTUM SELECTION  -----')
            sqv, sbv = QSelection(BTV, BPop[c], QTV, QAngle[c]) # generates new angle
            QAngle[c] = sqv
            BPop[c] = sbv
            #print('Updated Theta:', QAngle[c])
            
        fValue = []
        for p in BPop:
            fValue.append(Fitness(p))
            
        maxF = max(fValue)
        maxFIndex = fValue.index(maxF)
        bestV = BPop[maxFIndex]
         
        bestFitness.append(maxF)
        bestSolution.append(bestV)
            
            #print('\n----- STARTING OBSERVATION -----')
            #ob = Observation(QAngle[c], Dim)
            #BPop[c] = ob
            #print(BVec[c])
            
        '''print('\n----- POPULATION G: {} -----'.format(g))
        for i in range(Pop):
            print('Vector {}. Fitness {}'.format(BPop[i], Fitness(BPop[i])))'''
    
    '''print('\n----- FINAL POPULATION -----')
    for i in range(Pop):
        print('Vector {}. Fitness {}'.format(BPop[i], Fitness(BPop[i])))'''
    
    best = []
    fitnessValue = 0
    index = 0
    
    for i in range(Pop):
        if Fitness(BPop[i]) > fitnessValue:
            fitnessValue = Fitness(BPop[i])
            best = BPop[i]
            index = i
    
    x = []
    y = []
    fig, ax = plt.subplots()
    
    for i in range(MaxG):
        plt.clf()
        
        x.append(i+1)
        y.append(bestFitness[i])
        
        plt.xlim(1, MaxG)
        plt.ylim(1, Dim)
        plt.title('Visual Representation of GA Fitness')
        plt.xlabel('Generations')
        plt.ylabel('Fitness Value')
        plt.plot(x,y, c='red', linewidth = 2)
        plt.pause(0.001)
    
    plt.show()
    
    print('\n{}. Best Vector: {}, Fitness: {}'.format(index, best, Fitness(BPop[index])))
        
        
    
                
        
    
    
    
    
    
    
    
    
    
    
    
    
    