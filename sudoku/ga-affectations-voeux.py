
import random
import array
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import sys


def buildMatrixFromExcel(filename):
    df = pd.read_excel(filename)

    studentsNumber = {}
    studentsNumberToName = []
    voeux = {}
    projectsSelectedBy = {}
    projectsNumber = {}
    projectsNumberToName = []
    for i in range(0,22):
        nom = df['Nom - Prénom'][i]
        studentsNumber[nom] = len(studentsNumber)
        studentsNumberToName.append(nom)
        assert(studentsNumberToName[studentsNumber[nom]]==nom)
        voeux[nom] = []
        col = 0
        for j in df.columns[3:7]:
            project = df[j][i]
            if pd.isnull(project): break # Pas de voeux exprimé
            voeux[nom].append(project) # L'ordre de preference est conservé
            col += 1
            if project not in projectsNumber:
                projectsSelectedBy[project] = [nom]
                projectsNumber[project] = len(projectsNumber)
                projectsNumberToName.append(project)
            else:
                projectsSelectedBy[project].append(nom)

    matrixChoices = np.full(shape = (len(studentsNumber),len(projectsNumber)), fill_value = -1)
    for s in studentsNumber:
        r = 0
        for p in voeux[s]:
            matrixChoices[studentsNumber[s], projectsNumber[p]] = r
            r += 1

    #print("Projets sélectionnés")
    #print("--------------------")
    #for p in sorted([p for p in projectsSelectedBy], key=lambda x: len(projectsSelectedBy[x]), reverse=True):
    #    print(len(projectsSelectedBy[p]), ":",  p)

    return (matrixChoices, studentsNumber, studentsNumberToName, projectsNumber, projectsNumberToName, voeux)


class Configuration():
    RANDOMSEED = 1234
    POPULATIONSIZE = 150
    NOBJECTS = 22 # How many students
    MAXWEIGHTS= 60 # How many projects (max)
    MUTATIONRATE = 20 # 5% de mutation rate
    WEIGHTS = array.array('f')
    COSTS = array.array('f')

    def __init__(self):
        random.seed(self.RANDOMSEED)
        (self._matrixChoices, 
        self._studentsNameToNumber, self._studentsNumberToName, self._projectsNameToNumber,
        self._projectsNumberToName, self._orderedStudentsWishes) = buildMatrixFromExcel('voeux.xlsx')

config = Configuration()
print(config._projectsNumberToName)
print(config._studentsNumberToName)

class Chromosome:
    _value = None

    def __init__(self, initialValue=None):
        if initialValue is not None:
            self._value = initialValue
        else:
            self._initRandomOne()

    def fitness(self):
        pass

    def reproduceWith(self, other):
        pass

    def mutation(self):
        pass

    def _initRandomOne(self):
        pass

    def __repr__(self):
        return str(self._value)


class ChromosomeProjects(Chromosome):
    _weight = None
    _cost = None
    _penalties = [0,70, 501, 2001]
    def __init__(self, initialValue=None):
        global config
        config.NOBJECTS = len(config._studentsNumberToName)
        self._projectNumberSelected = np.zeros(len(config._projectsNumberToName))
        self._weight = 0
        self._cost = 0
        self._penalty = 0
        if initialValue is not None:
            self._value = initialValue
        else:
            self._initRandomOne()

    def _setProject(self, student, number):  # number is the project in student preference
        # Assumes that the student has not yet selected a project
        global config
        assert self._value[student] == -1
        assert len(config._orderedStudentsWishes[config._studentsNumberToName[student]]) > number
        projectNumber = config._projectsNameToNumber[config._orderedStudentsWishes[config._studentsNumberToName[student]][number]]
        self._projectNumberSelected[projectNumber] += 1
        self._value[student] = number
        if self._projectNumberSelected[projectNumber] > 3:
            self._penalty += 1000*(self._projectNumberSelected[projectNumber] - 3)
        elif self._projectNumberSelected[projectNumber] == 1:
            self._penalty += 5000
        elif self._projectNumberSelected[projectNumber] == 2:
            self._penalty -= 5000
        if len(config._orderedStudentsWishes[config._studentsNumberToName[student]]) > 3:
            self._penalty += self._penalties[number]  
        else:
            self._penalty += self._penalties[number] / 2  

    def _removeProject(self, student):
        # Assumes that the student has not yet selected a project
        global config
        number = self._value[student]
        self._value[student] = -1
        projectNumber = config._projectsNameToNumber[config._orderedStudentsWishes[config._studentsNumberToName[student]][number]]
        self._projectNumberSelected[projectNumber] -= 1
        if self._projectNumberSelected[projectNumber] > 2:
            self._penalty -= 1000*(self._projectNumberSelected[projectNumber] - 2)
        elif self._projectNumberSelected[projectNumber] == 1:
            self._penalty += 5000
        elif self._projectNumberSelected[projectNumber] == 0:
            self._penalty -= 5000

        if len(config._orderedStudentsWishes[config._studentsNumberToName[student]]) > 3:
            self._penalty -= self._penalties[number]  
        else:
            self._penalty -= self._penalties[number] / 2  

    def fitness(self):
        return -self._penalty

    def reproduceWith(self, other):
        global config 
        # generates the two (empty) children
        toret = []
        for i in range(0,2):
            toret.append(ChromosomeProjects(np.full(shape=config.NOBJECTS, dtype=int, fill_value=-1)))

        crossover = random.randint(1,config.NOBJECTS-1)

        for i in range(0,crossover):
            toret[0]._setProject(i, self._value[i] )
            toret[1]._setProject(i, other._value[i])
        for i in range(crossover, config.NOBJECTS):
            toret[0]._setProject(i, other._value[i] )
            toret[1]._setProject(i, self._value[i])

        return toret

    def mutation(self):
        global config
        i = random.randint(0,len(self._value)-1)
        forbidden = self._value[i]
        self._removeProject(i)
        while True:
            j = random.randint(0,len(config._orderedStudentsWishes[config._studentsNumberToName[i]])-1)
            if j != forbidden: break
        self._setProject(i,j)

    def _initRandomOne(self):
        global config
        self._value = np.full(shape=config.NOBJECTS, dtype=int, fill_value=-1)
        for i in range(0,config.NOBJECTS):
            self._setProject(i, random.randint(0,len(config._orderedStudentsWishes[config._studentsNumberToName[i]])-1))

    def __repr__(self):
        toret = ""
        for i,v in enumerate(self._value):
            toret += "--" if v == -1 else str(v) if v > 9 else "0"+str(v)
            toret += "("+str(config._projectsNameToNumber[config._orderedStudentsWishes[config._studentsNumberToName[i]][v]])+")"
            toret += " "
        toret += "(p="+str(int(self._penalty))+")"
        return toret 

class Population():
    _population = None
    _populationSize = None

    def __init__(self, populationsize = None):
        global config
        self._populationSize = populationsize if populationsize is not None else config.POPULATIONSIZE
        self.randomInit()

    def randomInit(self):
        self._population = []
        while len(self._population) < self._populationSize:
            self._population.append(ChromosomeProjects())
        self._sort()

    def oneGeneration(self):
        ''' We assume a sorted list here'''
        global config
        newpop = self._population[:4]
        while len(newpop) < len(self):
            i1 = self.randomSelect()
            i2 = self.randomSelect(i1)
            for newson in i1.reproduceWith(i2):
                if random.randint(0,100) < config.MUTATIONRATE:
                    newson.mutation()
                newpop.append(newson)
        self._population = newpop
        self._populationSize = len(newpop)
        self._sort()

    def randomSelect(self, taboo=None):
        ''' We assume a sorted list here'''
        somme = (len(self._population)*(len(self._population)-1)) / 2 #sum(x.fitness() for x in self._population)
        current = len(self._population)
        cumul = current
        limit = random.randint(0,somme)
        i = 0
        while  cumul < limit:
            current -= 1
            cumul += current
            assert current > 0
            i += 1
        assert i < len(self._population)
        return self._population[i]
        
        return self._population[random.randint(0,len(self._population)-1)]

    def _sort(self):
        self._population.sort(key=lambda x: x.fitness(), reverse=True)

    def __repr__(self):
        toret = ""
        for i in self._population:
            toret += i.__repr__() + " (f="+ str(int(i.fitness()))+")\n"
        return toret

    def __len__(self):
        return len(self._population)

best = None
for k in range(0,100):
    config.RANDOMSEED = random.randint(0,10000)
    config.POPULATIONSIZE = random.randint(50,500)
    config.MUTATIONRATE = random.randint(5,30)
    population = Population()
    for i in range(0,300):
        population.oneGeneration()
    population._sort()
    besttmp = population._population[0]
    if best is None or besttmp.fitness() > best.fitness():
        best = besttmp
        for i,v in enumerate(best._value):
            print("Student ", i, " ", config._studentsNumberToName[i]," ",v ," ",
                config._orderedStudentsWishes[config._studentsNumberToName[i]][v])
    print("iteration", k, "popsize=", config.POPULATIONSIZE, ", mutrate=", config.MUTATIONRATE, ": best solution of cost ", best.fitness())

print(best)
for i,v in enumerate(best._value):
    print("Student ", i, " ", config._studentsNumberToName[i]," ",v ," ",
            config._orderedStudentsWishes[config._studentsNumberToName[i]][v])

