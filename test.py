import os
import pandas as pd

for file in os.listdir('./data'):
    df = pd.read_csv(os.path.join('./data', file), nrows=10)
    print(f"{file}")
    print(len(df))
    print(df.columns)
    print()
    print()