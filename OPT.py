from ortools.linear_solver import pywraplp


#Set the IP Variables for the IP Solver for x and y
def setIPVars(solverIP):
  x = []
  y = []
  for i in range(m):
    x.append(solverIP.IntVar(0, 1, 'x_int' + str(i)))

  for j in range(n):
    y.append(solverIP.IntVar(0, 1, 'y_int' + str(j)))

  return x, y


def SolveIP(x, y, solver, k, S, YMap):

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

  #Solve the IP
  result = solver.Solve()

  #If the IP solver found an optimal solution, return the number of elements covered by the optimal choice for C
  if result == pywraplp.Solver.OPTIMAL:
    return [[S[i] for i in range(len(x)) if x[i].solution_value() == 1],
            sum(y_j.solution_value() for y_j in y)]
  return [[], 0]


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

solverIP = pywraplp.Solver('IP opt problem',
                           pywraplp.Solver.BOP_INTEGER_PROGRAMMING)
x2, y2 = setIPVars(solverIP)
#Solve IP
ipSolution = SolveIP(x2, y2, solverIP, k, S, YMap)
print(ipSolution[0], int(ipSolution[1]))
