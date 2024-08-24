# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random

luck = [5, 18, 33, 36, 38, 40]
my_randoms=[]
attempt = 0

while attempt < 10:
    while len(my_randoms) <= 5:
        j = random.randrange(1,51)
        if j not in my_randoms:
            my_randoms.append(j)
    attempt = attempt + 1 
    
    test = sorted(my_randoms)
    print (test)
    if luck != my_randoms:
        my_randoms = []

print(attempt)
