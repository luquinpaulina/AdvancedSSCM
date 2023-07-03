from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

num_instances = 20  # Number of instances (c1.txt, c2.txt, ..., c20.txt)
base_path = 'C:\\Users\\luqui\\PycharmProjects\\AdvancedSSCM\\DATA\\c'  # Base path for the data files

# Combine the coordinates of all instances
all_xc = []
all_yc = []
for i in range(1, num_instances + 1):
    file_path = f"{base_path}{i}.txt"
    df = pd.read_csv(file_path, delim_whitespace=True)
    xc = df['XCOORD'].tolist()
    yc = df['YCOORD'].tolist()
    all_xc.extend(xc)
    all_yc.extend(yc)

# Convert coordinates to a NumPy array
X = np.array(list(zip(all_xc, all_yc)))

# Apply k-means clustering
k = 5  # Number of clusters
kmeans = KMeans(n_clusters=k)
kmeans.fit(X)

# Get the cluster labels
labels = kmeans.labels_

# Plot the clustered nodes
plt.scatter(X[:, 0], X[:, 1], c=labels)
plt.xlabel("Distance X")
plt.ylabel("Distance Y")
plt.title("Clustered Nodes")
plt.show()
