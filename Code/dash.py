import json
#import igraph as ig
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl
from dash.dependencies import Output, Input
from my_library import *

MAP_ID = "map"
MARKER_GROUP_ID = "marker-group"
COORDINATE_CLICK_ID = "coordinate-click-id"


import pandas as pd

url_grigio = "https://image.flaticon.com/icons/png/512/594/594840.png"
icon_grigio = {
    "iconUrl": url_grigio,
    "iconSize": [5, 5]  # size of the icon
}
url_blu = "https://image.flaticon.com/icons/png/512/1281/1281225.png"
icon_blu = {
    "iconUrl": url_blu,
    "iconSize": [5, 5]  # size of the icon
}
url_giallo = "https://image.flaticon.com/icons/png/512/1281/1281188.png"
icon_giallo = {
    "iconUrl": url_giallo,
    "iconSize": [5, 5]  # size of the icon
}
url_rosa = "https://image.flaticon.com/icons/png/512/480/480996.png"
icon_rosa = {
    "iconUrl": url_rosa,
    "iconSize": [5, 5]  # size of the icon
}

url_arancione = "https://cdn3.iconfinder.com/data/icons/softwaredemo/PNG/256x256/Circle_Orange.png"
icon_arancione = {
    "iconUrl": url_arancione,
    "iconSize": [5, 5]  # size of the icon
}
url_bianco = "https://cdn0.iconfinder.com/data/icons/shape-1/20/circle-512.png"
icon_bianco = {
    "iconUrl": url_bianco,
    "iconSize": [5, 5]  # size of the icon
}


icon3 = {
    "iconUrl": "https://image.flaticon.com/icons/png/512/1281/1281188.png",
    "iconSize": [4, 4]  # size of the icon
}
icon2 = {
    "iconUrl": "https://image.flaticon.com/icons/png/512/481/481037.png",
    "iconSize": [3, 3]  # size of the icon
}
url_rosso = "https://image.flaticon.com/icons/png/512/595/595005.png"
icon = {
    "iconUrl": url_rosso,
    "iconSize": [5, 5]  # size of the icon
}
g = read_graph(False, 'csv/stops.csv', 'data/edges_station_completo.csv', 'data/names.csv')
g_train = read_graph(True, 'csv/stops.csv', 'dataV2/edges.csv', 'dataV2/nodes.csv')


def get_nodes(g, vertex_del, first):
    markers = []
    for vertex in g.vs:
        if vertex['stop_id'] == first:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon3,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
        elif vertex['stop_id'] in vertex_del:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon2,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id = str(vertex['stop_id'])
                )
            )
        else:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
    cluster = dl.LayerGroup(id="markers", children=markers)
    return cluster

def get_line(g, vertex_del):

    lines = []
    for el in g.es:
        helptuple = el.tuple
        source = helptuple[0]
        target = helptuple[1]

        lat_source = g.vs(source)[0]['stop_lat']
        long_source = g.vs(source)[0]['stop_lon']

        lat_target = g.vs(target)[0]['stop_lat']
        long_target = g.vs(target)[0]['stop_lon']

        if vertex_del == [] or (g.vs(source)[0]['stop_id'] not in vertex_del and g.vs(target)[0]['stop_id'] not in vertex_del):
            lines.append(
                dl.Polyline(
                    positions = [[lat_source, long_source], [lat_target, long_target]], weight=1.5, dashArray='0'))
        else:
            lines.append(
                dl.Polyline(
                    positions=[[lat_source, long_source], [lat_target, long_target]], weight=0.1, dashArray='3'))

    cluster = dl.LayerGroup(id="lines", children=lines)
    return cluster


#keys = ["watercolor", "toner", "terrain"]
keys = ["watercolor", "terrain"]
url_template = "http://{{s}}.tile.stamen.com/{}/{{z}}/{{x}}/{{y}}.png"
attribution = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' \
              '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data ' \
              '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

def create_map_train(g):
    df = node_load(g)
    #print(df['load'])
    df.sort_values(by=["load"], ascending=True, inplace=True)
    low = df.head(100)
    high = df.tail(100)
    #print(low)
    #print(high)
    vertex_h = high['id'].tolist()
    vertex_l = low['id'].tolist()

    return dl.Map(style={'width': '700px', 'height': '500px'},
           center=[45.415604, 9.401200],
           zoom=8,
           children=[
               # https://manage.thunderforest.com/dashboard - userei la prima commentata
               # dl.TileLayer(url="https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),


               dl.LayersControl(
                   [dl.BaseLayer(dl.TileLayer(url=url_template.format(key), attribution=attribution),
                                 name=key, checked=key == "toner") for key in keys] +
                   [dl.BaseLayer(dl.TileLayer(url="https://unpkg.com/elm-pep"), name='gray')]
                   )
               ,
               # dl.TileLayer(url="https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),
               # dl.TileLayer(url="http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"),
               # dl.Marker(position=[45.4654219, 9.1859243], children=[dl.Tooltip('MIlan')]),

               get_nodes_train(g, vertex_h, vertex_l),
               #get_line(g, vertex_del),
               dl.LayerGroup(id=MARKER_GROUP_ID)
           ], id='map_train')

def get_nodes_train(g, vertex_h, vertex_l):
    markers = []
    for vertex in g.vs:
        if vertex['stop_id'] in vertex_h:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_blu,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id = str(vertex['stop_id'])
                )
            )
        elif vertex['stop_id'] in vertex_l:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_giallo,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
        else:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_grigio,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
    cluster = dl.LayerGroup(id="markers", children=markers)
    return cluster

def get_nodes_centrality(g, v_1, v_2, v_3, v_4, v_5):
    markers = []
    for vertex in g.vs:
        if vertex['stop_id'] in v_1:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id = str(vertex['stop_id'])
                )
            )
        elif vertex['stop_id'] in v_2:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_rosa,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
        elif vertex['stop_id'] in v_3:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_arancione,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
        elif vertex['stop_id'] in v_4:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_giallo,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
        elif vertex['stop_id'] in v_5:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_bianco,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
        else:
            markers.append(
                dl.Marker(
                    title=vertex['stop_name'],
                    position=(vertex['stop_lat'], vertex['stop_lon']),
                    icon=icon_grigio,
                    children=[
                        dl.Tooltip(vertex['stop_name']),
                        dl.Popup(vertex['stop_name']),
                    ],
                    id=str(vertex['stop_id'])
                )
            )
    cluster = dl.LayerGroup(id="markers", children=markers)
    return cluster

def create_map(g, vertex_del, first):

    return dl.Map(style={'width': '700px', 'height': '500px'},
           center=[45.415604, 9.401200],
           zoom=8,
           children=[
               # https://manage.thunderforest.com/dashboard - userei la prima commentata
               # dl.TileLayer(url="https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),

               dl.LayersControl(
                   [dl.BaseLayer(dl.TileLayer(url=url_template.format(key), attribution=attribution),
                                 name=key, checked=key == "toner") for key in keys] +
                   [dl.BaseLayer(dl.TileLayer(url="https://unpkg.com/elm-pep"), name='gray')]
                   )
               ,
               # dl.TileLayer(url="https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),
               # dl.TileLayer(url="http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"),
               # dl.Marker(position=[45.4654219, 9.1859243], children=[dl.Tooltip('MIlan')]),
               get_nodes(g, vertex_del, first),
               get_line(g, vertex_del),
               dl.LayerGroup(id=MARKER_GROUP_ID)
           ], id=MAP_ID)

def create_map_degree(g):
    v_1 = []
    v_2 = []
    v_3 = []
    v_4 = []
    v_5 = []

    for v in g.vs:
        if v['degree_all'] == 5:
            v_1.append(v['stop_id'])
        elif v['degree_all'] == 4:
            v_2.append(v['stop_id'])
        elif v['degree_all'] == 3:
            v_3.append(v['stop_id'])
        elif v['degree_all'] == 2:
            v_4.append(v['stop_id'])
        elif v['degree_all'] == 1:
            v_5.append(v['stop_id'])

    return dl.Map(style={'width': '700px', 'height': '500px'},
           center=[45.415604, 9.401200],
           zoom=8,
           children=[
               # https://manage.thunderforest.com/dashboard - userei la prima commentata
               # dl.TileLayer(url="https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),

               dl.LayersControl(
                   [dl.BaseLayer(dl.TileLayer(url=url_template.format(key), attribution=attribution),
                                 name=key, checked=key == "toner") for key in keys] +
                   [dl.BaseLayer(dl.TileLayer(url="https://unpkg.com/elm-pep"), name='gray')]
                   )
               ,
               # dl.TileLayer(url="https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),
               # dl.TileLayer(url="http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"),
               # dl.Marker(position=[45.4654219, 9.1859243], children=[dl.Tooltip('MIlan')]),
               get_nodes_centrality(g, v_1, v_2, v_3, v_4, v_5 ),
               get_line(g, []),
               dl.LayerGroup(id=MARKER_GROUP_ID)
           ], id=MAP_ID)

def create_map_betweenness(g):
    v_1 = []
    v_2 = []
    v_3 = []
    v_4 = []
    v_5 = []

    for v in g.vs:
        if v['betweenness'] > 0.1*2:
            print(v)
            v_1.append(v['stop_id'])
        elif v['betweenness'] > 0.05*2:
            v_2.append(v['stop_id'])
        elif v['betweenness'] > 0.02*2:
            v_3.append(v['stop_id'])
        elif v['betweenness'] > 0:
            v_4.append(v['stop_id'])
        else:
            v_5.append(v['stop_id'])


    return dl.Map(style={'width': '700px', 'height': '500px'},
           center=[45.415604, 9.401200],
           zoom=8,
           children=[
               # https://manage.thunderforest.com/dashboard - userei la prima commentata
               # dl.TileLayer(url="https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),

               dl.LayersControl(
                   [dl.BaseLayer(dl.TileLayer(url=url_template.format(key), attribution=attribution),
                                 name=key, checked=key == "toner") for key in keys] +
                   [dl.BaseLayer(dl.TileLayer(url="https://unpkg.com/elm-pep"), name='gray')]
                   )
               ,
               # dl.TileLayer(url="https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=7f0fbd00049e4efd95b34ac1aafdeb34"),
               # dl.TileLayer(url="http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga"),
               # dl.Marker(position=[45.4654219, 9.1859243], children=[dl.Tooltip('MIlan')]),
               get_nodes_centrality(g, v_1, v_2, v_3, v_4, v_5 ),
               get_line(g, []),
               dl.LayerGroup(id=MARKER_GROUP_ID)
           ], id=MAP_ID)

# Create app.
app = dash.Dash(__name__, external_scripts=['https://codepen.io/chriddyp/pen/bWLwgP.css'],suppress_callback_exceptions=True)
app.layout = html.Div(children=[html.H2('Trenord Transport Network', style={'text-align': 'center'}),
    dcc.Tabs(id="tabs-example", value='tab-1-example', style={'margin-bottom': '10px'}, children=[
        dcc.Tab(label='Station Network', value='tab-1-example'),
        dcc.Tab(label='Train Network', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')], style = {'font-family': 'Calibri'})



@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([html.Div(children=[
            html.Div(id='div_map', children=[
                create_map(g, [], None),
            ],  style={
                        "padding-right": "15px"
                    }),
        html.Div([
            html.Div([html.H4('Attack Strategies', style={'text-align': 'center', 'margin-top': 'auto',
                                'margin-bottom': '7px'}),
            html.Div([

            html.Div(html.Button('Original', id='original', style={'width': '150px', 'height': '50px'}),
                style={
                    "padding-bottom": "15px",
                    "padding-right": "15px",
                }),

            html.Div(html.Button('Cascading Failure Betweenness', id='cascading-fail', style={'width': '150px', 'height': '50px'}),
                style={
                    "padding-bottom": "15px",
                    "padding-right": "15px",
                }),
            html.Div(html.Button('Cascading Failure Random', id='random_cascading', style={'width': '150px', 'height': '50px'}),
                         style={
                             "padding-bottom": "15px",
                             "padding-right": "15px",
                         })
            ], style={
                    "display": "inline-flex",
                    'margin-bottom':'35px'
                }),

            html.Div([
                html.Div(html.Button('Targeted Attack (Degree)', id='targeted_degree', style={'width': '150px', 'height': '50px'}),
                style={
                    "padding-bottom": "15px",
                    "padding-right": "15px",
                }),
            html.Div(html.Button('Targeted Attack (Betweenness)', id='targeted_bet', style={'width': '150px', 'height': '50px'}),
                style={
                    "padding-bottom": "15px",
                    "padding-right": "15px",
                }),
            html.Div(html.Button('Random Attack', id='random', style={'width': '150px', 'height': '50px'}),
                )], style={
                    "display": "inline-flex"
                }
            ),dcc.Slider(
                id='slider',
                min=1,
                max=int(g.vcount()/4*3),
                value=8,
                marks={str(i): str(i) for i in range(int(g.vcount()/4*3)) if i%20==0},
                step=1
            ),html.Div([html.P('Calculate Graphs:   '),
                dcc.RadioItems(

                        id='radio',
                        options=[{'label': i, 'value': i} for i in ['Yes', 'No']],
                        value='No',
                        labelStyle={'display': 'inline-block'}
                )],style={
                    "display": "inline-flex",
                    'align-items':'center'}
                )], style={
                    "display": "inline-flex",
                    'flex-direction': 'column',
                    'height': '270px',
                    'border': '1px solid ',
                    'border-radius': '6px',
                    'border-color' : 'gray',
                    'padding' : '10px',
                    'margin-bottom': '30px'
                }),
        html.Div([
        html.Div([html.H4('Centrality Measures', style={'text-align': 'center', 'margin-top': 'auto',
                                'margin-bottom': '7px'}),

            html.Div([
                        html.Div(html.Button('Degree', id='degree_centrality', style={'width': '150px', 'height': '50px'}),
                style={
                    "padding-bottom": "15px",
                    "padding-right": "15px",
                }),

             html.Div(html.Button('Betweenness', id='betweenness_centrality', style={'width': '150px', 'height': '50px'}),
                style={
                    "padding-bottom": "15px",
                    "padding-right": "15px",
                }),
                html.P('- ', style={'margin':'3px'}),
                html.Div([html.Img(src=url_bianco, width='10px', style={'margin':'3px'}),
                      html.Img(src=url_giallo, width='10px', style={'margin':'3px'}),
                      html.Img(src=url_arancione, width='10px', style={'margin':'3px'}),
                     html.Img(src=url_rosa, width='10px', style={'margin':'3px'}),
                      html.Img(src=url_rosso, width='10px', style={'margin':'3px'})], style={'margin-top':'6px'}),
                html.P(' +', style={'margin':'3px'}),
            ], style={
                    "display": "inline-flex",
                    'margin-bottom':'35px'
                }),

            ], style={
                    "display": "inline-flex",
                    'flex-direction': 'column',
                    'height': '80px',
                    'border': '1px solid ',
                    'border-radius': '6px',
                    'border-color' : 'gray',
                    'padding' : '10px'
                })])
                ], style={
                    "display": "inline-flex",
                    'flex-direction': 'column',
                    'width': '50%',
                })

    ], style={
                "display": "inline-flex"
            }),


    html.Div([
        html.Div([dcc.Graph(
            id='e',
            figure = {'data': [{'y': [], 'type': 'line', 'name': 'E'}],
            'layout': {
                'title': 'Efficiency'
            }}
        )], style = {'width': '600px'}),
        html.Div([dcc.Graph(
            id='s',
            figure = {'data': [{'y': [], 'type': 'line', 'name': 'S'}],
            'layout': {
                'title': 'Large Component Size'
            }}
        )], style = {'width': '600px'})],
        style={
                "display": "inline-flex"
            })], style = {'font-family': 'Calibri'})
    elif tab == 'tab-2-example':
        return html.Div([html.Div(id='div_map_train', children=[
                create_map_train(g_train)]),

                html.Div([html.H4('Trains Load ', style={'text-align': 'center', 'margin-top': 'auto',
                                                              'margin-bottom': '7px'}),
                          html.Div([
                              html.Div(
                                  html.Button('All', id='all', style={'width': '150px', 'height': '50px'}),
                                  style={
                                      "padding-bottom": "15px",
                                      "padding-right": "15px",
                                  }),
                              html.Div(
                                  html.Button('Before 9:59', id='9', style={'width': '150px', 'height': '50px'}),
                                  style={
                                      "padding-bottom": "15px",
                                      "padding-right": "15px",
                                  }),

                              html.Div(html.Button('10:00 - 12:59', id='10',
                                                   style={'width': '150px', 'height': '50px'}),
                                       style={
                                           "padding-bottom": "15px",
                                           "padding-right": "15px",
                                       }),
                              html.Div(html.Button('13:00 - 16:59', id='13',
                                                   style={'width': '150px', 'height': '50px'}),
                                       style={
                                           "padding-bottom": "15px",
                                           "padding-right": "15px",
                                       }),
                              html.Div(html.Button('17:00 - 19:59', id='17',
                                                   style={'width': '150px', 'height': '50px'}),
                                       style={
                                           "padding-bottom": "15px",
                                           "padding-right": "15px",
                                       }),
                              html.Div(html.Button('After 20:00', id='20',
                                                   style={'width': '150px', 'height': '50px'}),
                                       style={
                                           "padding-bottom": "15px",
                                           "padding-right": "15px",
                                       }),
                              html.Div(children = [ html.P('- ', style={'margin':'3px'}),
                                       html.Div([html.Img(src=url_giallo, width='10px', style={'margin':'3px'}),
                                       html.Img(src=url_grigio, width='10px', style={'margin':'3px'}),
                                       html.Img(src=url_blu, width='10px', style={'margin':'3px'})], style={'margin-top':'5px'}
                                      ),
                                        html.P(' +', style={'margin':'3px'})], style={'display':'flex', 'justify-content': 'center'})
                          ], style={
                              "display": "inline-flex",
                              'flex-direction': 'column',
                              'margin-bottom': '35px'
                          })



            ],  style={
                        "padding-right": "15px",
                        'flex-direction': 'column',
                        'height': '440px',
                        'width':'151px',
                        'border': '1px solid ',
                        'border-radius': '6px',
                        'border-color': 'gray',
                        'padding': '10px',
                        'margin-left': '10px'

                    })
            ], style={
                              "display": "inline-flex",
                          })



@app.callback(
        Output('div_map_train', 'children'),
        [Input('all', 'n_clicks'),
         Input('9', 'n_clicks'),
         Input('10', 'n_clicks'),
         Input('13', 'n_clicks'),
         Input('17', 'n_clicks'),
         Input('20', 'n_clicks'),
         ])
def update_map_train(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'all' in changed_id:
        print('all train load')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/edges.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)
    elif '9' in changed_id:
        print('1')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/fasce/edges_first.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)
    elif '10' in changed_id:
        print('10')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/fasce/edges_second.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)
    elif '13' in changed_id:
        print('13')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/fasce/edges_third.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)
    elif '17' in changed_id:
        print('17')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/fasce/edges_fourth.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)
    elif '20' in changed_id:
        print('20')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/fasce/edges_fifth.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)
    else:
        print('all train load')
        g2 = read_graph(True, 'csv/stops.csv', 'dataV2/edges.csv', 'dataV2/nodes.csv')
        return create_map_train(g2)




@app.callback(
        [Output('div_map', 'children'),
         Output('e', 'figure'),
         Output('s', 'figure')],
        [Input('cascading-fail', 'n_clicks'),
         Input('random_cascading', 'n_clicks'),
         Input('original', 'n_clicks'),
         Input('random', 'n_clicks'),
         Input('targeted_degree', 'n_clicks'),
         Input('targeted_bet', 'n_clicks'),
         Input('betweenness_centrality', 'n_clicks'),
         Input('degree_centrality', 'n_clicks'),
         Input('slider', 'value'),
         Input('radio', 'value')])
def update_map(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, n, radio):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'cascading-fail' in changed_id:
        print('cascade fail')
        g_fail = g.copy()
        if radio == 'Yes':
            [g_fail, vertex_del, Er, Sr] = failure_cascade(g_fail, True)
        else:
            [g_fail, vertex_del, Er, Sr] = failure_cascade(g_fail, False)
        print(vertex_del)

        figure_e = {
            'data': [
                {'y': Er, 'type': 'line', 'name': 'E'},
            ],
            'layout': {
                'title': 'Cascading Failure Efficiency'
            }
        }

        figure_s = {
            'data': [
                {'y': Sr, 'type': 'line', 'name': 'S'},
            ],
            'layout': {
                'title': 'Cascading Failure Large Connected Component'
            }
        }
        return create_map(g, vertex_del, vertex_del[0]), figure_e, figure_s
    elif 'random_cascading' in changed_id:
        print('cascading-fail-ran')
        g_fail = g.copy()
        if radio == 'Yes':
            [g_fail, vertex_del, Er, Sr] = failure_cascade_random(g_fail, True)
        else:
            [g_fail, vertex_del, Er, Sr] = failure_cascade_random(g_fail, False)
        print(vertex_del)

        figure_e = {
            'data': [
                {'y': Er, 'type': 'line', 'name': 'E'},
            ],
            'layout': {
                'title': 'Cascading Failure Random Efficiency'
            }
        }

        figure_s = {
            'data': [
                {'y': Sr, 'type': 'line', 'name': 'S'},
            ],
            'layout': {
                'title': 'Cascading Failure Random Large Connected Component'
            }
        }
        return create_map(g, vertex_del, vertex_del[0]), figure_e, figure_s
    elif 'random' in changed_id:
        print('random')
        g_att_r = g.copy()
        #n = g.vcount() / 100 * 2
        print(n)
        if radio == 'Yes':
            [g_att_r, vertex_del, Er, Sr] = random_attack(g_att_r, n, True)
        else:
            [g_att_r, vertex_del, Er, Sr] = random_attack(g_att_r, n, False)
        figure_e = {
            'data': [
                {'y': Er, 'type': 'line', 'name': 'E'},
            ],
            'layout': {
                'title': 'Random Attack Efficiency'
            }
        }

        figure_s = {
            'data': [
                {'y': Sr, 'type': 'line', 'name': 'S'},
            ],
            'layout': {
                'title': 'Random Attack Large Connected Component'
            }
        }

        return create_map(g, vertex_del, None), figure_e, figure_s
    elif 'targeted_degree' in changed_id:
        print('targeted_degree')
        g.vs['degree_all'] = calcolate_degree(g, 'all')
        g_att_t = g.copy()
        #n = g.vcount() / 100 * 2
        print(n)
        if radio == 'Yes':
            [g_att_t, vertex_del, Er, Sr] = target_attack_degree(g_att_t, n, True)
        else:
            [g_att_t, vertex_del, Er, Sr] = target_attack_degree(g_att_t, n, False)
        print(vertex_del)

        figure_e = {
            'data': [
                {'y': Er, 'type': 'line', 'name': 'E'},
            ],
            'layout': {
                'title': 'Target Attack (Degree) Efficiency'
            }
        }

        figure_s = {
            'data': [
                {'y': Sr, 'type': 'line', 'name': 'S'},
            ],
            'layout': {
                'title': 'Target Attack (Degree) Large Connected Component'
            }
        }
        return create_map(g, vertex_del, None), figure_e, figure_s
    elif 'targeted_bet' in changed_id:
        print('targeted_bet')
        g.vs['betweenness'] = calcolate_betweenness(g, False, None)
        g_att_bet = g.copy()
        #n = g.vcount() / 100 * 2
        print(n)
        if radio == 'Yes':
            [g_att_bet, vertex_del, Er, Sr] = target_attack_betweenness(g_att_bet, n, True)
        else:
            [g_att_bet, vertex_del, Er, Sr] = target_attack_betweenness(g_att_bet, n, False)
        figure_e = {
            'data': [
                {'y': Er, 'type': 'line', 'name': 'E'},
            ],
            'layout': {
                'title': 'Target Attack (Betweenness) Efficiency'
            }
        }

        figure_s = {
            'data': [
                {'y': Sr, 'type': 'line', 'name': 'S'},
            ],
            'layout': {
                'title': 'Target Attack (Betweenness) Large Connected Component'
            }
        }
        return create_map(g, vertex_del, None), figure_e, figure_s
    elif 'original' in changed_id:
        print('originals')
        figure_e = {'data': [{'y': [], 'type': 'line', 'name': 'E'}],
                  'layout': {
                      'title': 'Efficiency'
                  }}
        figure_s = {'data': [{'y': [], 'type': 'line', 'name': 'S'}],
                    'layout': {
                        'title': 'Large Connected Component'
                    }}
        return create_map(g, [], None), figure_e, figure_s
    elif 'degree_centrality' in changed_id:
        print('Degree')
        g.vs['degree_all'] = calcolate_degree(g, 'all')
        return create_map_degree(g), {}, {}
    elif 'betweenness_centrality' in changed_id:
        print('betweenness')
        g.vs['betweenness'] = calcolate_betweenness(g, False, None)
        return create_map_betweenness(g), {}, {}

    else:
        figure_e = {'data': [{'y': [], 'type': 'line', 'name': 'E'}],
                  'layout': {
                      'title': 'Efficiency'
                  }}
        figure_s = {'data': [{'y': [], 'type': 'line', 'name': 'S'}],
                  'layout': {
                      'title': 'Large Connected Component'
                  }}
        return create_map(g, [], None), figure_e, figure_s


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, use_reloader=False)