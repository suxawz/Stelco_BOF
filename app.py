import streamlit as st
import pandas as pd
import numpy as np  
from pathlib import Path

st.title("Streamlit app for data analysis for Stelco BOF model.")
st.write("This app allows you to upload a json file, display its contents, and perform basic data analysis.")
st.write("Developed by [Your Name].")
# File uploader
uploaded_file = st.file_uploader("Choose a JSON file", type="json")
LoadDefaults = st.checkbox('Load Default Data')
if LoadDefaults:
    base_path = Path(__file__).parent
    relative_path = Path('Static/default_data.json')
    uploaded_file = base_path / relative_path
if uploaded_file is not None:
    # Read the JSON file
    data = pd.read_json(uploaded_file)

 
    if 'df' not in st.session_state:
        st.session_state.df = data
    
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