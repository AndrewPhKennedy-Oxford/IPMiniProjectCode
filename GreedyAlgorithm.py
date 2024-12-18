import copy

#Implements the Greedy Algorithm from Part I
def GreedyAlgorithm(S, k, m):
  #our solution is made up of the elements covered by C
  C = set([])
  #our final solution will be the size of this set
  elementsCovered = set([])

  #Iterate until we have chosen k sets from S (or all the sets if there are fewer than k in S)
  for i in range(min(k, len(S))):
    maxSize = 0
    optchoice = 0
    #Try adding each of the unchosen sets so far
    for r in range(m):
      #if we have already added S_r to C, don't consider it
      if r in C:
        continue
      #Consider what happens to elementsCovered if we add S_r to C
      tempSet = copy.deepcopy(elementsCovered)
      for sj in S[r]:
        tempSet.add(sj)
      #If S_r is a maximizer for elementsCovered by C so far, save it as the optimal choice so far
      if len(tempSet) - len(elementsCovered) >= maxSize:
        maxSize = len(tempSet) - len(elementsCovered)
        optchoice = r
    #Add the set which maximized the elementsCovered to C
    C.add(optchoice)
    #Add all the elements from this newly added set to the set of covered elements
    for sj in S[optchoice]:
      elementsCovered.add(sj)
  #At the end, our solution is just the number of elements covered by C
  return [S[i] for i in C], len(elementsCovered)


S = [[0], [1, 2], [3, 4, 5], [6, 7, 8], [2, 4, 6], [2, 7, 9], [4, 5, 6, 9],
     [1, 3, 5], [8, 9], [9], [10], [0, 1, 3], [1, 2, 3], [1, 4, 5]]
k = 3
m = 10
print(GreedyAlgorithm(S, k, m))
