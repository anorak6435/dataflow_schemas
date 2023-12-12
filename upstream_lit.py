import streamlit as st
import pandas as pd

df = pd.read_csv("D:\projects\Blok_2_Data_Science\DataScience_poverty_casus_data\Data\BenBuurt2015.csv")
st.dataframe(df)