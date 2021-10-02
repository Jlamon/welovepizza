import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def mean_week_maker():
    df = pd.read_csv('./data/user_pizzas.csv')
    total_hsp = []
    total_gembloux = []
    total = []
    temp_hsp = 0
    temp_gembloux = 0
    temp_total = 0

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')

        if date.weekday() == 0:
            total_hsp.append(temp_hsp)
            total_gembloux.append(temp_gembloux)
            total.append(temp_total)
            temp_hsp = 0
            temp_gembloux = 0
            temp_total = 0

        if 'Haine' in row['Distributeur']:
            temp_hsp += row['Total']
        elif 'Gembloux' in row['Distributeur']:
            temp_gembloux += row['Total']
        elif 'Sélection' in row['Distributeur']:
            temp_total += row['Total']

    avg_hsp = sum(total_hsp) / len(total_hsp)
    avg_gembloux = sum(total_gembloux) / len(total_gembloux)
    avg_total = sum(total) / len(total)
    distribs = ['Haine Saint Paul', 'Gembloux', 'Total']

    fig = go.Figure([go.Bar(x=distribs, y=[avg_hsp, avg_gembloux, avg_total])])
    fig.update_layout(
        title="Moyenne de pizzas vendues par semaine",
        xaxis_title="Distributeurs",
        yaxis_title="Moyenne",
        height=650
    )

    return fig


def mean_day_maker():
    df = pd.read_csv('./data/user_pizzas.csv')
    counter_hsp = 0
    counter_gembloux = 0
    counter_total = 0
    total_hsp = 0
    total_gembloux = 0
    total = 0

    for index, row in df.iterrows():
        if 'Haine' in row['Distributeur']:
            total_hsp += row['Total']
            counter_hsp += 1
        elif 'Gembloux' in row['Distributeur']:
            total_gembloux += row['Total']
            counter_gembloux += 1
        elif 'Sélection' in row['Distributeur']:
            total += row['Total']
            counter_total += 1

    avg_hsp = total_hsp / counter_hsp
    avg_gembloux = total_gembloux / counter_gembloux
    avg_total = total / counter_total
    distribs = ['Haine Saint Paul', 'Gembloux', 'Total']

    fig = go.Figure([go.Bar(x=distribs, y=[avg_hsp, avg_gembloux, avg_total])])
    fig.update_layout(
        title="Moyenne de pizzas vendues par jour",
        xaxis_title="Distributeurs",
        yaxis_title="Moyenne",
        height=650
    )

    return fig
