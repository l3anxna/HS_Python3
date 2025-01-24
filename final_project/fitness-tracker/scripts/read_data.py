import pandas as pd
import json

filename = "fitness_data.csv"

try:
    data = pd.read_csv(filename)
    print(data.to_json(orient="records"))
except FileNotFoundError:
    print("[]")
