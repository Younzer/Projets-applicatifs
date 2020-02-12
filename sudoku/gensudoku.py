from pysat import *
import time, sys
from generateEmptySudoku import *
import random



def decode(x):
    z = x % 10
    x = int(x / 10)
    y = x % 10
    x = int(x / 10)
    return x, y, z

def printSolution(l):
    for v in l:
        if v > 0:
          (x,y,z) = decode(v)
          if x > 0 and x < 10 and y > 0 and y < 10 and z > 0 and z < 10:
            print(x,y,z)

def getSolver(hints):
    solver = Solver()
    solver._config.verbosity = 0
    solver._config.printModel = False
    generateConstraints(solver.addClause)
    for h in hints:
        solver.addClause([h[0]*100+h[1]*10+h[2]])
    return solver

def onlyOneSolution(hints):
    ''' Returns True if with the hints we have only one solution. False if more than one solution and None if anything
    goes wrong '''
    solver = getSolver(hints)
    solver.buildDataStructure()
    result = solver.solve()
    if result == solver._cst.lit_True:
        blockingLiterals = []
        for v in solver.finalModel:
            (x,y,z) = decode(abs(v))
            if x > 0 and x < 10 and y > 0 and y < 10 and z > 0 and z < 10:
                blockingLiterals.append(-v)
        solver = getSolver(hints) # Gets a fresh solver
        solver.addClause(blockingLiterals) # with an additional constraint
        solver.buildDataStructure()
        result = solver.solve()
        return result == solver._cst.lit_False
    return None 

def removableClues(clues):
    ''' Gets the list of removable clues'''
    removable = []
    for clue in clues:
        others = [c for c in clues if c != clue]
        if onlyOneSolution(others):
            removable.append(clue)
    return removable

def readSudokuFile(filename, callback):
    starttime = time.time()
    print("c Opening file {f:s}".format(f=filename))
    
    for line in myopen(filename):
        if not line[0] in ['c','p']:
            callback([l for l in list(map(int,line.split())) if l is not 0]) 

    print("c File readed in {t:03.2f}s".format(t=time.time()-starttime))

if __name__ == "__main__":
    initialClues = []
    readSudokuFile(sys.argv[1], callback = lambda x: initialClues.append(x))
    clues = initialClues.copy()
    nonremovable = []
    while len(clues) > 0:
        random.shuffle(clues)
        print(clues)
        while len(clues) > 0 :
            c = clues.pop()
            print(c)
            if onlyOneSolution(nonremovable + clues): 
                print("removed hint", c)
            else:
                print("non removable", c)
                nonremovable.append(c)
    print("Initial clues :", initialClues)
    print("Minimal clues :", nonremovable)
    print("Clues length :", len(nonremovable))

