import sys
import pandas as pd
import numpy as np
from math import sqrt
import heapq
import copy

# Dictionary for distances for the heuristic
distances={}
# Constant to represent infinity
infinity = float("inf")
#node dictionary for RBFS, unused
#node_dictionary = {}
# This variable is used to return the final distance
RBFS_distance = []
# Global variable for putting together RBFS path
RBFS_path = []
# This variable is used to return the number of states expanded
RBFS_states = []
# This is the global list of nodes
nodes = []

# Basic compare function
def cmp(a, b):
    return (a > b) - (a < b) 

#This is the node class that stores a letter and number for viewing purposes,
# an h value, a f value for choice purposes and its neighbors to continue on
class Node:
    def __init__(self, letter, number, h):
        self.letter = letter
        self.number = number
        self.h = h
        self.f = 0
        self.neighbors = {}

    def __str__(self):
        return "Node(number='{}',letter='{}' h={}, f={}, neighbors={} )".format(self.number, self.letter, self.h, self.f, self.neighbors)
    
    def __repr__(self):
        return str(self)
    
    def __cmp__(self, other):
        return cmp(self.f, other.f)

    def __lt__(self, other):
        return self.f < other.f  




# This is the second attempt at RBFS
# This is the introduction
# Start is the start node
# End is the goal node
def RBFSStart2(start,end):
    # The start nodes f will be identical to the heuristic
    start.f= start.h
    # Add 1 to the list of states expanded
    RBFS_states.append(1)
    # Call with an initial flimit of infinity and gvalue of 0
    RBFS2(start, end, 0, infinity)
    return 1, "success"

# This is the recursive function that also takes a gvalue and a flimit
def RBFS2(current, end, g_value, f_limit):
    #Initial Check for success
    #print(current)
    if(current.number == end.number):
        # add this to the path
        RBFS_path.append(current.number)
        return 1, "success"
    # if there are no neighbors
    if(len(current.neighbors) == 0):
        return(0, infinity)
    successors = []
    # Check successors
    for val, distance in current.neighbors.items():
        # deepcopy allows it to not cause recursive problems
        successorNode = copy.deepcopy(nodes[val])
        tent_g = g_value + distance
        f_value = tent_g + successorNode.h
        successorNode.f = max(f_value, current.f)
        successors.append(successorNode)


    # Old faulty method 
    # for node1, node2, distance in edges:
    #         if int(node1) == int(current.number):
    #             # Calculate the tentative g-value for the neighbor node
    #             copyNode = copy.deepcopy(nodes[node2])
    #             tent_g = g_value + distance
    #             f_value = tent_g + copyNode.h
    #             if(current.f is None):
    #                 copyNode.f = f_value
    #             else:
    #                 copyNode.f = max(f_value, current.f)
    #             # Make a new successor list with f_value
    #             successors.append(copyNode)

    while True:
        #Sort the successors
        successors.sort()
        #print(successors)
        # Get all the best stats
        best = successors[0]
        best_f_value = best.f
        best_node = int(best.number)
        best_distance = current.neighbors[best_node]
        # If the best is above the limit go back
        if best_f_value > f_limit:
            return (0, best_f_value)
        # Assign the best alternative
        if(len(successors) > 1):
            alternative = successors[1].f
        else:
            alternative = infinity
        # Add to states expanded and go recursive
        RBFS_states.append(1)
        success, returned_best = RBFS2(copy.deepcopy(best), end, g_value + best_distance, min(f_limit, alternative) )
        # change f to returned best
        successors[0].f = returned_best
        # Check for successful return
        if(success > 0):
            RBFS_path.append(current.number)
            RBFS_distance.append(best_distance)
            return (1, "SUCCESS")    






# Returns a solution or failure and starts at the max integer
# Faulty RBFS start
#def recursive_best_first_search(heuristics, edges, start, end):
    #explored list for RBFS
    exploredStart = []
    #seen paths list
    seen_paths = {}
    RBFS_states.append(start)
    current_route = []
    path = RBFS(heuristics, edges, start, end, seen_paths, current_route, node_dictionary, exploredStart, 0, infinity)
    return path

# Faulty RBFS
#def RBFS(heuristics, edges, current, end, seen_paths, current_route, node_dictionary, explored, g_value, f_limit):
    #toDrop = []
    updated_f_limit = f_limit
    explored.append(current)
    current_route.append(current)
    if(current == end):
        
        return 1, current
    successors = []
    for node1, node2, distance in edges:
            if node1 == current and node2 not in current_route:
                # Calculate the tentative g-value for the neighbor node
                tent_g = g_value + distance
                f_value = tent_g + heuristics[node2]
                # Make a new successor list with f_value
                successors.append( (f_value, node1, node2, distance))
                #print(f_value)
    if(len(successors) == 0):
        successors_df = pd.DataFrame(np.empty((0, 4)))
    else:
        successors_df = pd.DataFrame(successors)
    successors_df.columns = ['f_value', 'node1', 'node2', 'distance']
    
    
   
    
    while True:
        #print(current_route)
        for i, row in successors_df.iterrows():
            current_node1 = successors_df.iloc[i]['node1']
            current_node2 = successors_df.iloc[i]['node2']
            letter_path = nodes_to_letters(current_node1, current_node2)

            if(letter_path not in node_dictionary):
                node_dictionary[letter_path] = successors_df.iloc[i]['f_value']
            if(seen_paths.get(successors_df.iloc[i]['node2']) is None):
                seen_paths[successors_df.iloc[i]['node2']] = [successors_df.iloc[i]['node1']]
            if(successors_df.iloc[i]['node1'] not in seen_paths[successors_df.iloc[i]['node2']]):
                seen_paths[successors_df.iloc[i]['node2']] += [successors_df.iloc[i]['node1']]
            
            successors_df.at[i,'f_value'] = max( successors_df.iloc[i]['f_value'], node_dictionary[letter_path])
     
        
        #print(seen_paths)
        #print(node_dictionary)
        successors_df=successors_df.sort_values(by=['f_value'])
        successors_df= successors_df.reset_index(drop=True)
        #print(successors_df)
        if(successors_df.empty):
            current_route.remove(current)
            return 0, infinity
        else:
            best_f_value = successors_df.iloc[0]['f_value']
        ##print(best_f_value)
        
        if(len(successors_df) > 1):
            alternative = successors_df.iloc[1]['f_value']
        else:
            alternative = infinity
        ##change the f-limit being passed
        updated_f_limit = min(f_limit, alternative)
        #print("Updated F-limit= " + str(updated_f_limit))
        if(best_f_value> updated_f_limit):
            current_route.remove(current)
            return 0, best_f_value
        best_node = successors_df.iloc[0]['node2']
        best_distance = successors_df.iloc[0]['distance']
        RBFS_states.append(best_node)
        result = RBFS(heuristics, edges, best_node, end, seen_paths, current_route, node_dictionary, explored, g_value + best_distance, updated_f_limit)
        if result[0] != 0:
            RBFS_distance.append(best_distance)
            RBFS_path.append(current)
            return 1, best_f_value
        returned_letters = nodes_to_letters(current, best_node)
        node_dictionary[returned_letters] = result[1]
        
        
# Turns the nodes number into letters. Ex: 0, 5 becomes AF
def nodes_to_letters(node1, node2):
    concat = chr(int(node1) + ord('A')) + chr(int(node2) + ord('A'))
    return concat

# function RBFS(problem, node, f_limit) returns a solution or failure, and a new f-cost limit
# if problem.IS-GOAL(node.STATE)
# then return node
# successors=LIST(EXPAND(node))
# if successors is empty then return failure, ∞
# for each s in successors do
# // update f with value from previous search
# s.f←max(s.PATH-COST + h(s), node.f))
# while true do
#     best =the node in successors with lowest f-value
#     if best.f> f_limit then return failure, best.f
#     alternative = the second-lowest f-value among successors
#     result, best.f = RBFS(problem, best, min(f_limit, alternative))
#     if result != failure then return result, best.f



# Function to calculate Euclidean distance
def euclidean_distance(x1, y1, x2, y2):
    return sqrt((float(x1) - float(x2))**2 + (float(y1) - float(y2))**2)

# Function to turn a matrix of edge weights into a graph
def matrix_to_graph(matrix):
    # Get the number of nodes in the graph
    num_nodes = matrix.shape[0]

    # Initialize an empty list to store the edges
    edges = []

    # Iterate through the matrix and add edges to the list
    for i in range(num_nodes):
        for j in range(num_nodes):
            # If the edge weight is not zero, add it to the list
            if matrix[i,j] != 0:
                nodes[i].neighbors[j] = matrix[i,j]
                edges.append((i, j, matrix[i,j]))
    #print(nodes)
    # Return the list of edges
    return edges

# Formats the path in a letter system
def path_to_letters(path):
    finished_path = ""
    path_length = len(path)
    for x in range(path_length):
        finished_path += chr(ord('A') + int(path[x]))
        if( x != (path_length-1) ):
            finished_path += " -> "
    return finished_path

# Sums the RBFS distance
def RBFS_distance_sum(distances):
    sum = 0
    for i in range(len(distances)):
        sum += distances[i]
    return sum

# a* formula that takes the list of heuristics, the edges, and a start and goal
def a_star(heuristics, edges, start, end):
    # Create a dictionary to store the g-values (cost from start to current node)
    g_values = {start: 0}
    # Create a priority queue using heapq
    priority_queue = [(0 + heuristics[start], start)]
    # Create a dictionary to store the came from information for each node
    came_from = {}
    # Keep track of states expanded along the way
    states_expanded = 0

    while priority_queue:
        # Get the node with the lowest f-value (g-value + h-value)
        current = heapq.heappop(priority_queue)[1]
        states_expanded = states_expanded + 1
        
        # Check if we have reached the end node
        if current == end:
            # Find the length of the path
            path_length =  g_values[current]
            # Create a list to store the path
            path = []
            # Add the end node to the path
            path.append(end)
            # Trace back the path from the end node to the start node
            while current in came_from:
                current = came_from[current]
                path.append(current)
            # Reverse the path to start from the start node
            path.reverse()
            return path, states_expanded, path_length

        # Iterate through the edges connected to the current node
        for node1, node2, distance in edges:
            if node1 == current:
                # Calculate the tentative g-value for the neighbor node
                tent_g = g_values[current] + distance
                # Check if the tentative g-value is better than the current g-value for the neighbor node
                if node2 not in g_values or tent_g < g_values[node2]:
                    # Update the g-value and came from information for the neighbor node
                    g_values[node2] = tent_g
                    came_from[node2] = current
                    # Add the neighbor node to the priority queue
                    f_value = tent_g + heuristics[node2]
                    heapq.heappush(priority_queue, (f_value, node2))
    return None


# Read in coordinates from file and make distance to goal heuristic
# Get the text file name from the command line
file_name = sys.argv[1]
#print(file_name)
# Read the text file into a matrix
with open(file_name, 'r') as file:
    lines = file.readlines()
    #Get the start and goal from name
    start = ord(file_name[5])-ord('A')
    goal = ord(file_name[7])-ord('A')
    total_nodes = goal-start+1
    matrix = np.array([[int(x) for x in line.strip().replace(" ","").rstrip(',').split(',')] for line in lines])
# Read the excel file into a dataframe
coordinates = pd.read_csv('cities.csv', names=['node', 'city', 'lat', 'lng'])
# Drop the unnecessary data
coordinates = coordinates.drop('city', axis=1 )
coordinates = coordinates.drop(0, axis=0 )
for x in range(26, total_nodes, -1):
    coordinates = coordinates.drop(x, axis=0 )

# Get the coordinates of the final row (destination)
lat2=coordinates.iloc[total_nodes-1]["lat"]
lon2=coordinates.iloc[total_nodes-1]["lng"]


# Iterate through the rows of the dataframe
for i in range(0, total_nodes):
    lat1, lon1 = coordinates.iloc[i]["lat"], coordinates.iloc[i]["lng"]
    
    # Calculate the Euclidean distance
    distance = sqrt(euclidean_distance(lat1,lon1,lat2,lon2))
    #print(distance)
    node = Node(chr(i + ord('A')), i, distance)
    
    nodes.append(node)
    # Add the distance to the dictionary
    distances[i] = distance

# Turn the matrix into a list of edges
edges = matrix_to_graph(matrix)


#print(distances)
#print(edges)

# Call and print A*
path = a_star(distances, edges, start, goal)
shortest_path_a = path_to_letters(path[0])
print("\nA* Search:\nShortest path: " + shortest_path_a + "\nShortest path cost: " + str(path[2]) + "\nNumber of states expanded: " + str(path[1]))

# Call and print RBFS
path = RBFSStart2(nodes[0],nodes[total_nodes-1])
# print(path)
# path = recursive_best_first_search(distances, edges, start, goal)
RBFS_path.reverse()
shortest_path_r = path_to_letters(RBFS_path)
shortest_distance_r = RBFS_distance_sum(RBFS_distance)
print("\nRBFS Search:\nShortest path: " + shortest_path_r + "\nShortest path cost: " + str(shortest_distance_r)+ "\nNumber of states expanded: " + str(len(RBFS_states)))

