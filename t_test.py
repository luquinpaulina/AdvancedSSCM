import pandas as pd
import numpy as np
from scipy.stats import ttest_rel
import matplotlib.pyplot as plt

# Create lists to store the distances for each instance
total_distances = []
min_distances = []
max_distances = []
average_distances = []
average_distances_depot = []

num_instances = 20  # Number of instances (c1.txt, c2.txt, ..., c20.txt)
base_path = 'C:\\Users\\luqui\\PycharmProjects\\AdvancedSSCM\\DATA\\c'  # Base path for the data files

for i in range(1, num_instances + 1):
    file_path = f"{base_path}{i}.txt"
    df = pd.read_csv(file_path, delim_whitespace=True)

    # Extract data from the dataframe
    n = len(df) - 1  # number of clients
    xc = df['XCOORD'].tolist()  # location of clients + depot
    yc = df['YCOORD'].tolist()  # location of clients + depot

    N = [i for i in range(1, n + 1)]  # Set of clients [1,2,3,4,5,6,7,8,9,10]
    V = [0] + N  # The union of 0 + N [0,1,2,3,4,5,6,7,8,9,10]
    A = [(i, j) for i in V for j in V if i != j]  # [(0,1), (0,2],...,(10,9]]
    # Create dictionary for distance
    c = {(i, j): np.hypot(xc[i] - xc[j], yc[i] - yc[j]) for i, j in A}

    # Compute the total distance per instance
    total_distance = sum(c.values())
    # Compute the minimum, maximum, and average distances
    min_distance = min(c.values())
    max_distance = max(c.values())
    average_distance = total_distance / len(c)
    # Compute the average distance to the depot
    depot_distances = [c[(i, 0)] for i in N]  # Distances from each node to the depot (0)
    average_distance_depot = np.mean(depot_distances)
    average_distances_depot.append(average_distance_depot)


    # Store the distances
    total_distances.append(total_distance)
    min_distances.append(min_distance)
    max_distances.append(max_distance)
    average_distances.append(average_distance)


# Sample arrays
sample_1 = np.array(total_distances)
sample_2 = np.array(min_distances)
sample_3 = np.array(max_distances)
sample_4 = np.array(average_distances)
sample_5 = np.array(average_distances_depot)

from scipy.stats import f_oneway

# Combine all the samples into a single array
all_samples = np.concatenate([sample_1, sample_2, sample_3, sample_4, sample_5])

# Create an array of labels for each group within each sample
sample_labels = ['sample_1'] * len(sample_1) + ['sample_2'] * len(sample_2) + ['sample_3'] * len(sample_3) + \
                ['sample_4'] * len(sample_4) + ['sample_5'] * len(sample_5)

# Perform one-way ANOVA
f_value, p_value = f_oneway(sample_1, sample_2, sample_3, sample_4, sample_5)

# Print the results
print("One-way ANOVA results:")
print(f"F-value: {f_value}")
print(f"p-value: {p_value}")

