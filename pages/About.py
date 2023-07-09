import streamlit as st

st.markdown("""# Streamlit RNG Data Visualization App

An application that takes TRNG data from an AWS S3 Bucket and analyzes it into a graph and a dataframe.

## Features

- Login functionality with username and password verification;
- The user can select which file he wants to work on in the side menu;
- After clicking on "Show Graph", a graph will be displayed with the data and the standard deviation and, below, the dataframe used.""")