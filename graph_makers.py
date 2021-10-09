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
        title="Moyenne vendues par semaine",
        xaxis_title="Distributeurs",
        yaxis_title="Moyenne",
        height=650
    )

    return fig


def mean_per_day_maker():
    df = pd.read_csv('./data/user_pizzas.csv')

    weeks_hsp = {}
    weeks_gembloux = {}
    temp_hsp = 0
    temp_gembloux = 0

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')

        if 'Haine' in row['Distributeur']:
            if date.weekday() in weeks_hsp.keys():
                temp = weeks_hsp[date.weekday()]
                weeks_hsp[date.weekday()] = temp + [row['Total']]
            else:
                weeks_hsp[date.weekday()] = [row['Total']]
        elif 'Gembloux' in row['Distributeur']:
            if date.weekday() in weeks_gembloux.keys():
                temp = weeks_gembloux[date.weekday()]
                weeks_gembloux[date.weekday()] = temp + [row['Total']]
            else:
                weeks_gembloux[date.weekday()] = [row['Total']]

    avg_hsp = []
    avg_gembloux = []

    for key in weeks_hsp.keys():
        temp = sum(weeks_hsp[key]) / len(weeks_hsp[key])
        avg_hsp.append(temp)
    for key in weeks_gembloux.keys():
        temp = sum(weeks_gembloux[key]) / len(weeks_gembloux[key])
        avg_gembloux.append(temp)

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    fig = go.Figure([go.Bar(x=days, y=avg_hsp)])
    fig.update_layout(
        title="Moyenne vendues par jour pour HSP seulement",
        xaxis_title="Journées",
        yaxis_title="Moyenne",
        height=650
    )

    return fig
