#! /usr/bin/python

import csv
import curses
import nltk

from curses.ascii import isdigit
from nltk.corpus import cmudict

# Class to store information for a name
# Also contains function to determine the number of 
# syllables in a name
class Name:
    """
    Class to store information for a name
    Also contains the setSyls function, which sets the number of syllables
    in the name to self.syls
    """

    def __init__(self, name, sex, count):
        self.name  = name.lower()
        self.sex   = sex
        self.count = count
        self.syls  = 0
    # END def __init__

    def __str__(self):
        return self.name + ', ' + self.sex + ', ' + self.count
    # END __str__

    def setSyls(self, d):
        """
        Calculate the number of syllables in self.name, and
        set the results equal to set.syls
        Inputs:
            d - A dictionary of words from the nltk.corpus library
        Output:
            None
        """
        if self.name in d:
            self.syls = \
                len([x for x in d[self.name][0] if isdigit(str(x[-1]))])
    # END nsyl

# END class Name

def getNameList(namePath):
    """
    Parses a csv to get a list of Name objects
    Inputs:
        namePath - A string containing a path to a csv
                   with Name, Sex, and Count information
    Output:
        A list of Name objects
    """
    nameIdx  = 0
    sexIdx   = 1
    countIdx = 2
    names = []

    data = csv.reader(open(namePath, 'r'))

    return [Name(row[nameIdx], row[sexIdx], row[countIdx]) for row in data]
# END getNameList

def filterNames(nameList):
    """
    Applies various filters so that only desired names are returned
    The filters are:
        1) Only include girls
        2) Only include names whose last character is 'a', 'ah', or 'oh'
        3) Only include names that have two syllables
    Inputs:
        nameList - A list of Name objects
    Outputs:
        A list of Name objects
    """
    # Only girls
    nameList = [n for n in nameList if n.sex == 'F']
    # Only last character = 'a', 'ah', or 'oh'
    nameList = [n for n in nameList if \
        ( n.name[-1] == 'a' ) or \
        ( (n.name[-2] == 'a') and (n.name[-1] == 'h') ) or \
        ( (n.name[-2] == 'o') and (n.name[-1] == 'h') ) ]

    # Only two syllables
    nameList = [n for n in nameList if (n.syls == 2) or (n.syls == 1)]
    return nameList
# END filterNames

def getSyllables(nameList):
    """
    Set the number of syllables for each Name object in nameList
    Inputs:
        nameList - A list of Name objects
    Outputs:
        A list of Name objects
    """
    d = cmudict.dict()
    for n in nameList: n.setSyls(d)
    return nameList
# END getSyllables

def writeToCsv(outputPath, nameList):
    """
    Write results to a csv file
    Inputs:
        outputPath - The path to write the output to
        nameList   - A list of Name objects
    Outputs:
        None
    """
    writer = csv.writer(open(outputPath, 'w'))
    rank = 1
    for n in nameList:
        row = (n.name.title(),str(rank),str(n.count))
        writer.writerow(row)
        rank += 1
    # END for n ...

# END writeToCsv

def main():
    """
    Main function.  The workflow is...
        1. Parse a csv of name data, and put data into Name objects
        2. Get the number of syllables for each name
        3. Filter the list of names to those that are desirable
        4. Write results to a csv file
    Inputs - None
    Outputs - None
    """
    inputPath  = '/home/gary/blog/babyNames/yob2014.txt'
    outputPath = '/home/gary/blog/babyNames/names.csv'

    nameList = getNameList(inputPath)
    nameList = getSyllables(nameList)
    nameList = filterNames(nameList)
    writeToCsv(outputPath, nameList)

# END main

if __name__ == "__main__":
    main()

