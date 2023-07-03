# THIS PROBLEM IS DISTANCE MINIMIZATION WITH SOLOMON REAL DATA
# This is correct and it works to analyze the individual tours
# n is the number of clients to visit
# N is the set of clients, with N = {1, 2,...n}
# V set of vertices (or nodes), with V = {0} U N
# A set of arcs, with A = {(i,j) E V**2 : i != j}
# c is distance of travel over arc(i,j)
# Q is the vehicle capacity
# qi is demand of each client
# w is curb weight

import pandas as pd
from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Read the text file
file_path = 'C:\\Users\\luqui\\PycharmProjects\\AdvancedSSCM\\DATA\\c5.txt'
df = pd.read_csv(file_path, delim_whitespace=True)


n = 10 # number of clients
xc = df['XCOORD'].tolist() # n location of clients + 1 for depot - EXTRACTED FROM SOLOMON DATA
yc = df['YCOORD'].tolist() # n location of clients + 1 for depot - EXTRACTED FROM SOLOMON DATA

N = [i for i in range(1,n+1)] # Set of clients [1,2,3,4,5,6,7,8,9,10]
V = [0] + N # The union of 0 + N [0,1,2,3,4,5,6,7,8,9,10]
A = [(i,j) for i in V for j in V if i!=j] # [(0,1), (0,2],...,(10,9]]
# Create dictionary for distance
c = {(i, j): np.hypot(xc[i] - xc[j], yc[i] - yc[j]) for i,j in A}
Q = 80 # vehicle capacity
q = df['DEMAND'].tolist() # EXTRACTED FROM SOLOMON DATA

# Create arrays of city names
city_names = ["Depot (0) ", "Guadalajara (1)", "Colima (2)", "Michoacan (3)", "Tijuana (4)", "Merida (5)", "Monterrey (6)", "Aguascalientes (7)", "Queretaro (8)", "Mexico City (9)", "Guanajuato (10)"]

# Set the figure size
plt.figure(figsize=(10, 8))

# Plot solution with active arcs
for i, j in c:
    plt.plot([xc[i], xc[j]], [yc[i], yc[j]], color="grey", linestyle="dotted", zorder=0)
    plt.annotate(city_names[j], (xc[j], yc[j]), textcoords="offset points", xytext=(10, 15), ha='center')

plt.plot(xc[0], yc[0], c='r', marker='s')  # That is the depot
plt.scatter(xc[1:], yc[1:], c='b')  # These are the clients


#Print graphical solution
plt.xlabel("Distance X")
plt.ylabel("Distance Y")
plt.title("Instance # 5")

plt.show()

#print(c) #uncomment to see correct distances
