# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 11:40:59 2019
@author: aanduss

Credit: I used the timeit decorator function from https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d

"""

import time
from functools import wraps


def timeit(method):
    # This decorator is used to time some of the key functions. The results are printed to the console upon completion.
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' %  (method.__name__, (te - ts) * 1000))
            
        return result
    return timed


class Node:
    # This is a custom object used to store the pertinent information for each data point (i.e. location)
    # All data points in-scope are translated to and stored as nodes early in the script.
    def __init__(self, Neighbors,  Traversable, Location, FScore, GScore, Parent):
        
        self.Neighbors = Neighbors
        self.Traversable = Traversable
        self.Location = Location
        self.FScore = FScore
        self.GScore = GScore
        self.Parent = Parent

@timeit
def createRange(width, length, start, goal, blockStart, blockEnd, diagonalsAllowed):
    # Creates nodes using the given dimensions and adds them to the node list (nList)
    
    nlist = []
    
    for x in range(1, width+1):
        for y in range(1,length+1):
            
            if (y <= blockEnd[1] and y >= blockStart[1]) and (x <= blockEnd[0] and x >= blockStart[0]):        
                # Creating Non-Traversable Nodes here to demonstrate pathfinding ability. 
                # They will appear as 'x' in the final print out. 
                n1 = Node(None, False, (x,y), 0, 0, None)
            else:    
                # Create Traversable Nodes here. They will appear as '0' in the final print out. 
                # The path itself will be left blank.
                n1 = Node(None, True, (x,y), 0, 0, None)
                
            nlist.append(n1)
    
    # Populate the neighbor information for each node
    nlist = populateNeighbors(nlist, start, goal, diagonalsAllowed)    
    
    return nlist

@timeit
def populateNeighbors(nlist, start, goal, diagonalsAllowed):
    # Populates the neighbors for each node
    # This function is built to accomodate a 2 dimensional grid, but could be adapted for any kind of data (i.e. 3 dimensions, hexagonal, unstructured, etc.)
    
    for node in nlist:
        coord = node.Location
        
        # Manual identification of neighbor nodes
        NW = nodeLookup((coord[0]-1,coord[1]+1), nlist)
        N = nodeLookup((coord[0],coord[1]+1), nlist)
        NE = nodeLookup((coord[0]+1,coord[1]+1), nlist)
        W = nodeLookup((coord[0]-1,coord[1]), nlist)
        E = nodeLookup((coord[0]+1,coord[1]), nlist)
        SW = nodeLookup((coord[0]-1,coord[1]-1), nlist)
        SE = nodeLookup((coord[0]+1,coord[1]-1), nlist)
        S = nodeLookup((coord[0],coord[1]-1), nlist)
                
        neighList = []
               
        neighList.append(N)
        neighList.append(W)
        neighList.append(E)
        neighList.append(S)
        
        # If diagonals are allowed then also add the diagonal nodes to the nieghbor list to be evaluated
        if(diagonalsAllowed):
            neighList.append(NE)
            neighList.append(SW)
            neighList.append(SE)
            neighList.append(NW)
        
        # Assign list of neihbors to the node.Neighbors variable
        node.Neighbors = neighList
    
    return nlist        
            
            
def nodeLookup(coord, nlist):
    for tmpNode in nlist:
         if coord == tmpNode.Location:
            return tmpNode
    return None

def heuristic(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def gscore(neighbor, start): # Note this function is not in use
    return abs(neighbor[0] - start[0]), abs(neighbor[1] - start[1])

def minFScore(nodeList):
    min = nodeList[0]
    for x in nodeList:
        if x.FScore < min.FScore:
            min = x
    return min

#@timeit
def findRoot(node, finalPath):
    # Recursive lookup function to compile the final path by backtracking from the final goal node back to the start node using the 'parent' attributes we have been updating along the way
    
    # Add the given node to the final path list
    finalPath.insert(0, node)
    
    # If the given node has no parent node then it is the start node and we can return the completed path.
    # Otherwise we continue the recursive search
    if node.Parent == None:
        return finalPath
    else:
        return findRoot(node.Parent, finalPath)

@timeit
def astar(nlist, start, goal):

    startNode = nodeLookup(start, nlist)
    goalNode = nodeLookup(goal, nlist)
    
    # The set of nodes already evaluated
    close_set = []
    
    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.    
    open_set = []
    
    # Determine FScore fore each Node in orginal list (nlist)
    # This may only need to be initially calculated for the start node    
    startNode.GScore = 0
    startNode.FScore = heuristic(start, goal)      

    open_set.append(startNode)
        
    while open_set:
        
        #current is the node in openset having the lowest fScore value        
        current = minFScore(open_set)
        
        #if current node = goal then return path
        if current.Location == goal:
            finalPath = []
            finalPath = findRoot(current, finalPath)
            return finalPath
        
        open_set.remove(current)
        close_set.append(current)
        
        # Loop through neighbor nodes
        for neighbor in current.Neighbors:    
                              
            if neighbor != None:
                
                # Ignore the neighbor which is already evaluated.
                if neighbor in close_set:
                    continue
               
                # The distance from start to a neighbor
                tentative_g_score = heuristic(current.Location, goal) + heuristic(current.Location, neighbor.Location)
                           
                # Jump to next  if neighbor is not traversable
                if neighbor.Traversable != True:
                    continue
                
                #If the neighbor node is not already in the open_set, then add it to the open_set
                if neighbor not in open_set:
                    open_set.append(neighbor)
                #else if the current node's tentative G Score is greater than or equal to the Neighbor's G Score, jump to next neighbor's loop
                elif tentative_g_score >= neighbor.GScore:
                    continue
                                
                # This neighbor is the best next node in the path discovered so far, link it to the current node via its parent attribute.
                neighbor.Parent = current
                
                #G Score is the distance from the start to this neighbor node
                neighbor.Gscore = tentative_g_score 
                
                # the F score is the cost of getting from start to finish. This is partly known(G Score) and partly heuristic.
                neighbor.FScore = tentative_g_score + heuristic(neighbor.Location, goal)
                
    return False

def printCoords(path):
    # Print each coordinate in the path found
    
    print('\nPath Coordinates:')    
    if(path != None and path != False):
        for x in path:
            print (x.Location)
    else:
        print("__________________")
        print("Path returned " + str(path) + '\n')

def printMap(length, width, path, nlist):
    # Create a visual representation of the map printed out to the console.
    
    # Map legend:
    # -Traversable node = 0
    # -Non-Traversable node = x
    # -Path node = blank (' ')
    # -Start node = 's'
    # -End node = 'e'
    
    print('\nPath Map:')
    
    if(path == False):
        print("Path not possible. Please ensure your start and end points are possible in the given dimensions")
    else:        
        for y in reversed(range(1, length+1)): 
            
            # a single string (i.e. row) is used to visually represent the map for each row
            row = ''
            for x in (range(1, width+1)):
                
                nodeBlocked = False
                nodeFound = False
                startNode = False
                endNode = False        
                length = len(path) - 1
                
                for node in path:
                    if( (x,y) == (node.Location[0], node.Location[1]) ):
                        nodeFound = True
                        
                        # If coordinates equal the coordinates of the first node in the Path list then startNode = true
                        if( (x,y) == (path[0].Location[0], path[0].Location[1]) ):
                            startNode = True
                        # If coordinates equal the coordinates of the last node in the path list then endNod = true
                        elif( (x,y) == (path[length].Location[0], path[length].Location[1]) ):
                            endNode = True
                for nodeN in nlist:
                    if( (x,y) == nodeN.Location and nodeN.Traversable == False):
                        nodeBlocked = True
                
                # If a node was found at the current coordinates then add the proper character to the row string.
                if(nodeFound == True):
                    if(startNode == True):
                        row = row + 's'
                    elif(endNode == True):
                        row = row + 'e'
                    else:
                        row = row + ' '
                elif(nodeBlocked == True):
                    row = row + 'x'
                elif(nodeFound == False):        
                    row = row + str(0)        
                
            # Once we have traveresed through each coordinate for this row, print the row string and then move on to the next row in the loop
            print(row)