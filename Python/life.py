#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 18:30:59 2019

@author: taneshmanimaran
"""

import random

luck = [4, 6, 12, 16, 21, 27, 31, 35]
my_randoms=[]
attempt = 0

while attempt <10:
    while len(my_randoms) <= 7:
        j = random.randrange(1,37)
        if j not in my_randoms:
            my_randoms.append(j)
    attempt = attempt + 1    
    test = sorted(my_randoms)
    print (test)
    if luck != my_randoms:
        my_randoms = []

print(attempt)
