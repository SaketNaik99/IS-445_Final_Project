import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import requests

app = dash.Dash()


def yearwise_arrests(data):
    yearwise_stats_count = data.groupby('year_of_arrest')[['arrest_code']].count()
    yearwise_stats_count.reset_index(inplace=True)
    fig = px.line(yearwise_stats_count,
                  x="year_of_arrest", y="arrest_code",
                  title='Yearwise arrests trend',
                  labels={"year_of_arrest": "Year of Arrest", "arrest_code": "Number of Offenders"}
                  )
    return fig


def case_res(data):
    plot_df = data.groupby('arrest_res')[['arrest_code']].count()
    plot_df.reset_index(inplace=True)
    plot_data = data.merge(plot_df, left_on="arrest_res", right_on="arrest_res", suffixes=("_ungrouped", "_grouped"))
    fig = px.line(plot_data,
                  x="arrest_res", y="arrest_code_grouped",
                  title='Yearwise arrests trend',
                  labels={"year_of_arrest": "Year of Arrest", "arrest_code": "Number of Offenders"}
                  )
    return fig


# %%
def arrest_types(data):
    plot_df = data.groupby('arrest_type_descp')[['arrest_code']].count()
    plot_df.reset_index(inplace=True)
    plot_data = data.merge(plot_df, left_on="arrest_type_descp", right_on="arrest_type_descp",
                           suffixes=("_ungrouped", "_grouped"))
    fig = px.line(plot_data, x='arrest_type_descp', y='arrest_code_grouped',
                  animation_frame="year_of_arrest")
    return fig


def age_plot(df, clause):
    yearwise_ageofarrests = df.groupby(clause)[['age_at_arrest']].mean()
    yearwise_ageofarrests.reset_index(inplace=True)
    fig = px.line(yearwise_ageofarrests, x=clause, y="age_at_arrest")
    return fig


def monthly_arrests(data):
    num_arrests = data.groupby('month_of_arrest').size().reset_index(name="number_of_arrests")
    fig1 = px.bar(data_frame=num_arrests, x="month_of_arrest", y="number_of_arrests", barmode="group",
                  category_orders={"month_of_arrest": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]})
    return fig1


# Plotting 3 age groups by number of arrests
def cat2_arrests(data):
    bins = [0, 30, 50, 99]
    group_names = ['<=30', '30-50', '50-99']
    data['age_at_arrest_cat2'] = pd.cut(data['age_at_arrest'], bins, labels=group_names)
    age_group_cat2 = data.groupby(['age_at_arrest_cat2', 'month_of_arrest']).size().reset_index(
        name="number_of_arrests")
    fig3 = px.bar(data_frame=age_group_cat2, x="age_at_arrest_cat2", y="number_of_arrests", barmode="group",
                  title='Number of Arrests in each Age Group', animation_frame='month_of_arrest')
    return fig3


# Plotting juvenile/non-juvenile age groups by number of arrests
def cat1_arrests(data):
    bins = [0.0, 18.0, 99.0]
    group_names = ['juvenile', 'non-juvenile']
    data['age_at_arrest_cat'] = pd.cut(data['age_at_arrest'], bins, labels=group_names)
    age_group_juvenile = data.groupby(['age_at_arrest_cat', 'month_of_arrest']).size().reset_index(
        name="number_of_arrests")
    fig2 = px.bar(data_frame=age_group_juvenile, x="age_at_arrest_cat", y="number_of_arrests", barmode="group",
                  title='Number of Juvenile/Non-Juvenile Arrests', animation_frame='month_of_arrest')
    return fig2


def arrests_by_sex(data):
    data_plot = data.loc[data['arrestee_sex'].isin(['MALE', 'FEMALE'])]
    age_group_sex = data_plot.groupby(['arrestee_sex', 'month_of_arrest']).size().reset_index(name="number_of_arrests")
    fig4 = px.bar(data_frame=age_group_sex, x="arrestee_sex", y="number_of_arrests", barmode="group",
                  title='Number of Arrests by sex', animation_frame='month_of_arrest')
    return fig4


def arrests_by_race(data):
    data_plot = data.loc[~data['arrestee_race'].isin(['MALE', 'FEMALE'])]
    age_group_race = data_plot.groupby(['arrestee_race', 'month_of_arrest']).size().reset_index(
        name="number_of_arrests")
    fig5 = px.bar(data_frame=age_group_race, x="arrestee_race", y="number_of_arrests", barmode="group",
                  title='Number of Arrests by race', animation_frame='month_of_arrest')
    return fig5


def plot_fig3(data):
    data_3 = data.groupby(['arrest_type_descp', 'crime_code_desc'])['arrest_code'].count().to_frame('no_of_arrests').\
        reset_index()
    fig = px.bar(data_3, x="crime_code_desc", y="no_of_arrests", color = 'arrest_type_descp')
    return fig


def plot_fig2(data):
    data_2 = data.groupby(['crime_code_desc','arrest_res'])['arrest_code'].count().to_frame('no_of_arrests').\
        reset_index()
    fig = px.bar(data_2, x="crime_code_desc", y="no_of_arrests", color = 'arrest_res')
    return fig


def plot_fig1(data):
    data_1 = data.groupby(['crime_code_desc','age_group'])['arrest_code'].count().to_frame('no_of_arrests').\
        reset_index()
    fig = px.bar(data_1, x="crime_code_desc", y="no_of_arrests", color = 'age_group')
    return fig


def get_data():
    response = requests.get('https://data.urbanaillinois.us/resource/afbd-8beq.json?$limit=50000').json()
    arrest_code = []
    incident_number = []
    date_of_arrest = []
    year_of_arrest = []
    month_of_arrest = []
    arrest_type_descp = []
    crime_code = []
    crime_code_desc = []
    crime_category_code = []
    crime_category_desc = []
    violation = []
    disposition_code = []
    disposition_desc = []
    age_at_arrest = []
    arrestee_sex = []
    arrestee_race = []
    arrestee_emp_desc = []
    arrestee_residency_desc = []
    arrestee_home_zip = []
    arrestee_home_city = []
    arrestee_home_state = []
    arrest_res = []

    for i in response:
        arrest_code.append(i['arrest_code'])
        incident_number.append(i['incident_number'])
        date_of_arrest.append(i['date_of_arrest'])
        year_of_arrest.append(i['year_of_arrest'])
        month_of_arrest.append(i['month_of_arrest'])
        try:
            arrest_type_descp.append(i['arrest_type_description'])
        except:
            arrest_type_descp.append(None)
        crime_code.append(i['crime_code'])
        crime_code_desc.append(i['crime_code_description'])
        violation.append(i['violation'])
        disposition_code.append(i['disposition_code'])
        age_at_arrest.append(i['age_at_arrest'])
        try:
            arrestee_sex.append(i['arrestee_race'])
        except:
            arrestee_sex.append(None)
        try:
            arrestee_race.append(i['arrestee_sex'])
        except:
            arrestee_race.append(None)
        try:
            arrestee_emp_desc.append(i['arrestee_employment_description'])
        except:
            arrestee_emp_desc.append(None)
        try:
            arrestee_residency_desc.append(i['arrestee_residency_description'])
        except:
            arrestee_residency_desc.append(None)
        try:
            arrestee_home_zip.append(i['arrestee_home_zip'])
        except:
            arrestee_home_zip.append(None)
        try:
            arrestee_home_city.append(i['arrestee_home_city'])
        except:
            arrestee_home_city.append(None)
        try:
            arrestee_home_state.append(i['arrestee_home_state'])
        except:
            arrestee_home_state.append(None)
        arrest_res.append(i['arrest_resolution'])

        d = {'arrest_code': arrest_code, 'incident_number': incident_number, 'date_of_arrest': date_of_arrest,
             'year_of_arrest': year_of_arrest,
             'year_of_arrest': year_of_arrest, 'month_of_arrest': month_of_arrest,
             'arrest_type_descp': arrest_type_descp, 'crime_code': crime_code,
             'crime_code_desc': crime_code_desc, 'violation': violation, 'disposition_code': disposition_code,
             'age_at_arrest': age_at_arrest,
             'arrestee_sex': arrestee_sex, 'arrestee_race': arrestee_race, 'arrestee_emp_desc': arrestee_emp_desc,
             'arrestee_residency_desc': arrestee_residency_desc,
             'arrestee_home_zip': arrestee_home_zip, 'arrestee_home_city': arrestee_home_city,
             'arrestee_home_state': arrestee_home_state, 'arrest_res': arrest_res}
    data = pd.DataFrame(d)
    return data


def dash_layout():
    data = get_data()
    app.layout = html.Div(children=
    [
        html.Div
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=yearwise_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=case_res(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=arrest_types(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=age_plot(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=monthly_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=arrests_by_race(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=arrests_by_sex(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=cat1_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=cat2_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Crimes Commited by Different Age Groups', style={'textAlign': 'center',
                                                                                        'marginTop': 40,
                                                                                        'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=plot_fig1(), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H2', children='Punshiment for Crime Commited', style={'textAlign': 'center',
                                                                              'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=plot_fig2(), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Method of Arresting the Suspect', style={'textAlign': 'center',
                                                                                'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=plot_fig3(), style={'width': 1500, 'height': 1000})
        ])
    ]
    )


if __name__ == '__main__':
    app.run_server(debug=False)
