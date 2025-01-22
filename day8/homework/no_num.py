import random
import time
import matplotlib.pyplot as plt

def generate_random_segments(num_segments, x_range=(-10, 10), y_range=(-10, 10)):
    segments = []
    for _ in range(num_segments):
        x1 = random.randint(x_range[0], x_range[1])
        y1 = random.randint(y_range[0], y_range[1])
        x2 = random.randint(x_range[0], x_range[1])
        y2 = random.randint(y_range[0], y_range[1])
        segments.append([x1, y1, x2, y2])
    return segments

def measure_performance(num_segments):
    segments = generate_random_segments(num_segments)
    rectangle = [-5, -5, 5, 5]

    start_time = time.time()
    filtered_segments_python = filter_segments(segments, rectangle)
    python_duration = time.time() - start_time

    print(f"Filtered {len(filtered_segments_python)} segments using plain Python in {python_duration:.4f} seconds.")
    
    return segments, filtered_segments_python

def visualize(segments, filtered_segments):
    plt.figure(figsize=(10, 10))
    
    for seg in segments:
        plt.plot([seg[0], seg[2]], [seg[1], seg[3]], 'b-', alpha=0.5)

    for seg in filtered_segments:
        plt.plot([seg[0], seg[2]], [seg[1], seg[3]], 'r-', linewidth=2)

    rect = plt.Rectangle((-5, -5), 10, 10, fill=None, edgecolor='green', linewidth=2)
    plt.gca().add_patch(rect)

    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.title('Segments Filtering')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    num_segments = 100000
    segments, filtered_segments_python = measure_performance(num_segments)
    
    visualize(segments, filtered_segments_python)
