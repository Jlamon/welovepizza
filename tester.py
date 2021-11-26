import math

import pandas as pd
from datetime import datetime

if __name__ == '__main__':
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
        sub_percentage.append(round((el / sum(sub_totals)) * 100, 2))

    table.loc[len(table.index)] = sub_totals
    table.loc[len(table.index)] = sub_percentage

    table = table.reset_index()
    table = table.rename({"index": "Pizzas", 0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"},
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
        sub_percentage_pizza.append(round((el / sum(last_col)) * 100, 2))
    sub_percentage_pizza.append("")
    sub_percentage_pizza.append("")
    table["%/Pizza"] = sub_percentage_pizza

    print(table)
