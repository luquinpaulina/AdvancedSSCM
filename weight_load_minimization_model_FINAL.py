# THIS PROBLEM IS WEIGHT LOAD MINIMIZATION WITH SOLOMON DATA 27/06/2023
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
    print("Objective Function: ", str(round(mdl.ObjVal, 2)))
    for a in mdl.getVars():
        if a.x > 0.9:
            print(str(a.varName) + "=" + str(a.x))

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
        print(f"Total for {var_name}: {total}")

    print("Sum of all totals:", total_sum)
    print(c)  # uncomment to see correct distances

    # Create arrays of city names
    city_names = ["Kingston_upon_Hull (0) ", "Pocklington (1)", "Brough (2)", "Selby (3)", "Boughton (4)",
                  "Barton_upon_Humber (5)", "Darfield (6)", "Bentley (7)", "Watton (8)", "Cudworth (9)", "Haxby (10)"]

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

    # Print graphical solution
    plt.xlabel("Distance X")
    plt.ylabel("Distance Y")
    plt.title("WEIGHT LOAD MINIMIZATION")

    # Get the legend text from the var_dict
    legend_text = [f"{var_name} = {var_value}" for var_name, var_value in var_dict.items()]

    plt.legend(legend_text, loc='best')

    plt.show()

