import streamlit as st
import pandas as pd
import numpy as np  

st.title("Streamlit app for data analysis for Stelco BOF model.")
st.write("This app allows you to upload a json file, display its contents, and perform basic data analysis.")
st.write("Developed by [Your Name].")

# File uploader
uploaded_file = st.file_uploader("Choose a JSON file", type="json")
LoadDefaults = st.checkbox('Load Default Data')
if LoadDefaults:
    uploaded_file = 'Static/default_data.json'  # Replace with your default file path
if uploaded_file is not None:
    # Read the JSON file
    data = pd.read_json(uploaded_file)
    
    # Display the data
    st.subheader("Data Preview")
    st.write(data.head())
    
    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())
    
    # Data visualization
    st.subheader("Data Visualization")
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_columns:
        column_to_plot = st.selectbox("Select a column to plot", numeric_columns)
        st.line_chart(data[column_to_plot])
    else:
        st.write("No numeric columns available for plotting.")