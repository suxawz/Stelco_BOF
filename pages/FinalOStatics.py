import streamlit as st
import pandas as pd
from streamlit_extras.altex import *
import matplotlib.pyplot as plt
Data_columns = {"BOFCalculationID":"BOFCalculationID"
,"Grade":"Grade"
,"AimAnalEOBC":"AimAnalEOBC"
,"CalculationTime":"CalculationTime"
,"HeatNumber":"HeatNumber"
,"ModelHeatID":"ModelHeatID"
,"HotMetalTemp":"HotMetalTemp"
,"HotMetalC":"HotMetalC"
,"HotMetalSi":"HotMetalSi"
,"HotMetalP":"HotMetalP"
,"AimC":"AimC"
,"AimP":"AimP"
,"PredC":"PredC"
,"PredFeO":"PredFeO"
,"MixAnalysisC":"MixAnalysisC"
,"MixAnalysisSi":"MixAnalysisSi"
,"ModelTemp":"ModelTemp"
,"AimtempEOB":"AimtempEOB"
,"PredBascy":"PredBascy"
,"ModelHotMetalWeight":"ModelHotMetalWeight"
,"PredBush1":"PredBush1"
,"PredHMS1":"PredHMS1"
,"PredHomeScrap":"PredHomeScrap"
,"PredPAndS":"PredPAndS"
,"PredPitScrap":"PredPitScrap"
,"PredScrap":"PredScrap"
,"PredShred":"PredShred"
,"PredSlabCrops":"PredSlabCrops"
,"PredTundish":"PredTundish"
,"PredTotal":"PredTotal"
,"ActTotal":"ActTotal"
,"PRED_ORE":"PRED_ORE"
,"PRED_LIME":"PRED_LIME"
,"PRED_DOLO":"PRED_DOLO"
,"ActCastingLadle":"ActCastingLadle"
,"OxygenVolumePred":"OxygenVolumePred"
,"BlowingProfileActive":"BlowingProfileActive"
,"MaterialFluxActive":"MaterialFluxActive"
,"MaterialTappingActive":"MaterialTappingActive"
,"SteelAnalysisC":"SteelAnalysisC"
,"SteelAnalysisP":"SteelAnalysisP"
,"TempMeasTemp":"TempMeasTemp"
,"TempMeasTempModel":"TempMeasTempModel"
,"TempMeasTempTime":"TempMeasTempTime"
,"CeloxTemp":"CeloxTemp"
,"CeloxOxygen":"CeloxOxygen"
,"CeloxCarbon":"CeloxCarbon"
,"CeloxTempModel":"CeloxTempModel"
,"CeloxTempDateTime":"CeloxTempDateTime"
,"ModelSteelMass":"ModelSteelMass"
,"ActHotMetalWeight":"ActHotMetalWeight"
,"ActBush1":"ActBush1"
,"ActHMS1":"ActHMS1"
,"ActHomeScrap":"ActHomeScrap"
,"ActPAndS":"ActPAndS"
,"ActPitScrap":"ActPitScrap"
,"ActScrap":"ActScrap"
,"ActShred":"ActShred"
,"ActSlabCrops":"ActSlabCrops"
,"ActTundish":"ActTundish"
,"ACTUAL_ORE":"ACTUAL_ORE"
,"ACTUAL_LIME":"ACTUAL_LIME"
,"ACTUAL_DOLO":"ACTUAL_DOLO"
,"PRED_SIC":"PRED_SIC"
,"OxygenVolumeAct":"OxygenVolumeAct"
,"ACTUAL_SIC":"ACTUAL_SIC"
,"SlagAnalysisSiO2":"SlagAnalysisSiO2"
,"SlagAnalysisFeO":"SlagAnalysisFeO"
,"SlagAnalysisCaO":"SlagAnalysisCaO"
,"SlagAnalysisMgO":"SlagAnalysisMgO"
,"ActBascy":"ActBascy"
,"PRED_FESI":"PRED_FESI"
,"PredDealerBundles":"PredDealerBundles"
,"ActDealerBundles":"ActDealerBundles"
,"PredLowSStelcoPigIro":"PredLowSStelcoPigIro"
,"ActLowSStelcoPigIro":"ActLowSStelcoPigIro"
,"PredPrimeBundles":"PredPrimeBundles"
,"ActPrimeBundles":"ActPrimeBundles"
,"ACTUAL_FESI":"ACTUAL_FESI"}
#### deal with datetime conversion issues
def convert_to_datetime(df, date_cols):
   # # Ensure datetime columns are in datetime format
        # Display the data
    #st.subheader("Data Preview")
    #st.write(df.head())
    df = df.dropna(subset=date_cols)
    for col in date_cols:
        df[col] = df[col].str[:19]  # Truncate to first 19 characters ignore the milliseconds.
    # Display the data
    #st.subheader("Data Preview")
    #st.write(df.head())
    #transfer json datatime to pandas datetime
    for col in date_cols:
        try:
            print(col)
            df[col] = pd.to_datetime(df[col],format='%Y-%m-%d %H:%M:%S', errors='coerce').dt.floor('s')
        except (ValueError, TypeError):
            pass
    # Display the data
    #st.subheader("Data Preview")
    #st.write(df.head())
    st.write("Select date range records to analyze performance values.")
    return df 
 
def data_validation(df):
    df = df[(abs(df[Data_columns['AimtempEOB']])>1000)&(df['CeloxTemp']>1500)&(df['AimC']>0.01)&(df['CeloxCarbon']>0.01)]
    return df

def FinalOStatics(filtered_data):

    def CalcOModel(AimTemp,AimEOBC,)
    raise NotImplementedError

if st.session_state.get('df') is not None:
    df = st.session_state.df
    
    st.title("Aim Temperature Value Analysis")
    st.write("This page allows you to analyze the Aim EOB values from the uploaded data.")
     # Specify the datetime columns to convert
    date_cols = ['CalculationTime','CeloxTempDateTime','BlowStartTime']
    df = convert_to_datetime(df, date_cols)
    st.write(df[date_cols])
    date_column = st.selectbox("Select the date column", df.select_dtypes(include=['datetime64']).columns)
    #if pd.api.types.is_datetime64_any_dtype(df[date_column]):
    start_date = st.date_input("Start date", df[date_column].max()-pd.DateOffset(months=2))
    end_date = st.date_input("End date", df[date_column].max())
    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
    else:
        mask = (df[date_column] >= pd.to_datetime(start_date)) & (df[date_column] <= pd.to_datetime(end_date))
        filtered_data = df.loc[mask]
        #st.write(f"Filtered data from {start_date} to {end_date}:")
        #st.dataframe(filtered_data)
        st.write("Basic Statistics of Filtered Data:")
        st.write(filtered_data.describe())
        # Call the ModelPerformanceValue function
        filtered_data = data_validation(filtered_data)
        FinalOStatics(filtered_data)    
    
else:
    st.write("Please upload a JSON file on the main page to analyze performance values.")    
 