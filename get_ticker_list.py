import pandas as pd

df = pd.read_csv("data/bats_symbols.csv")
tickers = list(df["Name"])
print(tickers)