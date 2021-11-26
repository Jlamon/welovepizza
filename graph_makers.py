import math

import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from datetime import datetime


def per_pizza_all_time():
    df = pd.read_csv('./data/user_pizzas.csv')
    total_global = 0
    total = {}

    pizzas = ['Merguez', 'Transalpine', 'Chèvre Miel', 'Reine', '3 Fromages', 'Marguerita', 'Poulet oignons',
              'Légumes grillés']

    for pizza in pizzas:
        total[pizza] = 0

    for index, row in df.iterrows():
        if 'Sélection' in row['Distributeur']:
            for pizza in pizzas:
                total_global = total_global + row[pizza]
                total[pizza] = total[pizza] + row[pizza]

    fig = go.Figure(data=[go.Pie(labels=list(total.keys()), values=list(total.values()))])

    title = "% de vente par sorte de pizza (2 distributeurs assemblés) <br><b>Total Global:</b> " + str(total_global)
    fig.update_layout(
        title=title,
        height=650
    )

    return dcc.Graph(figure=fig)


def mean_month_maker():
    df = pd.read_csv('./data/user_pizzas.csv')
    total_hsp = []
    total_gembloux = []
    total = []
    temp_hsp = 0
    temp_gembloux = 0
    temp_total = 0

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')

        if date.day == 1:
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
        title="Moyenne du nombre de pizzas vendues par mois",
        xaxis_title="Distributeurs",
        yaxis_title="Moyenne",
        height=650
    )

    return dcc.Graph(figure=fig)


def mean_per_day_maker():
    df = pd.read_csv('./data/user_pizzas.csv')

    weeks_hsp = {}
    weeks_gembloux = {}

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

    for key in sorted(weeks_hsp.keys()):
        temp = sum(weeks_hsp[key]) / len(weeks_hsp[key])
        avg_hsp.append(temp)
    for key in sorted(weeks_gembloux.keys()):
        temp = sum(weeks_gembloux[key]) / len(weeks_gembloux[key])
        avg_gembloux.append(temp)

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    fig = go.Figure(data=[
        go.Bar(name='Haine Saint Paul', x=days, y=avg_hsp),
        go.Bar(name='Gembloux', x=days, y=avg_gembloux)
    ])

    fig.update_layout(
        title="Moyenne du nombre de pizzas vendues par jours",
        xaxis_title="Journées",
        yaxis_title="Moyenne",
        height=650
    )

    return dcc.Graph(figure=fig)


def mean_per_pizza_gembloux():
    df = pd.read_csv('./data/user_pizzas.csv')

    weeks_gembloux = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    pizzas = ['Merguez', 'Transalpine', 'Chèvre Miel', 'Reine', '3 Fromages', 'Marguerita', 'Poulet oignons',
              'Légumes grillés']

    for key in weeks_gembloux.keys():
        for pizza in pizzas:
            weeks_gembloux[key][pizza] = []

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')
        day = date.weekday()

        if 'Gembloux' in row['Distributeur']:
            for pizza in pizzas:
                weeks_gembloux[day][pizza].append(row[pizza])

    for key in weeks_gembloux.keys():
        for idx, pizza in enumerate(pizzas):
            temp_gem = weeks_gembloux[key][pizza]
            mean_gem = sum(temp_gem) / len(temp_gem)
            weeks_gembloux[key][pizza] = math.ceil(mean_gem)

    table = pd.DataFrame.from_dict(weeks_gembloux)

    sub_totals = []
    for col in table:
        sub_totals.append(sum(table[col]))

    sub_percentage = []
    for el in sub_totals:
        percentage = str(round((el / sum(sub_totals)) * 100, 2)) + " %"
        sub_percentage.append(percentage)

    table.loc[len(table.index)] = sub_totals
    table.loc[len(table.index)] = sub_percentage

    table = table.reset_index()
    table = table.rename(
        {"index": "Pizzas", 0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi",
         6: "Dimanche"},
        axis=1)
    table.loc[len(table.index) - 2, 'Pizzas'] = "<b> Total Journalier"
    table.loc[len(table.index) - 1, 'Pizzas'] = "<b> % Journalier"

    column_list = list(table)
    column_list.remove('Pizzas')

    table["Total/Pizza"] = table[column_list].sum(axis=1)
    table.loc[len(table.index) - 1, 'Total/Pizza'] = ""

    sub_percentage_pizza = []
    last_col = list(table["Total/Pizza"])[:-2]
    for el in last_col:
        percentage = str(round((el / sum(last_col)) * 100, 2)) + " %"
        sub_percentage_pizza.append(percentage)
    sub_percentage_pizza.append("")
    sub_percentage_pizza.append("")
    table["%/Pizza"] = sub_percentage_pizza

    fig = go.Figure(data=[
        go.Table(
            header=dict(values=["<b>" + column for column in table]),
            cells=dict(values=[table[column] for column in table],
                       height=30)
        )
    ])

    fig.update_layout(
        title="Moyenne du nombre de pizzas vendues par jours",
        height=650
    )

    return dcc.Graph(figure=fig)


def mean_per_pizza_hsp():
    df = pd.read_csv('./data/user_pizzas.csv')

    weeks_hsp = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    pizzas = ['Merguez', 'Transalpine', 'Chèvre Miel', 'Reine', '3 Fromages', 'Marguerita', 'Poulet oignons',
              'Légumes grillés']

    for key in weeks_hsp.keys():
        for pizza in pizzas:
            weeks_hsp[key][pizza] = []

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')
        day = date.weekday()

        if 'Haine' in row['Distributeur']:
            for pizza in pizzas:
                weeks_hsp[day][pizza].append(row[pizza])

    for key in weeks_hsp.keys():
        for idx, pizza in enumerate(pizzas):
            temp_hsp = weeks_hsp[key][pizza]
            mean_hsp = sum(temp_hsp) / len(temp_hsp)
            weeks_hsp[key][pizza] = math.ceil(mean_hsp)

    table = pd.DataFrame.from_dict(weeks_hsp)

    sub_totals = []
    for col in table:
        sub_totals.append(sum(table[col]))

    sub_percentage = []
    for el in sub_totals:
        percentage = str(round((el / sum(sub_totals)) * 100, 2)) + " %"
        sub_percentage.append(percentage)

    table.loc[len(table.index)] = sub_totals
    table.loc[len(table.index)] = sub_percentage

    table = table.reset_index()
    table = table.rename(
        {"index": "Pizzas", 0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"},
        axis=1)
    table.loc[len(table.index) - 2, 'Pizzas'] = "<b> Total Journalier"
    table.loc[len(table.index) - 1, 'Pizzas'] = "<b> % Journalier"

    column_list = list(table)
    column_list.remove('Pizzas')

    table["Total/Pizza"] = table[column_list].sum(axis=1)
    table.loc[len(table.index) - 1, 'Total/Pizza'] = ""

    sub_percentage_pizza = []
    last_col = list(table["Total/Pizza"])[:-2]
    for el in last_col:
        percentage = str(round((el / sum(last_col)) * 100, 2)) + " %"
        sub_percentage_pizza.append(percentage)
    sub_percentage_pizza.append("")
    sub_percentage_pizza.append("")
    table["%/Pizza"] = sub_percentage_pizza

    fig = go.Figure(data=[
        go.Table(
            header=dict(values=["<b>" + column for column in table]),
            cells=dict(values=[table[column] for column in table],
                       height=30)
        )
    ])

    fig.update_layout(
        title="Moyenne du nombre de pizzas vendues par jours",
        height=650
    )

    return dcc.Graph(figure=fig)
