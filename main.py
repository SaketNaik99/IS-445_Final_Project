import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import requests

app = dash.Dash()


def yearwise_arrests(data):
    """
    This function creates a plot of arrests made over the years
    :param data:
    :return:
    """
    yearwise_stats_count = data.groupby('year_of_arrest')[['arrest_code']].count()
    yearwise_stats_count.reset_index(inplace=True)
    fig = px.line(yearwise_stats_count,
                  x="year_of_arrest", y="arrest_code",
                  title='Yearwise arrests trend',
                  labels={"year_of_arrest": "Year of Arrest", "arrest_code": "Number of Offenders"}
                  )
    return fig


def case_res(data):
    """
    This function creates a plot of different arrest resolutions over the years
    :param data:
    :return:
    """
    plot_df = data.groupby('arrest_res')[['arrest_code']].count()
    plot_df.reset_index(inplace=True)
    plot_data = data.merge(plot_df, left_on="arrest_res", right_on="arrest_res", suffixes=("_ungrouped", "_grouped"))
    fig = px.line(plot_data,
                  x="arrest_res", y="arrest_code_grouped",
                  title='Yearwise arrests trend',
                  labels={"arrest_res": "Arrest Resolution", "arrest_code": "Number of Offenders"}
                  )
    return fig


# %%
def arrest_types(data):
    """
    This fucntion creates a plot of number of offenders of each arrest type descriptions over the years
    :param data:
    :return:
    """
    plot_df = data.groupby('arrest_type_descp')[['arrest_code']].count()
    plot_df.reset_index(inplace=True)
    plot_data = data.merge(plot_df, left_on="arrest_type_descp", right_on="arrest_type_descp",
                           suffixes=("_ungrouped", "_grouped"))
    fig = px.line(plot_data, x='arrest_type_descp', y='arrest_code_grouped',
                  animation_frame="year_of_arrest")
    return fig


def age_plot(data, clause):
  """Plotting monthly average age at arrest"""
  data['age_at_arrest'] = data['age_at_arrest'].astype(float)
  yearwise_ageofarrests = data.groupby('year_of_arrest')['age_at_arrest'].mean().reset_index(name = 'Average Arrest Age')
  fig = px.line(yearwise_ageofarrests, x='year_of_arrest', y='Average Arrest Age', title = 'Average Age at Arrest by Month')
  return fig


def monthly_arrests(data):
  """Plotting the monthly arrests by grouping by month and taking the count of arrests"""
  num_arrests = data.groupby('month_of_arrest').size().reset_index(name="number_of_arrests")
  fig = px.bar(data_frame=num_arrests, x="month_of_arrest", y="number_of_arrests", barmode="group",
                category_orders={"month_of_arrest": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]})
  return fig

def cat1_arrests(data):
  """Plotting the number of arrests by binning age into 2 categories"""
  bins = [0.0, 18.0, 99.0]
  group_names = ['juvenile', 'non-juvenile']
  data['age_at_arrest_cat'] = pd.cut(data['age_at_arrest'].astype(float), bins, labels=group_names)
  age_group_juvenile = data.groupby(['age_at_arrest_cat', 'month_of_arrest']).size().reset_index(name="number_of_arrests")
  fig = px.bar(data_frame=age_group_juvenile, x="age_at_arrest_cat", y="number_of_arrests", barmode="group", 
                title = 'Number of Juvenile/Non-Juvenile Arrests', animation_frame = 'month_of_arrest')
  return fig

def cat2_arrests(data):
  """Plotting the number of arrests by binning age into 3 categories"""
  data['age_at_arrest'] = data['age_at_arrest'].astype('float')
  bins = [0, 30, 50, 99]
  group_names = ['<=30', '30-50', '50-99']
  data['age_at_arrest_cat2'] = pd.cut(data['age_at_arrest'], bins, labels=group_names)
  age_group_cat2 = data.groupby(['age_at_arrest_cat2', 'month_of_arrest']).size().reset_index(
      name="number_of_arrests")
  fig = px.bar(data_frame=age_group_cat2, x="age_at_arrest_cat2", y="number_of_arrests", barmode="group",
                title='Number of Arrests in each Age Group', animation_frame='month_of_arrest')
  return fig


def arrests_by_sex(data):
  """Plotting the number of arrests by sex"""
  data_plot = data.loc[data['arrestee_sex'].isin(['MALE', 'FEMALE'])]
  age_group_sex = data_plot.groupby(['arrestee_sex', 'month_of_arrest']).size().reset_index(name="number_of_arrests")
  fig = px.bar(data_frame=age_group_sex, x="arrestee_sex", y="number_of_arrests", barmode="group",
                title='Number of Arrests by sex', animation_frame='month_of_arrest')
  return fig


def arrests_by_race(data):
  """Plotting the number of arrests by race"""
  data_plot = data.loc[~data['arrestee_race'].isin(['MALE', 'FEMALE'])]
  age_group_race = data_plot.groupby(['arrestee_race', 'month_of_arrest']).size().reset_index(
      name="number_of_arrests")
  fig = px.bar(data_frame=age_group_race, x="arrestee_race", y="number_of_arrests", barmode="group",
                title='Number of Arrests by race', animation_frame='month_of_arrest')
  return fig


def plot_fig3(data):
    data_3 = data.groupby(['arrest_type_descp', 'crime_code_desc'])['arrest_code'].count().to_frame('no_of_arrests'). \
        reset_index()
    fig = px.bar(data_3, x="crime_code_desc", y="no_of_arrests", color='arrest_type_descp')
    return fig


def plot_fig2(data):
    data_2 = data.groupby(['crime_code_desc', 'arrest_res'])['arrest_code'].count().to_frame('no_of_arrests'). \
        reset_index()
    fig = px.bar(data_2, x="crime_code_desc", y="no_of_arrests", color='arrest_res')
    return fig


def plot_fig1(data):
    data['year_of_arrest'] = pd.to_numeric(data['year_of_arrest'])
    data['month_of_arrest'] = pd.to_numeric(data['month_of_arrest'])
    data ['age_group'] = pd.cut(x = data['age_at_arrest'], bins=[0,17, 55, 99],
                     labels=['Minor', 'Adult',
                             'Elderly'])
    data['age_at_arrest'] = pd.to_numeric(data['age_at_arrest'])
    data_1 = data.groupby(['crime_code_desc', 'age_group'])['arrest_code'].count().to_frame('no_of_arrests').reset_index()
    fig = px.bar(data_1, x="crime_code_desc", y="no_of_arrests", color='age_group')
    return fig


def get_data():
    """

    :return:
    """
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


def city_sex(data):
  data['year_of_arrest'] = data['year_of_arrest'].astype('int32')
  data['month_of_arrest'] = pd.to_datetime(data['month_of_arrest'], format='%m')
  data['date_of_arrest'] = pd.to_datetime(data['date_of_arrest'])
  data_only_sex = data[(data['arrestee_sex'] == 'MALE') | (data['arrestee_sex'] == 'FEMALE')]
  fig = px.histogram(data_only_sex, x = data_only_sex['arrestee_home_city'],
                     y = data_only_sex['arrestee_home_city'].index,
                     color = data_only_sex['arrestee_sex'],
                     animation_frame=data_only_sex['year_of_arrest'],
                     log_y = True,
                     title = 'Relationship Between Offender Home City and Sex',
                     labels = {'arrestee_home_city' : 'Offender Home City'})
  return fig


def city_age(data):
  data_age = data.dropna()
  data_age['age_at_arrest'] = data_age['age_at_arrest'].astype(float)
  bins= [0,13,20,50,110]
  labels = ['Kid','Teen','Adult','Elder']
  data_age['AgeGroup'] = pd.cut(data_age['age_at_arrest'], bins=bins, labels=labels, right=False)
  fig = px.histogram(data_age, x = data_age['arrestee_home_city'],
                     y = data_age['arrestee_home_city'].index,
                     color = data_age['AgeGroup'],
                     animation_frame=data_age['year_of_arrest'],
                     log_y = True,
                     title = 'Relationship Between Offender Home City and Age',
                     labels = {'arrestee_home_city' : 'Offender Home City'})
  return fig


def city_crime_type(data):
  fig = px.histogram(data, x = data['arrestee_home_city'],
                     y = data['arrestee_home_city'].index,
                     color = data['crime_code_desc'],
                     animation_frame=data['year_of_arrest'],
                     log_y = True,
                     title = 'Relationship Between Offender Home City and Crime Types',
                     labels = {'arrestee_home_city' : 'Offender Home City',
                               'arrestee_race' : 'Offender Race'})
  return fig


def city_race(data):
    fig = px.histogram(data, x = data['arrestee_home_city'],
                     y = data['arrestee_home_city'].index,
                     color = data['arrestee_race'],
                     animation_frame=data['year_of_arrest'],
                     log_y = True,
                     title = 'Relationship Between Offender Home City and Race',
                     labels = {'arrestee_home_city' : 'Offender Home City',})
    return fig


def preprocess(dataframe):
    df1 = dataframe.copy()
    df1['age_at_arrest'] = df1['age_at_arrest'].astype(float)

    # convert year to datetime and drop month
    df1['year_of_arrest'] = pd.to_datetime(df1['year_of_arrest'], format='%Y')
    df1.drop(columns='month_of_arrest', inplace=True)

    # Creating Age Category Column
    bins = [0, 18, 24, 34, 54, 74, 84, 100]
    labels = ['0 to 18', '18 to 24', '24 to 34', '34 to 54', '54 to 74', '74 to 84', "84 to 100"]
    df1['Arreste Age Category'] = pd.cut(df1['age_at_arrest'], bins=bins, labels=labels, right=False)

    return df1


def age_crimetype(dataframe):
    import plotly.graph_objects as go

    age_crimetype_df = dataframe[["age_at_arrest", "crime_code_desc", "arrestee_sex"]]
    age_crimetype_df = pd.DataFrame(age_crimetype_df.groupby("crime_code_desc")["age_at_arrest"].mean())
    age_crimetype_df.reset_index(inplace=True)
    age_crimetype_df = age_crimetype_df[age_crimetype_df["crime_code_desc"] != "."]
    age_crimetype_df.sort_values(by="age_at_arrest", ascending=True, inplace=True)
    age_crimetype_df["age_at_arrest"] = age_crimetype_df["age_at_arrest"].astype("int")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=age_crimetype_df["crime_code_desc"],
        x=age_crimetype_df["age_at_arrest"],
        name='Age at Arrest',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        )
    ))

    fig.update_layout(
        title_text="Crime Type VS Mean Age at Arrest",
        uniformtext=dict(mode="hide", minsize=10),
        xaxis_title="Mean Age at Arrest",
        yaxis_title="Crime Type ")

    fig.update_layout(barmode='stack')
    return fig


def age_crimecount(dataframe):
    age_minor_df = pd.DataFrame(dataframe.groupby("Arreste Age Category")["Arreste Age Category"].count())
    age_minor_df.rename(columns={"Arreste Age Category": "Count"}, inplace=True)
    age_minor_df.reset_index(inplace=True)

    fig = px.bar(age_minor_df, x="Arreste Age Category", y="Count",
                 title="Number of Arrest made for different age category")
    return fig


def age_resolution(dataframe):
    age_resolution_df = pd.DataFrame(
        dataframe.groupby(["arrest_res", "Arreste Age Category"])["Arreste Age Category"].count())
    age_resolution_df.rename(columns={"Arreste Age Category": "Count"}, inplace=True)
    age_resolution_df.reset_index(inplace=True)

    fig = px.bar(age_resolution_df, x='arrest_res', y='Count',
                 color='Arreste Age Category',
                 labels={'Count': 'Number of People Arrested', 'arrest_res': 'Resolution at Arrest'}, height=1000,
                 title="Count of People arrested vs Arrest Resolution")

    return fig


def dash_layout():
    data = get_data()
    app.layout = html.Div(children=
    [
        html.Div
            ([
            html.H1(id='H1', children='Number of Arrests made each year', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='yearwise_arrests_plot', figure=yearwise_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Offenders for each arrest resolution', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='arrest_res_plot', figure=case_res(data))
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
            dcc.Graph(id='line_plot', figure=arrest_types(data))
        ]),
        ([
            html.H1(id='H1', children='Trend of number of offenders per year based on Arrest type',
                    style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=monthly_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests by race', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=arrests_by_race(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests by sex', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=arrests_by_sex(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Juvenile/Non-Juvenile Arrests', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=cat1_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Number of Arrests in each Age Group', style={'textAlign': 'center',
                                                                                 'marginTop': 40,
                                                                                 'marginBottom': 40}),
            dcc.Graph(id='line_plot', figure=cat2_arrests(data))
        ]),
        ([
            html.H1(id='H1', children='Crimes Commited by Different Age Groups', style={'textAlign': 'center',
                                                                                        'marginTop': 40,
                                                                                        'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=plot_fig1(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H2', children='Punishment for Crime Commited', style={'textAlign': 'center',
                                                                              'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=plot_fig2(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Method of Arresting the Suspect', style={'textAlign': 'center',
                                                                                'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=plot_fig3(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Relationship Between Offender Home City and Sex', style={'textAlign': 'center',
                                                                                'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=city_sex(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Relationship Between Offender Home City and Race',
                    style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=city_race(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Relationship Between Offender Home City and Age', style={'textAlign': 'center',
                                                                                'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=city_age(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Relationship Between Offender Home City and Crime Types',
                    style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=city_crime_type(data), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Crime Type VS Mean Age at Arrest',
                    style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=age_crimetype(age_df), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Number of Arrest made for different age category',
                    style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=age_crimecount(age_df), style={'width': 1500, 'height': 1000})
        ]),
        ([
            html.H1(id='H3', children='Count of People arrested vs Arrest Resolution',
                    style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
            dcc.Graph(id='bar_chart', figure=age_resolution(age_df), style={'width': 1500, 'height': 1000})
        ])
    ]
    )


if __name__ == '__main__':
    age_df = preprocess(get_data())
    dash_layout()
    app.run_server(debug=False)
