import dash
import joblib
import json
import plotly
import time

import dash_core_components as dcc
import dash_html_components as html
#import dash_table as dt
import dash_table_experiments as dt
import matplotlib.pyplot as plt
import matplotlib.colors
import plotly.graph_objs as go
import dash_ui as dui
import pandas as pd
import numpy as np
from IPython.display import HTML


from dash.dependencies import Input, Output, State

data_dir = '/home/cdsw/airline-sentiment/data'

def value_to_hex_color(value, vmin=0, vmax=1):
    cmap = plt.cm.inferno
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    return matplotlib.colors.to_hex(cmap(norm([value][0])))


app = dash.Dash(__name__, static_folder='data')
app.title = 'Cloudera CDSW 1.6 Demo'
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

DATA = data_dir+'/umap_embedding.joblib'
features = ['tweet', 'prediction', 'airline', 'umap_x', 'umap_y']

cluster_data = joblib.load(DATA)
cluster_data = cluster_data[features]

cluster_data['marker_color'] = cluster_data['prediction'].apply(lambda x: value_to_hex_color(x)) 


# CSS grid layout for easy positioning
grid = dui.Grid(
    _id="grid",
    num_rows=12,
    num_cols=12,
    grid_padding=5
)


grid.add_element(
    col=6,
    row=1,
    width=6,
    height=6,
    element=dcc.Graph(id='umap'),
)

grid.add_element(
    col=7,
    row=10,
    width=1,
    height=1,
    element = dcc.RadioItems(
        id='model-select',
        options=[
            {'label': 'all', 'value': 0},
            {'label': 'United', 'value': 1},
            {'label': 'US Airways', 'value': 2},
            {'label': 'American', 'value': 3},
            {'label': 'Southwest', 'value': 4},
            {'label': 'Delta', 'value': 5},
            {'label': 'Virgin America', 'value': 6},
    ],
    value=0,
    ),
)

grid.add_element(
    col=7,
    row=1,
    width=1,
    height=1,
    element=html.Button('save table', id='save-table-button'),
)

grid.add_element(
    col=7,
    row=2,
    width=1,
    height=1,
    element=html.P(id='save-table-textbox'),
)


@app.callback(Output('save-table-textbox', 'children'),
             [Input('save-table-button', 'n_clicks')],
             [State('table', 'rows'),
              State('table', 'selected_row_indices')]
              )
def save_current_table(savebutton, tablerows, selected_row_indices):

    table_df = pd.DataFrame(tablerows)

    if selected_row_indices:
        table_df = table_df.loc[selected_row_indices]

    if savebutton:
        filename = f'selection_{time.strftime("%Y%m%d-%H%M%S")}.csv'
        table_df.to_csv(filename)
        return f"Current selection saved to {filename}."  
  
  
@app.callback(
    Output('umap', 'figure'),
    [Input('model-select', 'value'),
     ])
def build_umap_graph(value):

    trace = go.Scattergl(
        x = cluster_data['umap_x'],
        y = cluster_data['umap_y'],
        
        text = cluster_data['tweet'],
        hoverinfo = 'text', 
        
        mode = 'markers',
        
        marker = dict(
            color = cluster_data['marker_color'],
            line = dict(
                width = 1,
                color = '#404040')
        )
    )

    traces = [trace]

    return {
        'data': traces,
        'layout': go.Layout(
            margin=dict(l=5,r=5,b=5,t=5),
            showlegend=False,
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
            ),
        ),
    }


table = dt.DataTable(
    # Initialise the rows
    rows=cluster_data[['prediction', 'tweet', 'airline']].head(10).to_dict('records'),
    row_selectable=True,
    #filterable=True,
    sortable=True,
    #max_rows_in_viewport=10,
    selected_row_indices=[],
    id='table',
)


grid.add_element(
    col=7,
    row=1,
    width=1,
    height=12,
    element=table,
)


@app.callback(
    Output('table', 'rows'),
    [Input('umap', 'selectedData'),
     ])
def build_table(selected_data):
   
    if selected_data is None:
        data = cluster_data[['prediction', 'tweet', 'airline']].head(10).copy()
    else:
        selected_indices = [p['pointIndex'] for p in selected_data['points']]
        data = cluster_data[['prediction', 'tweet', 'airline']].iloc[selected_indices].copy()
    
    return data.to_dict('records')
    

app.layout = html.Div(
    dui.Layout(
        grid=grid,
    ),
    style={
        'height': '100vh',
        'width': '100vw'
    }
)

#HTML("<a href='https://{}.{}'>URL</a>".format(os.environ['CDSW_ENGINE_ID'],os.environ['CDSW_DOMAIN']))

if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')
    #app.run_server(debug=True, host=os.environ['CDSW_IP_ADDRESS'], port=int(os.environ['CDSW_PUBLIC_PORT']))
