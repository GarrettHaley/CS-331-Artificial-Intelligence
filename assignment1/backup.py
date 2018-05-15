import sys
from collections import deque
from Queue import PriorityQueue
import heapq
allowedActions = [[1,0],[2,0],[0,1],[1,1],[0,2]]
nodesExpanded = 0
class Node:
	def __init__(self,leftState,rightState,cost,treeDepth,parentNode):
		self.leftState = leftState
		self.rightState = rightState
		self.cost = cost
		self.treeDepth = treeDepth
		self.parentNode = parentNode
		self.key = "".join(map(str,(list(self.leftState) + list(self.rightState))))
def CreateState(File):
	with open(File, "r") as fileStream:
		leftStr = fileStream.readline().rstrip().split(',')
		rightStr = fileStream.readline().rstrip().split(',')
		leftState = []
		rightState = []
		for i in leftStr:
			leftState.append(int(i))
		for i in rightStr:
			rightState.append(int(i))
	return Node(leftState,rightState,0,0,None)

def IsEqualStates(state1,state2):
	if state1.leftState == state2.leftState and state1.rightState == state2.rightState:
        	return True
	else:
		return False
def Iddfs(node,goal):
	limit = 0
	while True:
		result = DLSGraphSearch(node,goal,limit)
		if result != None:
			return result
		limit+=1
def DLSGraphSearch(initial, goal, limit):
	cutoff = None
	failure = None

	explored = {}

	frontier = [initial]

	while True:
		if len(frontier) == 0:
			return cutoff
		
		state = frontier.pop()
		
		if (IsEqualStates(state, goal)):
			return state

		if state.key not in explored or state.treeDepth < explored[state.key]:
			explored[state.key] = state.treeDepth
			if state.treeDepth <= limit:
				children = Expand(state)
				for child in children:
					frontier.append(child)
	
def GraphSearch(initialState,goalState,mode):
	if IsEqualStates(initialState,goalState):
		PrintPath(initialState)
	if mode == "astar":
		frontier = []
		heapq.heappush(frontier,(initialState.cost,initialState))
	else:
		frontier = deque()
		frontier.append(initialState)
	explored = {}
	while True:
		if len(frontier) == 0:
			sys.exit("Solution was not found")
		if mode == "bfs":
			currentNode = frontier.popleft()
		elif mode == "dfs":
			currentNode = frontier.pop()
		else:
			currentNode  = heapq.heappop(frontier)[1]
		if IsEqualStates(currentNode,goalState):
			PrintPath(currentNode,currentNode.treeDepth)
			sys.exit()
		if currentNode.key not in explored:
			explored[currentNode.key] = currentNode.treeDepth
			if mode == "astar":
				map(lambda j:heapq.heappush(frontier,(GetCost(j,goalState),j)),Expand(currentNode)) 
			else:
				frontier += Expand(currentNode)

def Expand(currentNode):
	global nodesExpanded
	nodesExpanded+=1
	childrenNodes = []
	for action in allowedActions:
		if IsAllowed(action,currentNode):
			childNode = UseAction(action,currentNode)
			childrenNodes.append(childNode)
	return childrenNodes

def GetCost(node,goalState):
	if goalState.leftState[2] == 1:
		return (int(node.rightState[0]) + int(node.rightState[1]))/2 + node.cost
	else:
		return (int(node.leftState[0]) + int(node.leftState[1]))/2 + node.cost

def PrintPath(childNode,treeDepth):
	print(childNode.leftState)
	print(str(childNode.rightState) + "\n")
	if childNode.parentNode == None:
		print("Tree depth: " + str(treeDepth))
		print("Nodes expanded: " + str(nodesExpanded))
		print("Goal has been completed.")
		return 0
	PrintPath(childNode.parentNode,treeDepth)
	
def IsAllowed(action,currentNode):
    if currentNode.leftState[2] == 1:
	boat = list(currentNode.leftState)
	noBoat = list(currentNode.rightState)
    if currentNode.rightState[2] == 1:
	boat = list(currentNode.rightState)
	noBoat = list(currentNode.leftState)
    boat[0] = boat[0] - action[0]
    boat[1] = boat[1] - action[1]
    noBoat[0] = noBoat[0] + action[0]
    noBoat[1] = noBoat[1] + action[1]
    
    if boat[0] < 0 or boat[1] < 0 or noBoat[0] < 0 or noBoat[1] < 0:
        return False
    elif (boat[0] == 0 or boat[0] >= boat[1]) and (noBoat[0] == 0 or noBoat[0] >= noBoat[1]):
        return True
    else:
        return False					
					
def UseAction(action,currentNode):
	leftState = []
	rightState = []
	if currentNode.leftState[2] == 1:
         	leftState.append(int(currentNode.leftState[0]) - action[0])
		leftState.append(int(currentNode.leftState[1]) - action[1])
		leftState.append(0)
		rightState.append(int(currentNode.rightState[0]) + action[0])
		rightState.append(int(currentNode.rightState[1]) + action[1])
		rightState.append(1)
	else:
		rightState.append(int(currentNode.rightState[0]) - action[0])
                rightState.append(int(currentNode.rightState[1]) - action[1])
		rightState.append(0)
                leftState.append(int(currentNode.leftState[0]) + action[0])
                leftState.append(int(currentNode.leftState[1]) + action[1])
		leftState.append(1)
	
        return  Node(leftState,rightState,int(currentNode.cost)+1,int(currentNode.treeDepth)+1,currentNode)
		
				
def main():
	if len(sys.argv) != 5:
		sys.exit("Arguments given are incorrect. Make sure to include python < program name > < initial state file > < goal state file > < mode > < output file >")
	initialState = CreateState(sys.argv[1])
	goalState = CreateState(sys.argv[2])
	mode = sys.argv[3]
	outputFile = sys.argv[4]
	if mode == "iddfs":
		map(lambda x:PrintPath(x,x.treeDepth),[(Iddfs(initialState,goalState))])
	elif mode == "bfs" or mode == "dfs" or mode == "astar":
		GraphSearch(initialState,goalState,mode)
	else:
		print("Incorrect mode: please use bfs, dfs, iddfs, or astar for proper evaluation")
	return 0
main()
