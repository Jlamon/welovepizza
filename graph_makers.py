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
            # print("first day of the month")
            # It is the first day of the month
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
        for pizz in pizzas:
            weeks_gembloux[key][pizz] = []

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')
        day = date.weekday()

        if 'Gembloux' in row['Distributeur']:
            for pizz in pizzas:
                weeks_gembloux[day][pizz].append(row[pizz])

    mergu = []
    trans = []
    chevre = []
    reine = []
    fromage = []
    margu = []
    poulet = []
    legumes = []

    for key in weeks_gembloux.keys():
        for idx, pizz in enumerate(pizzas):
            temp_gem = weeks_gembloux[key][pizz]
            mean_gem = sum(temp_gem) / len(temp_gem)

            if idx == 0:
                mergu.append(mean_gem)
            elif idx == 1:
                trans.append(mean_gem)
            elif idx == 2:
                chevre.append(mean_gem)
            elif idx == 3:
                reine.append(mean_gem)
            elif idx == 4:
                fromage.append(mean_gem)
            elif idx == 5:
                margu.append(mean_gem)
            elif idx == 6:
                poulet.append(mean_gem)
            else:
                legumes.append(mean_gem)

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    fig = go.Figure(data=[
        go.Bar(name='Marguerita', x=days, y=margu),
        go.Bar(name='Reine', x=days, y=reine),
        go.Bar(name='3 Fromages', x=days, y=fromage),
        go.Bar(name='Chèvre Miel', x=days, y=chevre),
        go.Bar(name='Légumes Grillés', x=days, y=legumes),
        go.Bar(name='Merguez', x=days, y=mergu),
        go.Bar(name='Poulet Oignons', x=days, y=poulet),
        go.Bar(name='Transalpine', x=days, y=trans)
    ])

    fig.update_layout(
        barmode='stack',
        title="Moyenne du nombre de pizzas vendues par jours",
        xaxis_title="Journées",
        yaxis_title="Moyenne",
        height=650
    )

    return dcc.Graph(figure=fig)


def mean_per_pizza_hsp():
    df = pd.read_csv('./data/user_pizzas.csv')

    weeks_hsp = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    pizzas = ['Merguez', 'Transalpine', 'Chèvre Miel', 'Reine', '3 Fromages', 'Marguerita', 'Poulet oignons',
              'Légumes grillés']

    for key in weeks_hsp.keys():
        for pizz in pizzas:
            weeks_hsp[key][pizz] = []

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')
        day = date.weekday()

        if 'Haine' in row['Distributeur']:
            for pizz in pizzas:
                weeks_hsp[day][pizz].append(row[pizz])

    mergu = []
    trans = []
    chevre = []
    reine = []
    fromage = []
    margu = []
    poulet = []
    legumes = []

    for key in weeks_hsp.keys():
        for idx, pizz in enumerate(pizzas):
            temp_hsp = weeks_hsp[key][pizz]
            mean_hsp = sum(temp_hsp) / len(temp_hsp)

            if idx == 0:
                mergu.append(mean_hsp)
            elif idx == 1:
                trans.append(mean_hsp)
            elif idx == 2:
                chevre.append(mean_hsp)
            elif idx == 3:
                reine.append(mean_hsp)
            elif idx == 4:
                fromage.append(mean_hsp)
            elif idx == 5:
                margu.append(mean_hsp)
            elif idx == 6:
                poulet.append(mean_hsp)
            else:
                legumes.append(mean_hsp)

    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

    fig = go.Figure(data=[
        go.Bar(name='Marguerita', x=days, y=margu),
        go.Bar(name='Reine', x=days, y=reine),
        go.Bar(name='3 Fromages', x=days, y=fromage),
        go.Bar(name='Chèvre Miel', x=days, y=chevre),
        go.Bar(name='Légumes Grillés', x=days, y=legumes),
        go.Bar(name='Merguez', x=days, y=mergu),
        go.Bar(name='Poulet Oignons', x=days, y=poulet),
        go.Bar(name='Transalpine', x=days, y=trans)
    ])

    fig.update_layout(
        barmode='stack',
        title="Moyenne du nombre de pizzas vendues par jours",
        xaxis_title="Journées",
        yaxis_title="Moyenne",
        height=650
    )

    return dcc.Graph(figure=fig)
