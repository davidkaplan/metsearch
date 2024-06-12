#!/usr/bin/env python3

import csv
from collections import defaultdict 
import pprint

'''
Classifications.py

This is a helper script which analyzes the CSV dataset and creates a list of unique 'Classification' types.

Instruction: Manually download the following file to the current directory that this script is in.

https://github.com/metmuseum/openaccess/raw/master/MetObjects.csv

Then run this script from the command line.  You can direct the output to a file:

$ ./classifications.py >> classifications.txt 2>&1

'''

filename = './MetObjects.txt'
objects = []

def openFile():
    with open(filename, mode='r', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            objects.append(row)

def analyze():
    #print(objects[0])
    classifications = defaultdict(lambda: {''})

    for ob in objects:
        class_set = ob['Classification']
        for cl in class_set.split('|'):
            key, sep, value = cl.partition('-')
            if value not in classifications[key]:
                classifications[key].add(value)
                #print(key, classifications[key])

    classifications.pop('')
    #pprint.pp(classifications)
    keys = list(classifications.keys())
    keys.sort()
    print('\n'.join(keys))


if __name__ == '__main__':
    openFile()
    analyze()
