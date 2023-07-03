import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create lists to store the distances for each instance
total_distances = []
min_distances = []
max_distances = []
average_distances = []
average_distances_depot = []

num_instances = 20  # Number of instances (c1.txt, c2.txt, ..., c20.txt)
base_path = 'C:\\Users\\luqui\\PycharmProjects\\AdvancedSSCM\\DATA\\c'  # Base path for the data files

highlight_indices = [1, 2, 4, 6, 8, 9, 11, 13, 15, 16, 18]  # Indices to highlight

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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ... (rest of the code remains the same as before)

# Create a figure and axes for the histograms
fig, axs = plt.subplots(2, 2, figsize=(12, 8))

# Total Distance histogram
n, bins, patches = axs[0, 0].hist(average_distances_depot, bins=10, edgecolor='black', color='blue', alpha=0.7)
highlight_indices_adjusted = [index - 1 for index in highlight_indices if index - 1 >= 0 and index - 1 < len(patches)]
for index in highlight_indices_adjusted:
    patches[index].set_facecolor('orange')
axs[0, 0].set_title('Average Distance to Depot')
axs[0, 0].set_xlabel('Distance')
axs[0, 0].set_ylabel('Frequency')

# Minimum Distance histogram
n, bins, patches = axs[0, 1].hist(min_distances, bins=10, edgecolor='black', color='blue', alpha=0.7)
highlight_indices_adjusted = [index - 1 for index in highlight_indices if index - 1 >= 0 and index - 1 < len(patches)]
for index in highlight_indices_adjusted:
    patches[index].set_facecolor('orange')
axs[0, 1].set_title('Minimum Distance')
axs[0, 1].set_xlabel('Distance')
axs[0, 1].set_ylabel('Frequency')

# Maximum Distance histogram
n, bins, patches = axs[1, 0].hist(max_distances, bins=10, edgecolor='black', color='blue', alpha=0.7)
highlight_indices_adjusted = [index - 1 for index in highlight_indices if index - 1 >= 0 and index - 1 < len(patches)]
for index in highlight_indices_adjusted:
    patches[index].set_facecolor('orange')
axs[1, 0].set_title('Maximum Distance')
axs[1, 0].set_xlabel('Distance')
axs[1, 0].set_ylabel('Frequency')

# Average Distance histogram
n, bins, patches = axs[1, 1].hist(average_distances, bins=10, edgecolor='black', color='blue', alpha=0.7)
highlight_indices_adjusted = [index - 1 for index in highlight_indices if index - 1 >= 0 and index - 1 < len(patches)]
for index in highlight_indices_adjusted:
    patches[index].set_facecolor('orange')
axs[1, 1].set_title('Average Distance from Node to Node')
axs[1, 1].set_xlabel('Distance')
axs[1, 1].set_ylabel('Frequency')

# Adjust the layout and spacing
fig.tight_layout()

# Show the plots
plt.show()






