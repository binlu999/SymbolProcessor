#!/usr/bin/python

import sys
import csv
import json

#Main method
def main(argv):
    if len(argv) != 2 :
        print ('Usage: symbolprocessor.py <inputfile> <outputfile>')
        sys.exit()

    writeResult(aggregate(readDataFile(argv[0])), argv[1])
    print("The result wrote to %s \nDone!" % argv[1] )

#Read input file and convert to JSON list
def readDataFile(file):
    trades = []
    with open(file) as csvfile:
        fieldnames = ("TimeStamp","Symbol","Quantity","Price")
        reader = csv.DictReader( csvfile,fieldnames)
        for trade in reader:
            trades.extend([{fieldnames[i]:trade[fieldnames[i]] for i in range(len(fieldnames))}])
    
    return trades

#Aggegate symbole from input list
def aggregate(list):
    symbols = dict()
    for x in list:
        if x['Symbol'] in symbols:
            symbols[x['Symbol']].addTrade(x)
        else:
            symbols[x['Symbol']] = Symbol(x)
    return symbols

#Write method to export to output file
def writeResult(data, file):
    with open(file, "w") as f:
        for key, value in sorted(data.items()):
            f.write (key+","+value.toString()+"\n")

#Wrapping class of symbole for each trade operations
class Symbol:
    #<symbol>,<MaxTimeGap>,<Volume>,<WeightedAveragePrice>,<MaxPrice>
    #("TimeStamp","Symbol","Quantity","Price")
    def __init__(self, trade):
        self.earliestTimeStamp = int(trade['TimeStamp'])
        self.latestTimeStamp = int(trade['TimeStamp'])
        self.volume = int(trade['Quantity'])
        self.grandTotal=int(trade['Quantity'])*int(trade['Price'])
        self.maxPrice=int(trade['Price'])

    def addTrade(self,trade):
        if self.earliestTimeStamp > int(trade['TimeStamp']):
            self.earliestTimeStamp = int(trade['TimeStamp'])
        if self.latestTimeStamp < int(trade['TimeStamp']):
            self.latestTimeStamp = int(trade['TimeStamp'])
        self.volume += int(trade['Quantity'])
        self.grandTotal += int(trade['Quantity'])*int(trade['Price'])
        if self.maxPrice < int(trade['Price']):
            self.maxPrice=int(trade['Price'])

    def toString(self):
        return str(self.latestTimeStamp-self.earliestTimeStamp)+","+str(self.volume)+","+str(self.grandTotal/self.volume)+","+str(self.maxPrice)

if __name__ == "__main__":
    main(sys.argv[1:])

