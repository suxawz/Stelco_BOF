import streamlit as st
import pandas as pd
if st.session_state.get('df') is not None:
    df = st.session_state.df
    st.title("Performance Value Analysis")
    st.write("This page allows you to analyze the performance values from the uploaded data.")
    
    st.dataframe(df.columns)
else:
    st.write("Please upload a JSON file on the main page to analyze performance values.")    