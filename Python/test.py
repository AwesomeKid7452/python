#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 23:14:27 2019

@author: taneshmanimaran
"""

import random

luck = [2, 4]
my_randoms=[]
attempt = 0

while luck != my_randoms:
    while len(my_randoms) <= 1:
        j = random.randrange(1,5)
        if j not in my_randoms:
            my_randoms.append(j)
    attempt = attempt + 1    
    test = sorted(my_randoms)
    print (test)
    if luck != my_randoms:
        my_randoms = []

print(attempt)