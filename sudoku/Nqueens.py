from array import *
import time, sys

# My imports
from satutils import *
from sattypes import *
from satheapq import *
from satboundedqueue import *
from prettyPrinter import *
from pysat import *

__NQ = 8

def generateConstraints(callback = lambda x: print(" ".join([str(v) for v in x])+" 0")):
   NQ = __NQ 

   def encode(x, y):
      return x*10 + y
 
   def decode(q):
      return (q//10, q%10)

   def equals1(l):
      callback(l)
      for i,x in enumerate(l):
         for y in l[i+1:]:
             callback([-x, -y])

   def atmost1(l):
      for i,x in enumerate(l):
         for y in l[i+1:]:
             callback([-x, -y])

   # Exactly one value per cell x,y
   for x in range(0, NQ):
        equals1([encode(x+1, y+1) for y in range(0,NQ)])

   for y in range(0, NQ):
        equals1([encode(x+1, y+1) for x in range(0,NQ)])

   for x in range(-NQ+1, NQ):
      if x < 0:
         y = -x
         x = 0
      else:
         y = 0
      diag = []
      while y < NQ and x < NQ:
         diag.append(encode(x+1, y+1))
         y += 1
         x += 1
      #print("c atmost *{}*".format([decode(x) for x in diag]))
      atmost1(diag)

   for x in range(-NQ+1, NQ):
      if x < 0:
         y = NQ+x
         x = 0
      else:
         y = NQ-1
      diag = []
      while y >= 0 and x < NQ:
         diag.append(encode(x+1, y+1))
         y -= 1
         x += 1
      #print("c atmost *{}*".format([decode(x) for x in diag]))
      atmost1(diag)

solver = Solver()
generateConstraints(solver.addClause)
solver.buildDataStructure()
result = solver.solve()
nbsolutions = 0
blockedClauses = []
while result == solver._cst.lit_True:
   nbsolutions += 1

   if result == solver._cst.lit_True: # SAT was claimed
      blockedClause = []
      for v in solver.finalModel:
         if v > 0:
            print(v, end=" ")
            blockedClause.append(-v)
      print("")

      blockedClauses.append(blockedClause)
      solver = Solver()
      generateConstraints(solver.addClause)
      for c in blockedClauses:
         solver.addClause(c)
      solver.buildDataStructure()
      result = solver.solve()

print("Nombre de solutions", nbsolutions)
