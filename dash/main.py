import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
from io import StringIO

from data.dataDownloader import GCPDownloader

# -------------------------- PYTHON FUNCTIONS ---------------------------- #


def add_numbers(first_num,second_num):
    new_num = first_num + second_num
    return new_num

def multiply_numbers(first_num,second_num):
    new_num = first_num * second_num
    return new_num


def build_banner():
    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.Img(src=app.get_asset_url('dsc-logo2.png')),
        ],
    )


# -------------------------- LOAD DATA ---------------------------- #

# local data
# data = os.path.join('data/data.csv')

# cloud data
project_name = 'dash-example-265811.appspot.com'
folder_name = 'data'
file_name = 'data.csv'
GCP = GCPDownloader()
bytes_file = GCP.getData(project_name, folder_name, file_name)
s = str(bytes_file,'utf-8')
data = StringIO(s)

data_df = pd.read_csv(data)

add_num_list = []
multiply_num_list = []

for index, row in data_df.iterrows():
    add_num_list.append(add_numbers(row['first_num'], row['second_num']))
    multiply_num_list.append(multiply_numbers(row['first_num'], row['second_num']))

data_df['add_num'] = add_num_list
data_df['multiply_num'] = multiply_num_list


# -------------------------- TEXT ---------------------------- #


dash_text = '''

This is an example of a DSC dashboard.
'''


# -------------------------- DASH ---------------------------- #


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='assets')

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True


# -------------------------- PROJECT DASHBOARD ---------------------------- #


app.layout = html.Div(children=[
    html.H1(
        children=[
            build_banner(),
            html.P(
                id='instructions',
                children=dash_text),
            ]
    ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': data_df.index.values.tolist(), 'y': data_df['add_num'], 'type': 'bar', 'name': 'Add Numbers'},
                {'x': data_df.index.values.tolist(), 'y': data_df['multiply_num'], 'type': 'bar', 'name': 'Multiply Numbers'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])



# -------------------------- MAIN ---------------------------- #


if __name__ == '__main__':
    load_data_source = 'local'
    app.run_server(host='0.0.0.0', port=8000, debug=True)
