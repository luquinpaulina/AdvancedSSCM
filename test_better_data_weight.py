# THIS PROBLEM IS DISTANCE MINIMIZATION WITH SOLOMON DATA 01/07/2023
# THIS IS CORRECT, PRINTING TO FILE
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
import pandas as pd

num_instances = 20  # Number of instances (c1.txt, c2.txt, ..., c20.txt)
base_path = 'C:\\Users\\luqui\\PycharmProjects\\AdvancedSSCM\\DATA\\c'  # Base path for the data files

output_file = open("output_weight2.txt", "w")  # Open the output file in write mode

for i in range(1, num_instances + 1):
    file_path = f"{base_path}{i}.txt"
    df = pd.read_csv(file_path, delim_whitespace=True)

    # Extract data from the dataframe
    n = len(df) - 1  # number of clients
    w = 80  # curb weight
    xc = df['XCOORD'].tolist()  # location of clients + depot
    yc = df['YCOORD'].tolist()  # location of clients + depot
    q = df['DEMAND'].tolist()  # demand of each client

    N = [i for i in range(1, n + 1)]  # Set of clients [1,2,3,4,5,6,7,8,9,10]
    V = [0] + N  # The union of 0 + N [0,1,2,3,4,5,6,7,8,9,10]
    A = [(i, j) for i in V for j in V if i != j]  # [(0,1), (0,2],...,(10,9]]
    # Create dictionary for distance
    c = {(i, j): np.hypot(xc[i] - xc[j], yc[i] - yc[j]) for i, j in A}
    Q = 80  # vehicle capacity
    q = df['DEMAND'].tolist()  # EXTRACTED FROM SOLOMON DATA

    # Create the model
    mdl = Model('CVRP')

    # Create variables
    x = mdl.addVars(A, vtype=GRB.BINARY, name="x")  # If a vehicle travels in an arc
    f = mdl.addVars(A, vtype=GRB.CONTINUOUS,
                    name="f")  # the amount of commodity flowing at which a vehicle travels on this arc

    # objective function
    mdl.modelSense = GRB.MINIMIZE
    mdl.setObjective(quicksum(c[i, j] * w * x[i, j] for i, j in A) + quicksum(c[i, j] * f[i, j] for i, j in A))

    # constraint 10 //four vehicles
    mdl.addConstr(quicksum(x[0, j] for j in N) <= 4)
    # softened the constraint to make instance feasible

    # constraint 11
    mdl.addConstrs(quicksum(x[i, j] for j in V if j != i) == 1 for i in N)
    # Changed V to N as more than 1 truck is allowed to leave the depot

    # constraint 12
    mdl.addConstrs(quicksum(x[i, j] for i in V if i != j) == 1 for j in N)
    # Changed V to N as more than 1 truck is allowed to return to the depot

    # constraint 13
    mdl.addConstrs(quicksum(f[j, i] for j in V if j != i) - quicksum(f[i, j] for j in V if j != i) == q[i] for i in N)
    # changed formulation as the sums do only iterate over j not i

    # constraint 14
    mdl.addConstrs(q[j] * x[i, j] <= f[i, j] for (i, j) in A)
    mdl.addConstrs(f[i, j] <= (Q - q[i]) * x[i, j] for (i, j) in A)
    # change u-formulation to constraints from the paper

    # constraint 20
    mdl.addConstrs(f[i, j] >= 0 for i, j in A)

    # Optimize the model
    mdl.optimize()

    # Get active arcs
    active_arcs = [(i, j) for i, j in A if x[i, j].X > 0]

    # Print all my values
    output_file.write("Objective Function: " + str(round(mdl.ObjVal, 2)) + "\n")
    for a in mdl.getVars():
        if a.x > 0.9:
            output_file.write(str(a.varName) + "=" + str(a.x) + "\n")

    # Create a dictionary mapping varName f[a,b] to x value
    var_dict = {a.varName: a.x for a in mdl.getVars() if a.x > 0.9 and a.varName.startswith("x")}

    # Print the dictionary
    # for var_name, var_value in var_dict.items():
    #       print(f"{var_name} = {var_value}")

    # Calculate the sum of all totals
    total_sum = 0

    # Calculate "total" for each index in var_dict
    for var_name, var_value in var_dict.items():
        i, j = [int(s) for s in var_name.split('[')[1].split(']')[0].split(',')]
        distance = c[i, j]
        total = distance
        total_sum += total
        output_file.write(f"Total for {var_name}: {total}\n")

    output_file.write("Sum of all totals: " + str(total_sum) + "\n")
    output_file.write("\n")  # Add a blank line between instances

output_file.close()  # Close the output file
