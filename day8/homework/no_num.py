import random
import time
import matplotlib.pyplot as plt


def generate_segments(n, max_value=10):
    return [
        [
            (random.uniform(0, max_value), random.uniform(0, max_value)),
            (random.uniform(0, max_value), random.uniform(0, max_value)),
        ]
        for _ in range(n)
    ]


def filter_segments_python(segments, min_length):
    filtered_segments = []
    for segment in segments:
        x1, y1 = segment[0]
        x2, y2 = segment[1]
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if length > min_length:
            filtered_segments.append(segment)
    return filtered_segments


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

    start_time = time.time()
    filtered_segments = filter_segments_python(segments, min_length)
    elapsed_time = time.time() - start_time

    print(f"Python filtering took {elapsed_time:.6f} seconds.")

    plot_segments(segments, filtered_segments)
