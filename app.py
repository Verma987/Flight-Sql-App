import streamlit as st
from dbhelper import DB
import plotly.graph_objects as go
import plotly.express as px
import folium
import pandas as pd


db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu', ['Select One', 'Check Flights', 'Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')

    col1, col2 = st.columns(2)
    city = db.fetch_city_names()

    with col1:
        source = st.selectbox('Source', sorted(city))
    with col2:
        destination = st.selectbox('Destination', sorted(city))

    price_range = st.slider('Price Range', 0, 10000, (0, 10000), step=100)
    duration_range = st.slider('Duration Range (hours)', 0.0, 24.0, (0.0, 24.0), step=0.5)

    if st.button('Search'):
        results = db.fetch_all_flights(source, destination, start_date, end_date, min_price, max_price, airline)
        st.dataframe(results)



elif user_option == 'Analytics':
    st.header('Airline Frequency')
    airline, frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))
    st.plotly_chart(fig)

    st.header('Busy Airports')
    city, frequency1 = db.busy_airport()
    fig = px.bar(
        x=city,
        y=frequency1,
        labels={'x': 'City', 'y': 'Number of Flights'},
        title='Number of Flights per Airport'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.header('Daily Flight Frequency')
    date, frequency2 = db.daily_frequency()
    fig = px.line(
        x=date,
        y=frequency2,
        labels={'x': 'Date', 'y': 'Number of Flights'},
        title='Daily Flight Frequency'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.header('Price Trends')
    source_city = st.selectbox('Source for Price Trend', sorted(city))
    destination_city = st.selectbox('Destination for Price Trend', sorted(city))
    if st.button('Show Price Trend'):
        date, price = db.fetch_price_trend(source_city, destination_city)
        fig = px.line(
            x=date,
            y=price,
            labels={'x': 'Date', 'y': 'Average Price'},
            title='Price Trend over Time'
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.header('Historical Price Trends')
    airline, date, price = db.fetch_historical_price_trends()
    fig = px.line(
        x=date,
        y=price,
        color=airline,
        labels={'x': 'Date', 'y': 'Average Price'},
        title='Historical Price Trends by Airline'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)



    st.header('Airport Rankings')
    airport, ranking = db.fetch_airport_rankings()
    fig = px.bar(
        x=airport,
        y=ranking,
        labels={'x': 'Airport', 'y': 'Number of Flights'},
        title='Top Airports by Number of Flights'
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)



else:
    st.title('Flight Dashboard')
