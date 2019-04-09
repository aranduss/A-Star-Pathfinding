# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 11:40:59 2019

@author: aanduss
"""

#See the AStar_Functions file for the inner workings of the pathfinding
from AStar_Functions import *

#######################################################################################################
######  ASTAR Pathfinding   ###########################################################################
#######################################################################################################
    
# Set map dimensions  
width = 20
length = 20

# Set start and end points.
start = (1,1)
goal = (20,20)

# set start and end coordinates for blocked sqaures. this will essentially make all nodes between the two coordinates non-traversable.
# for example the coordinates of 3,3 and 10,10 will make the coordinates between (3,3), (3,10), (10,3), and (10,10) non-traversable.
# It will be easier to understand this visually in the final map output to the console. Non-traversable nodes are represented visually with x's.
blockStart = (2,2)
blockEnd = (10,10)

# If true, this boolean will allow the pathfinding to move diagonally (NE,NW,SW,SE) 
diagonalsAllowed = True

# Create Data Points
nlist = createRange(width, length, start, goal, blockStart, blockEnd, diagonalsAllowed)

# Perform Astar pathfinding and assign the discovered list of nodes to the path list
path = astar(nlist, start, goal)

# Print path coordinates or indicate if path not possible (i.e. result of None)  
printCoords(path)

# Print map of path 
printMap(length, width, path, nlist)
