import pandas as pd
import streamlit as stl
import logging
import numpy as np
from matplotlib import pylab
from matplotlib import pyplot
import matplotlib
from pylab import *
import xlrd
import pickle
import streamlit_authenticator as stauth
from pathlib import Path

names = ["Sam Seuss", "Jane Craft"]
usernames = ["sseuss", "jcraft"]
passwords = ["password123", "password123"]

credentials = {"sseuss": "password123", "jcraft": "password123"}

logger = open("log.txt", 'a')


def check_credentials(username, password):
    if username in credentials.keys():
        if password == credentials[username]:
            return True


def login():
    user_name_container = stl.empty()
    password_container = stl.empty()
    login_container = stl.empty()
    username = user_name_container.text_input("Username")
    password = password_container.text_input("Password", type="password")
    login_btn = login_container.button("Login")

    if login_btn:
        if check_credentials(username, password):
            stl.session_state.logged_in = True
            user_name_container.empty()
            password_container.empty()
            login_container.empty()
            timestamp = str(datetime.datetime.now())
            logger.write("User logged in at: " + timestamp + "\n")
            logger.close()
        else:
            stl.error("Invalid username or password!")
            timestamp = str(datetime.datetime.now())
            logger.write("\n" + timestamp + " User entered invalid credentials...")
            logger.close()


if "logged_in" not in stl.session_state:
    login()

if "logged_in" in stl.session_state:
    df = pd.read_excel("RBRTEd.xls", sheet_name="Data 1", skiprows=2801,
                       names=['Date', 'Brent_Price'])

    header = stl.container()
    descriptive_method = stl.container()
    non_descriptive = stl.container()
    df["Month"] = df["Date"].dt.month
    df["Year"] = df["Date"].dt.year

    with header:
        stl.title("Zachary Elmalak - C964 Capstone")

    with descriptive_method:
        stl.title("Descriptive Methods")
        first_scatter = pyplot.figure()
        pyplot.title("Overall Oil Price Scattergram")
        pyplot.plot(df['Brent_Price'])
        stl.pyplot(first_scatter)

        first_histo = pyplot.figure()
        pyplot.title("Overall Oil Price Histogram")
        pyplot.hist(df['Brent_Price'], bins=100)
        stl.pyplot(first_histo)

        percent_change_graph = pyplot.figure()
        pyplot.title("Oil Price Percentage Change")
        change_brent = df['Brent_Price'].pct_change()
        change_brent.hist(bins=100, range=(-0.1, 0.1))
        stl.pyplot(percent_change_graph)

    with non_descriptive:
        stl.title("Non-descriptive Methods")
        year_container = stl.empty()
        try:
            testing = year_container.text_input(
                "Enter two years separated by a comma between 1999-2022. Ex: 1999, 2000")
            if testing != "":
                first_year = int(testing.split(', ')[0])
                second_year = int(testing.split(', ')[1])
                if first_year < 1999 or second_year > 2022:
                    logging.basicConfig(filename="log.txt")
                    stl.error("Please enter a date between 1999 and 2022")
                    logging.warning("User entered invalid dates, can cause potential crash...")
                else:
                    timestamp = str(datetime.datetime.now())
                    logger.write("\n" + timestamp + " Program working as expected...")
                    logger.close()
                    average_scatter = pyplot.figure()
                    pyplot.title("Monthly Average for " + str(first_year) + " & " + str(second_year))
                    pyplot.plot(df[df.Year == first_year].groupby("Month")["Brent_Price"].mean(), )
                    pyplot.plot(df[df.Year == second_year].groupby("Month")["Brent_Price"].mean(),
                                color="Green")
                    pyplot.xlabel("Month")
                    stl.pyplot(average_scatter)
                    rise_change_index = change_brent[change_brent > 0.1].shape[0]
                    drop_change_index = change_brent[change_brent < 0.1].shape[0]
                    rise_formula = 100 * rise_change_index / change_brent.shape[0]
                    drop_formula = 100 * drop_change_index / change_brent.shape[0]

                    stl.text("Oil prices have a %1.2f%% " % rise_formula + " chance of rising more than 10%")
                    stl.text("Oil prices have a %1.2f%% " % drop_formula + " chance of dropping more than 10%")

                    brent_monthly = df.pivot_table(values="Brent_Price", columns=["Year"], aggfunc=np.mean,
                                                   index=["Month"])
                    brent_monthly = brent_monthly.dropna(axis=1)

                    brent_monthly_change = brent_monthly.pct_change()
                    brent_monthly_change = brent_monthly_change.drop(brent_monthly_change.index[0])
                    brent_monthly_change["Rise"] = \
                        brent_monthly_change[(brent_monthly_change.iloc[0:, :] > 0)].count(axis=1) / (
                            2022)
                    brent_monthly_change["Drop"] = \
                        brent_monthly_change[(brent_monthly_change.iloc[0:, :] < 0)].count(axis=1) / (
                            2022)

                    prediction_scatter = pyplot.figure()
                    pyplot.title("Price Predictions Probabilities")
                    pyplot.plot(brent_monthly_change["Rise"], color="Green")
                    pyplot.plot(brent_monthly_change["Drop"], color="Red")
                    pyplot.ylabel("Percent")
                    pyplot.xlabel("Month")
                    stl.pyplot(prediction_scatter)
        except:
            stl.error("Please enter a valid date")
            timestamp = str(datetime.datetime.now())
            logger.write("\n" + timestamp + " User entered an invalid date...")
            logger.close()
