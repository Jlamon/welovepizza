import base64
import io
import pandas as pd
from dash import html


def file_pizza_uploader(file_content, filename):
    if file_content is not None:
        content_type, content_string = file_content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode()), delimiter=';')
                df_filtered = df.drop(['test', 'du jour', 'test mano', 'Unnamed: 16', 'Unnamed: 17'], axis=1)
                df_only = df_filtered.drop(['Froides', 'Invendues'], axis=1)
                df_only.to_csv('data/user_pizzas.csv', index=False)

        except Exception as e:
            print(e)
            return html.Div(['There was an Error.'])

        return html.Div(['The file has been uploaded'])


def file_revenue_uploader(file_content, filename):
    if file_content is not None:
        content_type, content_string = file_content.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode()))
                df.columns = df.columns.str.replace(' ', '')

                # update the ranges
                global lat_range
                global long_range
                lat_range = (round(df['loc_lat'].min(), 3), round(df['loc_lat'].max(), 3))
                long_range = (round(df['loc_long'].min(), 3), round(df['loc_long'].max(), 3))

                # Update timestep
                global max_timestep
                max_timestep = df['timestep'].max()

                df.to_csv('data/user_input.csv', index=False)

        except Exception as e:
            print(e)
            return html.Div(['There was an Error.'])

        return html.Div(['The file has been uploaded'])
