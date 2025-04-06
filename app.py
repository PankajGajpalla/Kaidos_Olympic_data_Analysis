import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper
import plotly.express as px
import plotly.figure_factory as ff

import zipfile

with zipfile.ZipFile('athlete_events.csv.zip') as z:
    with z.open('athlete_events.csv') as f:
        df = pd.read_csv(f)


# df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("Olympic_rings.png")

user_menu = st.sidebar.radio(
    'Select an option', ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# st.dataframe(df)


if user_menu == 'Medal Tally':

    # st.header('Medal Tally') this will make in content page and below wala code does it in sidebar
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)


    # medal_tally = helper.medal_tally(df)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == "Overall" and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal tally in " + str(selected_year))
    elif selected_year == "Overall" and selected_country != "Overall":
        st.title("Year-wise medal won by "+ selected_country)
    else:
        st.title("Medal tally for " + selected_country +" in " + str(selected_year))


    # st.dataframe(medal_tally)
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    Editions = df['Year'].unique().shape[0] -1
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events = df['Event'].unique().shape[0]
    Athelets = df['Name'].unique().shape[0]
    Nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(Editions)
    with col2:
        st.header("Cities")
        st.title(Cities)
    with col3:
        st.header("Sports")
        st.title(Sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(Events)
    with col2:
        st.header("Athelets")
        st.title(Athelets)
    with col3:
        st.header("Nations")
        st.title(Nations)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y='region')
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athelets_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athelets_over_time, x="Edition", y="Name")
    st.title("Athelets over the years")
    st.plotly_chart(fig)


    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)


    st.title("Most successful Athelets")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select a Sport", sport_list)
    xf = helper.most_successful(df, "Overall")
    st.table(xf)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select country ", country_list)

    country_df = helper.year_wise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+ " Medal Tally over the years")
    st.plotly_chart(fig)


    st.title(selected_country + " excels in the following sport")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athelets of "+ selected_country)
    top10_df = helper.most_successful_country_wise(df, selected_country)
    st.table(top10_df)


if user_menu == 'Athlete-wise Analysis':
    athelet_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athelet_df['Age'].dropna()
    x2 = athelet_df[athelet_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelet_df[athelet_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelet_df[athelet_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distributoin of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Athletics', 'Gymnastics', 'Swimming', 'Shooting', 'Cycling', 'Fencing', 'Rowing', 'Cross Country Skiing',
     'Alpine Skiing', 'Wrestling', 'Football', 'Sailing', 'Equestrianism', 'Canoeing', 'Boxing', 'Speed Skating',
     'Ice Hockey', 'Hockey', 'Biathlon', 'Basketball', 'Weightlifting', 'Water Polo', 'Judo', 'Handball',
     'Art Competitions', 'Volleyball', 'Bobsleigh', 'Tennis', 'Diving', 'Ski Jumping', 'Archery', 'Figure Skating',
     'Table Tennis', 'Modern Pentathlon', 'Short Track Speed Skating', 'Luge', 'Badminton', 'Nordic Combined',
     'Freestyle Skiing', 'Snowboarding', 'Synchronized Swimming', 'Baseball']
    for sport in famous_sports:
        temp_df = athelet_df[athelet_df['Sport'] == sport]
        age_data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        if not age_data.empty:
            x.append(age_data)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distributoin of Age wrt sports(Gold Medalist)")
    st.plotly_chart(fig)


    st.title("Height vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a Sport", sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'], y = temp_df['Height'], hue= temp_df['Medal'], style= temp_df['Sex'], s=100)

    st.pyplot(fig)


    st.title("Men Vs Women participation over the years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)




