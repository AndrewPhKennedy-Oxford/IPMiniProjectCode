from ortools.linear_solver import pywraplp
from numpy.random import choice


#Set the LP Variables for the LP Solver for x and y
def setLPVars(solverLP):
  x = []
  y = []
  for i in range(m):
    x.append(solverLP.NumVar(0, 1, 'x_' + str(i)))

  for j in range(n):
    y.append(solverLP.NumVar(0, 1, 'y_' + str(j)))

  return x, y


def SolveLP(x, y, solver, k, S, YMap):

  #Add constraint \sum_{j=0}^{m}x_j=k
  solver.Add(sum(xi for xi in x) == k)

  #For all [1,n]
  for j in range(n):
    #Add constraints y_i <= \sum_{j|i \in S_j} x_j
    solver.Add(y[j] - sum(x[i] for i in range(m) if i in YMap[j]) <= 0)
    #Add constraints 0 <= y_i <= 1
    solver.Add(y[j] <= 1)
    solver.Add(y[j] >= 0)
  #For all [1,m]
  for i in range(m):
    #Add constraints 0 <= x_j <= 1
    solver.Add(x[i] <= 1)
    solver.Add(x[i] >= 0)

  #Add objective function maximize \sum_{i=1}^{n}y_i
  solver.Maximize(sum(yj for yj in y))

  #Solve the LP
  result = solver.Solve()

  Xs = []
  #If the LP Solver was able to find an optimal solution to the LP
  if result == pywraplp.Solver.OPTIMAL:
    print('Optimal objective value:', solver.Objective().Value())
    #Add the probabilities for each S_i of being chosen based on the LP solution
    for i in range(m):
      Xs.append(x[i].solution_value() / k)

    listOfChoices = []
    for i in range(m):
      listOfChoices.append(i)
    #Choose the sets for C from S, using the probability distribution induced by the LP solution
    draw = choice(listOfChoices, k, p=Xs, replace=False)
    print(Xs)
    print(sum(y_j.solution_value() for y_j in y))

    #Count the number of elements in E covered by the sets in C
    elementsCovered = set([])
    for i in range(k):
      for r in range(len(S[draw[i]])):
        elementsCovered.add(S[draw[i]][r])
    return len(elementsCovered)


S = [[0], [1, 2], [3, 4, 5], [6, 7, 8], [2, 4, 6], [2, 7, 9], [4, 5, 6, 9],
     [1, 3, 5], [8, 9], [9], [10], [0, 1, 3], [1, 2, 3], [1, 4, 5]]
k = 3
m = 14
n = 11

#Create a mapping of each of the elements (j) to the sets (S_i's) by which they are covered
YMap = []
for i in range(n):
  YMap.append([])

for i in range(m):
  arr = []
  for j in range(n):
    if j in S[i]:
      YMap[j].append(i)

solverLP = pywraplp.Solver('LP opt problem',
                           pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
x1, y1 = setLPVars(solverLP)
#Solve LP
lp = SolveLP(x1, y1, solverLP, k, S, YMap)
print(int(lp))
