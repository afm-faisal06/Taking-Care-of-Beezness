import numpy as np
import csv

def load_terrain_csv(filename):
    return np.loadtxt(filename, delimiter=',', dtype=int)

def load_params_csv(filename):
    params = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            key, value = row[0].strip(), row[1].strip()
            try:
                params[key] = eval(value)
            except:
                params[key] = value
    return params

