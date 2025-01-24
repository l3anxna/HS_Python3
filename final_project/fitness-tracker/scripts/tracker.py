import sys
import pandas as pd

filename = "fitness_data.csv"

date, steps, calories = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

try:
    data = pd.read_csv(filename)
except FileNotFoundError:
    data = pd.DataFrame(columns=["Date", "Steps", "Calories"])

new_entry = {"Date": date, "Steps": steps, "Calories": calories}
data = data.append(new_entry, ignore_index=True)
data.to_csv(filename, index=False)

print("Entry added successfully!")
