
import numpy as np

# Generate random data (coordinates, time windows, travel times)
def generate_data(num_cities, seed=42):
    np.random.seed(seed)
    coords = np.random.rand(num_cities, 2) * 100  # Random coordinates for cities
    time_windows = np.sort(np.random.randint(0, 100, size=(num_cities, 2)), axis=1)  # Time windows [e_i, l_i]
    travel_time = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(-1))  # Euclidean travel times
    return coords, time_windows, travel_time
