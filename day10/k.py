import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv('csv/points.csv', header=None)
points = df.values

x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])

print(f"X bounds: {x_min} to {x_max}")
print(f"Y bounds: {y_min} to {y_max}")

num_clusters = 3

kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(points)
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

print(f"Cluster centroids:\n{centroids}")

plt.scatter(points[:, 0], points[:, 1], c=labels, cmap='viridis', marker='o')

plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x')

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Clusters and Centroids')

plt.show()