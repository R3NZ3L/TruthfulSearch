import numpy as np
import pandas as pd

filename = "covid_philippines"
path = "datasets/" + filename + "/" + 'videos' + ".csv"
dataset = pd.read_csv(path).drop("Unnamed: 0", axis=1)
print(dataset.to_json())