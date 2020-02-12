# A few helper function for the Sudoku Exercices

# arrayOfVars is an array of int encoding propositional variables
# for instance, if you give this function the array [1, 2, 3, 4]
# it will print
# 1 2 3 4 0
# -1 -2 0
# -1 -3 0
# -1 -4 0
# -2 -3 0
# -2 -4 0
# -3 -4 0
def printClause(clause):
    print(" ".join([str(v) for v in clause]) + " 0")

def equals1a(arrayOfVars):
    printClause(arrayOfVars) 
    for i,x in enumerate(arrayOfVars):
        for y in arrayOfVars[i+1:]:
            printClause([-x, -y, 0])

# second way of doing this, with a callback function and a default one
# with a callback function, you will be able to use it for adding clauses in the solver
# by registering a function that will call solver.addClause instead of printClause !
def equals1(l, callback = printClause):
    callback(l)
    for i,x in enumerate(l):
      for y in l[i+1:]:
        callback([-x, -y])


# Examples
# Another self_contained definition:
def generateConstraints(callback = lambda x: print(" ".join([str(v) for v in x])+" 0")):
   def v(x,y,z):
      return x*100 + y*10 +z
 
   def equals1(l):
      callback(l)
      for i,x in enumerate(l):
         for y in l[i+1:]:
             callback([-x, -y])

   # Exactly one value per cell x,y
   for x in range(1,10):
      for y in range(1,10):
        equals1([v(x,y,z) for z in range(1,10)])

   # Exactly one value per line
   for x in range(1,10):
      for z in range(1,10):
        equals1([v(x,y,z) for y in range(1,10)])

   # Exactly one value per column
   for y in range(1,10):
      for z in range(1,10):
        equals1([v(x,y,z) for x in range(1,10)])

   # Exactly one value per square
   for sx in range(0,3):
      for sy in range(0,3):
        for z in range(1,10):
            equals1([100*(x+3*sx)+10*(y+3*sy)+z for x in range(1,4) for y in range(1,4)])


if __name__ == "__main__":
   generateConstraints()
