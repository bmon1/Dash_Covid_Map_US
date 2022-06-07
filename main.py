import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import date




app = Dash(__name__)


df = pd.read_csv("C:/Users/brand/PycharmProjects/dash_map/venv/all-states-history.csv")
df = df.groupby(['state', 'date', 'deathIncrease'])[['death']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Covid-19", style={'text-align': 'center'}),

    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2020, 2, 1),
        max_date_allowed=date(2021, 3, 7),
        initial_visible_month=date(2021, 3, 7),
        date=date(2021, 3, 7)
    ),
    html.Div(id='output-container-date-picker-single', ),


    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='covid_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='covid_map', component_property='figure')],
    [Input(component_id='my-date-picker-single', component_property='date')]
)


def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["date"] == option_slctd]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state',
        scope="usa",
        color='death',
        hover_data=['state', 'death', 'deathIncrease'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    '''#Plotly Graph Objects (GO)
    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states',
            locations=dff['state'],
            z=dff["death"].astype(float),
            colorscale='Reds',
        )]
    )'''

    fig.update_layout(
         title_text="Covid Numbers in the US",
         title_xanchor="center",
         title_font=dict(size=24),
         title_x=0.5,
         geo=dict(scope='usa'),
    )

    return container, fig



# ------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)