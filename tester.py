import base64
import io
import pandas as pd
from dash import html

if __name__ == '__main__':
    df = pd.read_csv('./data/pizzas.csv', delimiter=';')
    df_filtered = df.drop(['test', 'du jour', 'test mano', 'Unnamed: 16', 'Unnamed: 17'], axis=1)
    df_only = df_filtered.drop(['Froides', 'Invendues'], axis=1)
    print(df_only.head())