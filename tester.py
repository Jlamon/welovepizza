import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    df = pd.read_csv('./data/pizzas.csv', delimiter=';')
    df_filtered = df.drop(['test', 'du jour', 'test mano', 'Unnamed: 16', 'Unnamed: 17'], axis=1)
    df_only = df_filtered.drop(['Froides', 'Invendues'], axis=1)

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

    print(avg_hsp, len(avg_hsp))
    print(avg_gembloux, len(avg_gembloux))