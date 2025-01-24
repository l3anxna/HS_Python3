import numpy as np
import matplotlib.pyplot as plt

N =50
points = np.random.rand(N,2)
distances = np.sqrt(points[:,0] ** 2 + points[:,1] ** 2)

plt.figure(figsize=(6,6))
plt.scatter(points[:,0], points[:,1], c=distances, cmap='viridis')
plt.colorbar()
plt.grid()
plt.show()