import numpy as np
import time
import matplotlib.pyplot as plt


def generate_segments(n, max_value=10):
    return np.random.uniform(0, max_value, size=(n, 2, 2))


def filter_segments_numpy(segments, min_length):
    x1, y1 = segments[:, 0, 0], segments[:, 0, 1]
    x2, y2 = segments[:, 1, 0], segments[:, 1, 1]
    lengths = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    mask = lengths > min_length
    return segments[mask]


def plot_segments(all_segments, filtered_segments):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].set_title("All Segments")
    for segment in all_segments:
        x, y = zip(*segment)
        axes[0].plot(x, y, alpha=0.5)

    axes[1].set_title("Filtered Segments")
    for segment in filtered_segments:
        x, y = zip(*segment)
        axes[1].plot(x, y, alpha=0.8)

    plt.show()


if __name__ == "__main__":
    num_segments = 10000
    min_length = 5

    segments = generate_segments(num_segments)

    print("Starting filtering using NumPy...")
    start_time = time.time()
    filtered_segments = filter_segments_numpy(segments, min_length)
    elapsed_time = time.time() - start_time

    print(f"NumPy filtering took {elapsed_time:.6f} seconds.")

    plot_segments(segments, filtered_segments)
