# A-Star-Pathfinding
A python A-Star path finding algorithm implementation that converts the given data set into custom node objects before pathfinding.

## About
This python project was created to develop working proof of concepts for two things:
  - Processing and converting a coordinate based, related data set into a custom data structure (i.e. Nodes) with dynamic linkage (i.e. neighbor and parent attributes). My example uses a two dimensional grid based map that looks for the fastest way to get from a starting coordinate to an ending/goal coordinate. However, the scripts were designed to be easily adapted to any kind of linked data set that could be assigned a coordinate equivalent. Some examples include three dimensional grids and hexagonal grids.
  - A fast and reasonably efficient A Star pathfinding algorithm
## Prerequisites
1.	The following will need to be installed on your windows machine:
    - Python 3.7
    - A Python 3.7 IDE with console output 

## Running the Tests
1.  The AStar_Main.py file contains the unit tests for this project. The Width, length, start, goal, and block attributes have already been set.
2.  You can simply run this file as is and the console will print out:
    - The time it took for the Node population (populateNeighbors) and AStar pathfinding scripts to run
    - The coordinates from the start to goal nodes
    - A visual representation.
      - 0 = Traversable Node
      - x = Non-Traversable Node
      - blank = Path Node
      - s = Start Node
      - e = End/Goal Node
3. You can edit the preset variables for different outcomes. Note that if you significantly increase the length and width, the script will take longer (200 x 200 takes about 5 mins, Mostly for node population), and you may have to stretch out the console for the map to display properly. 

## Author
•	Alex Anduss – All python scripts
