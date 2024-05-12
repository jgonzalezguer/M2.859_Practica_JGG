import numpy as np
import pandas as pd
import plotly.express as px  #https://plotly.com/python/line-and-scatter/
from dash import Dash, dcc, html, Input, Output



#df = pd.read_excel('owid-energy-data.xlsx')
df = pd.read_excel('https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.xlsx')
df["gdp per capita"]=df.gdp/df.population #creo nuevo atributo PIB per capita
df["gdp per capita"]=df["gdp per capita"].round(2)

df=df[~df.iso_code.isnull()]


countries=list(set(df.country))
countries_none=countries.copy()
countries_none.append('None')
atributos=list(df.columns)
atributos_num=[atributo for atributo in atributos if df[atributo].dtypes=="float64"]


#df_metadatos = pd.read_excel('owid-energy-data.xlsx',sheet_name=1)
df_metadatos = pd.read_excel('https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.xlsx',sheet_name=1)
df_metadatos

dict_unidades=dict()

for columna in atributos:
    if columna != 'gdp per capita':
        try: dict_unidades[columna]=df_metadatos[df_metadatos.column==columna].unit.values[0]
        except: dict_unidades[columna]=df_metadatos[df_metadatos.column==columna].unit.values
    else: dict_unidades[columna]='$/person'
dict_unidades



app2 = Dash(__name__)

app2.layout = html.Div([
    html.H1('Diagrama de dispersión',style={'textAlign':'center'}),
    html.P("Selecciona los distintos atributos a comparar y año. Si no aparecen puntos en el diagrama de dispersión es porque no existen datos para esos atributos y año concreto."),
    html.P("Atributo eje X:"),
    dcc.Dropdown(
        id="dropdown21",
        options=atributos_num,
        value='population',
        clearable=False, style={'color': '#002a77'}, placeholder="Atributo eje X"
    ),html.P("Atributo eje Y:"),
    dcc.Dropdown(
        id="dropdown22",
        options=atributos_num,
        value='gdp',
        clearable=False, style={'color': '#002a77'}, placeholder="Atributo eje Y"
    ),html.P("Atributo tamaño:"),
    dcc.Dropdown(
        id="dropdown23",
        options=atributos_num,
        value='gdp per capita',
        clearable=False, style={'color': '#002a77'}, placeholder="Atributo tamaño"
    ),html.P("Atributo color:"),
    dcc.Dropdown(
        id="dropdown24",
        options=atributos_num,
        value='electricity_demand',
        clearable=False, style={'color': '#002a77'}, placeholder="Atributo color"
    ),html.P("Año:"),
    dcc.Slider(df.year.min(), df.year.max(), step=1, value=2010, marks=None,id='my-slider2' ,
    tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Graph(id="graph2")
],style={'color': '#002a77'})


@app2.callback(
    Output("graph2", "figure"), Input("my-slider2", "value"),
    Input("dropdown21", "value"),Input("dropdown22", "value"),
    Input("dropdown23", "value"),Input("dropdown24", "value"))

def dispersion(year,atributo_x="population", atributo_y="gdp", atributo_tamaño="gdp per capita",
               atributo_color="electricity_demand"):
    df_year=df[df.year==year]
    df_year=df_year[np.logical_not(np.isnan(df_year[atributo_tamaño]))]
    df_year=df_year[df_year.country!="World"]
    fig2 = px.scatter(df_year,x=atributo_x,y=atributo_y,color=atributo_color,size=atributo_tamaño,hover_data=["country"],
                     labels={
                     atributo_x: f"{atributo_x} ({dict_unidades[atributo_x]})",
                     atributo_y: f"{atributo_y} ({dict_unidades[atributo_y]})",
                     atributo_color: f"{atributo_color} ({dict_unidades[atributo_color]})",
                     atributo_tamaño: f"{atributo_tamaño} ({dict_unidades[atributo_tamaño]})"}, width=1600,height=600)
    fig2.update_layout(plot_bgcolor="white")
    fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    return fig2




if __name__ == '__main__':  app2.run_server(debug=False)



# (host='127.0.0.1', port='7080', proxy=None,
                                    # debug=False, dev_tools_ui=None, dev_tools_props_check=None,
                                    # dev_tools_serve_dev_bundles=None, dev_tools_hot_reload=None,
                                    # dev_tools_hot_reload_interval=None, dev_tools_hot_reload_watch_interval=None,
                                    # dev_tools_hot_reload_max_retry=None, dev_tools_silence_routes_logging=None,
                                    # dev_tools_prune_errors=None)



