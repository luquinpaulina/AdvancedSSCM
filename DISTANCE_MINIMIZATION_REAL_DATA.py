# THIS PROBLEM IS DISTANCE MINIMIZATION WITH NAME OF CITIES
# n is the number of clients to visit
# N is the set of clients, with N = {1, 2,...n}
# V set of vertices (or nodes), with V = {0} U N
# A set of arcs, with A = {(i,j) E V**2 : i != j}
# distance is distance of travel over arc(i,j)
# Q is the vehicle capacity
# qi is demand of each client

from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt

rnd = np.random
rnd.seed(2)

n = 10  # number of customers
xc = rnd.rand(n+1)*200 # n location of clients + 1 for depot - RANDOM LOCATION, WE DO NOT CARE
yc = rnd.rand(n+1)*100 # 200 x 100 rectangule - RANDOM LOCATION, WE DO NOT CARE

#xc = [130, 90, 100, 180, 160, 190, 140, 120, 90, 140, 140  ]
#yc = [50, 10, 20, 10, 40, 80, 80, 90, 60, 20, 30 ]


N = [i for i in range(1,n+1)] # Set of clients [1,2,3,4,5,6,7,8,9,10]
V = range(n+1)  # Set of vertices (cities)
A = [(i, j) for i in V for j in V if i != j]  # Set of arcs

Q = 6350  # vehicle capacity

distance = {
    (0, 0): 0,     (0, 1): 41150,  (0, 2): 25680,  (0, 3): 54200,  (0, 4): 95380,  (0, 5): 15910,  (0, 6): 88960,  (0, 7): 74120,  (0, 8): 26010,  (0, 9): 88181,  (0, 10): 66070,
    (1, 0): 40660, (1, 1): 0,      (1, 2): 51980,  (1, 3): 32800,  (1, 4): 99870,  (1, 5): 42210,  (1, 6): 75660,  (1, 7): 63880,  (1, 8): 24350,  (1, 9): 72070,  (1, 10): 26250,
    (2, 0): 25010, (2, 1): 51780,  (2, 2): 0,      (2, 3): 61520,  (2, 4): 74050,  (2, 5): 12890,  (2, 6): 69270,  (2, 7): 52590,  (2, 8): 42910,  (2, 9): 73400,  (2, 10): 76700,
    (3, 0): 54270, (3, 1): 32750,  (3, 2): 61560,  (3, 3): 0,      (3, 4): 77030,  (3, 5): 51930,  (3, 6): 42930,  (3, 7): 31920,  (3, 8): 49480,  (3, 9): 39500,  (3, 10): 29500,
    (4, 0): 94930, (4, 1): 100030, (4, 2): 74070,  (4, 3): 76930,  (4, 4): 0,      (4, 5): 81260,  (4, 6): 55600,  (4, 7): 46100,  (4, 8): 111960, (4, 9): 61700,  (4, 10): 106350,
    (5, 0): 15830, (5, 1): 42600,  (5, 2): 12880,  (5, 3): 52340,  (5, 4): 81050,  (5, 5): 0,      (5, 6): 78000,  (5, 7): 61320,  (5, 8): 33730,  (5, 9): 82130,  (5, 10): 67520,
    (6, 0): 88751, (6, 1): 75700,  (6, 2): 69300,  (6, 3): 43030,  (6, 4): 55210,  (6, 5): 78040,  (6, 6): 0,      (6, 7): 17200,  (6, 8): 90550,  (6, 9): 6520,   (6, 10): 68800,
    (7, 0): 73340, (7, 1): 63440,  (7, 2): 52480,  (7, 3): 31830,  (7, 4): 46430,  (7, 5): 61220,  (7, 6): 17130,  (7, 7): 0,      (7, 8): 75520,  (7, 9): 21260,  (7, 10): 61250,
    (8, 0): 25990, (8, 1): 24350,  (8, 2): 43780,  (8, 3): 49530,  (8, 4): 111730, (8, 5): 34010,  (8, 6): 90550,  (8, 7): 75740,  (8, 8): 0,      (8, 9): 88960,  (8, 10): 48920,
    (9, 0): 88411, (9, 1): 71740,  (9, 2): 73420,  (9, 3): 39430,  (9, 4): 61390,  (9, 5): 82160,  (9, 6): 6550,   (9, 7): 21320,  (9, 8): 88830,  (9, 9): 0,      (9, 10): 64010,
    (10, 0): 65440,(10, 1): 26250, (10, 2): 76760, (10, 3): 29330, (10, 4): 106070, (10, 5): 66990,(10, 6): 68760, (10, 7): 61180, (10, 8): 48920, (10, 9): 64080, (10, 10): 0
}


q = { #demand
    1: 721,
    2: 814,
    3: 620,
    4: 311,
    5: 167,
    6: 513,
    7: 568,
    8: 763,
    9: 558,
    10: 636
}


# Create the model
mdl = Model('CVRP')

# Create variables
x = mdl.addVars(A, vtype=GRB.BINARY, name="x")  # If a vehicle travels in an arc
u = mdl.addVars(V, vtype=GRB.CONTINUOUS, name="u")

# Set the objective function
mdl.modelSense = GRB.MINIMIZE
mdl.setObjective(quicksum(x[i, j] * distance[i, j] for i, j in A)) # for each arc * distance, for all the arcs in A

# Add the constraints
#mdl.addConstrs(quicksum(x[i, j] for j in V if j != i) == 1 for i in range(1, n+1))
#mdl.addConstrs(quicksum(x[i, j] for i in V if i != j) == 1 for j in range(1, n+1))
mdl.addConstrs(quicksum(x[i, j] for j in V if j != i) == 1 for i in N) # (11) each customer is visited at least once
mdl.addConstrs(quicksum(x[i, j] for i in V if i != j) == 1 for j in N) # (12) each customer is visited at least once

mdl.addConstrs((x[i, j] == 1) >> (u[i] + q[j] == u[j]) for i, j in A if i != 0 and j != 0) # elimination constraint, subtours

#mdl.addConstrs(u[i] >= q[i] for i in range(1, n+1))
mdl.addConstrs(u[i] >= q[i] for i in N) # (14)
#mdl.addConstrs(u[i] <= Q for i in range(1, n+1))
mdl.addConstrs(u[i] <= Q for i in N) # (14)

#mdl.addConstr(quicksum(x[0, j] for j in range(1, n+1)) <= 2)
mdl.addConstr(quicksum(x[0, j] for j in N) <= 2) # At most two vehicles

# Optimize the model
mdl.optimize()

# Get active arcs
active_arcs = [(i, j) for i, j in A if x[i, j].X > 0.9] # Find arcs where x[i, j] is approximately equal to 1

# Create arrays of city names
city_names = ["Kingston_upon_Hull (0) ", "Pocklington (1)", "Brough (2)", "Selby (3)", "Boughton (4)", "Barton_upon_Humber (5)", "Darfield (6)", "Bentley (7)", "Watton (8)", "Cudworth (9)", "Haxby (10)"]

# Set the figure size
plt.figure(figsize=(10, 8))

# Annotate city names
for i, txt in enumerate(city_names):
    plt.annotate(txt, (xc[i], yc[i]), textcoords="offset points", xytext=(0, 10), ha='center')

# Plot solution with active arcs
for i, j in active_arcs:
    plt.plot([xc[i], xc[j]], [yc[i], yc[j]], color="g", zorder=0)
    plt.annotate(city_names[j], (xc[j], yc[j]), textcoords="offset points", xytext=(0, 10), ha='center')
plt.plot(xc[0], yc[0], c='r', marker='s')  # That is the depot
plt.scatter(xc[1:], yc[1:], c='b')  # These are the clients

#Print graphical solution
plt.xlabel("Distance X")
plt.ylabel("Distance Y")
plt.title("DISTANCE MINIMIZATION")

plt.show()

#Print all my values

print("Objective Function: ",str(round(mdl.ObjVal,2)))
for a in mdl.getVars():
    if a.x > 0.9:
        print(str(a.varName)+"="+str(a.x))

