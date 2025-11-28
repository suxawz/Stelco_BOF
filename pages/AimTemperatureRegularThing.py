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
    df = df.fillna(0)
    df = df[(abs(df[Data_columns['AimtempEOB']])>1000)&(df['CeloxTemp']>1500)&(df['AimC']>0.01)&(df['CeloxCarbon']>0.01)&(df['ACTUAL_SIC']<=0.1)&(df['PRED_SIC']<=0.1)]
    return df

def ModelPerformanceValue(df):

    st.write(df.describe())
    #filter by AimtempEOB 1650
    Temp_Range_Start,Temp_Range_end = st.slider('Delta Temp Range Performance', float(df['AimtempEOB'].min()), float(df['AimtempEOB'].max()), (float(1600), float(1650)))
    mask = (df['AimtempEOB'] >= Temp_Range_Start) & (df['AimtempEOB'] <= Temp_Range_end)
    df = df.loc[mask]

    df['CorrectionTemperature'] = df['CeloxTemp'] - (df['PRED_LIME'] - df['ACTUAL_LIME']) * 0.00665 - (df['PRED_DOLO'] - df['ACTUAL_DOLO']) * 0.008 - (df['PRED_ORE'] - df['ACTUAL_ORE']) * 0.0434
    df['delta_temp'] = -df['AimtempEOB'] + df['CorrectionTemperature']
    df['Ratio_HM_Scrap'] = df['ActHotMetalWeight']/(df['ActTotal'])

    df = df[(abs(df['delta_temp'])<100)]
    st.write(df.describe())
    fig, ax = plt.subplots(figsize=(10,5))
    ax.scatter(df['AimtempEOB'], df['delta_temp'], label='Delta Temperatue', color='blue')
    #ax.plot(df['CalculationTime'], df['PRED_ORE'], label='Predicted Iron Ore', color='orange')
    ax.set_xlabel('Aim Temp EOB')
    ax.set_ylabel('Celox Temp - Aim Temp EOB')
    ax.set_title('Delta Temperature vs Aim Temp EOB')
    ax.legend()
    st.pyplot(fig)
    st.write("Delta Temperature Statistics:")
    st.write(df['delta_temp'].describe())

    st.write(df.describe())
    fig, ax = plt.subplots(figsize=(10,5))
    ax.scatter(df['Ratio_HM_Scrap'], df['delta_temp'], label='Delta Temperatue', color='blue')
    #ax.plot(df['CalculationTime'], df['PRED_ORE'], label='Predicted Iron Ore', color='orange')
    ax.set_xlabel('Ratio_HM_Scrap')
    ax.set_ylabel('Correct temp - Aim Temp EOB')
    ax.set_title('Delta Temperature vs HM_Scrap Ratio')
    ax.legend()
    st.pyplot(fig)



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
        ModelPerformanceValue(filtered_data)    
    
else:
    st.write("Please upload a JSON file on the main page to analyze performance values.")    
 