import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    df = pd.read_csv('./data/pizzas.csv', delimiter=';')
    df_filtered = df.drop(['test', 'du jour', 'test mano', 'Unnamed: 16', 'Unnamed: 17'], axis=1)
    df_only = df_filtered.drop(['Froides', 'Invendues'], axis=1)

    weeks_hsp = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    weeks_gembloux = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    pizzas = ['Merguez', 'Transalpine', 'Chèvre Miel', 'Reine', '3 Fromages', 'Marguerita', 'Poulet oignons', 'Légumes grillés']

    for key in weeks_hsp.keys():
        for pizz in pizzas:
            weeks_hsp[key][pizz] = []
            weeks_gembloux[key][pizz] = []

    for index, row in df.iterrows():
        date = datetime.strptime(row['Date'], '%d/%m/%Y')
        day = date.weekday()

        if 'Haine' in row['Distributeur']:
            for pizz in pizzas:
                weeks_hsp[day][pizz].append(row[pizz])
        elif 'Gembloux' in row['Distributeur']:
            for pizz in pizzas:
                weeks_gembloux[day][pizz].append(row[pizz])

    for key in weeks_hsp.keys():
        for pizz in pizzas:
            temp_hsp = weeks_hsp[key][pizz]
            temp_gem = weeks_gembloux[key][pizz]

            weeks_hsp[key][pizz] = sum(temp_hsp) / len(temp_hsp)
            weeks_gembloux[key][pizz] = sum(temp_gem) / len(temp_gem)

    print(weeks_hsp)
    print(weeks_gembloux)