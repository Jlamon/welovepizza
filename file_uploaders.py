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
                df.to_csv('data/user_pizzas.csv', index=False)

        except Exception as e:
            print(e)
            return html.Div(['There was an Error.'])

        return html.Div(['The file has been uploaded'])
