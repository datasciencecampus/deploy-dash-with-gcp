import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from io import StringIO
import os

from data.dataDownloader import GCPDownloaderLocal, GCPDownloaderCloud

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

def data_in():

    if cloud == False:
        data = os.path.join('data/data.csv')

    else:
        project = 'dash-example-265811'
        project_name = 'dash-example-265811.appspot.com'
        folder_name = 'data'
        file_name = 'data.csv'

        if local == True:
            GCP = GCPDownloaderLocal() # run locally
        else:
            GCP = GCPDownloaderCloud()  # run on cloud

        bytes_file = GCP.getData(project, project_name, folder_name, file_name)
        s = str(bytes_file, encoding='utf-8')
        data = StringIO(s)

    data_df = pd.read_csv(data)

    add_num_list = []
    multiply_num_list = []

    for index, row in data_df.iterrows():
        add_num_list.append(add_numbers(row['first_num'], row['second_num']))
        multiply_num_list.append(multiply_numbers(row['first_num'], row['second_num']))

    data_df['add_num'] = add_num_list
    data_df['multiply_num'] = multiply_num_list

    return data_df

def app_layout():
    data_df = data_in()
    return html.Div(children=[
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


# -------------------------- TEXT ---------------------------- #


dash_text = '''

This is an example of a DSC dashboard.
'''


# -------------------------- DASH ---------------------------- #


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='assets')
server = app.server

local = False
cloud = True

data_df = data_in()

app.layout = app_layout
app.config.suppress_callback_exceptions = True


# -------------------------- MAIN ---------------------------- #


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)