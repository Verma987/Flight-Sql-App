import mysql.connector
import pandas as pd
import numpy as np
import requests

class DB:
    def __init__(self):
        # connect to the database
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='mantu123',
                database='flight'

            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except:
            print('Connection error')
        self.api_key = 'YOUR_GOOGLE_MAPS_API_KEY'

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
        SELECT DISTINCT(Destination) FROM flight
        UNION
        SELECT DISTINCT(Source) FROM flight
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
        return city


    def fetch_all_flights(self, source, destination, price_range=None, duration_range=None):
        query = """
        SELECT Airline, Route, Dep_Time, Duration, Price FROM flight
        WHERE Source = '{}' AND Destination = '{}'
        """.format(source, destination)

        if price_range:
            query += " AND Price BETWEEN {} AND {}".format(price_range[0], price_range[1])
        if duration_range:
            query += " AND Duration BETWEEN '{}' AND '{}'".format(duration_range[0], duration_range[1])

        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        self.mycursor.execute("""
        SELECT Airline, COUNT(*) FROM flight
        GROUP BY Airline
        """)
        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            frequency.append(item[1])
        return airline, frequency

    def busy_airport(self):
        city = []
        frequency = []
        self.mycursor.execute("""
        SELECT Source, COUNT(*) FROM (
            SELECT Source FROM flight
            UNION ALL
            SELECT Destination FROM flight
        ) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            frequency.append(item[1])
        return city, frequency

    def daily_frequency(self):
        date = []
        frequency = []
        self.mycursor.execute("""
        SELECT Date_of_Journey, COUNT(*) FROM flight
        GROUP BY Date_of_Journey
        """)
        data = self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            frequency.append(item[1])
        return date, frequency

    def fetch_price_trend(self, source, destination):
        date = []
        price = []
        self.mycursor.execute("""
        SELECT Date_of_Journey, AVG(Price) FROM flight
        WHERE Source = '{}' AND Destination = '{}'
        GROUP BY Date_of_Journey
        ORDER BY Date_of_Journey
        """.format(source, destination))
        data = self.mycursor.fetchall()
        for item in data:
            date.append(item[0])
            price.append(item[1])
        return date, price


    def fetch_historical_price_trends(self):
        airline = []
        date = []
        price = []
        self.mycursor.execute("""
                SELECT Airline, Date_of_Journey, AVG(Price) FROM flight
                GROUP BY Airline, Date_of_Journey
                ORDER BY Date_of_Journey
                """)
        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            date.append(item[1])
            price.append(item[2])
        return airline, date, price



    def fetch_airport_rankings(self):
        airport = []
        ranking = []
        self.mycursor.execute("""
                SELECT Source, COUNT(*) FROM flight
                GROUP BY Source
                ORDER BY COUNT(*) DESC
                """)
        data = self.mycursor.fetchall()
        for item in data:
            airport.append(item[0])
            ranking.append(item[1])
        return airport, ranking
