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

    test = pd.DataFrame.from_dict(weeks_gembloux)

    sub_totals = []
    for col in test:
        sub_totals.append(sum(test[col]))

    test.loc[len(test.index)] = sub_totals

    test = test.reset_index()
    test = test.rename({"index": "Pizzas", 0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi", 6: "Dimanche"},
                       axis=1)

    print(test)
