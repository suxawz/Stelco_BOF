import streamlit as st
import pandas as pd
from streamlit_extras.altex import *
import matplotlib.pyplot as plt
import ExportClasses as EC
from scipy import stats
import numpy as np
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
    #select heat use model setpoints
    st.selectbox("Select Heat used model setpoints", ['All Heats no filter', 'Model Heats Only Blowing&Flux Active'], key='heat_number_type')
    if st.session_state.heat_number_type == 'Model Heats Only Blowing&Flux Active':
        df = df[(df['BlowingProfileActive'] == 1)&(df['MaterialFluxActive'] ==1)&(df['MaterialTappingActive']==1)]
    else:
        #select heats materials within 10% of model predicted values
        st.write("Optionally, you can apply a material filter to select heats where actual material inputs are within 500 Kg of predicted values.")
        material_filter = st.checkbox('Apply Material Filter', value=False)
        if material_filter:
            #replace missing values with 0 for comparison
            df = df.fillna(0)
            df = df[(abs(df['PRED_LIME'] - df['ACTUAL_LIME'])<= 500)&(abs(df['PRED_DOLO'] - df['ACTUAL_DOLO'])<= 500)&(abs(df['PRED_ORE'] - df['ACTUAL_ORE'])<= 500)&(abs(df['PRED_SIC'] - df['ACTUAL_SIC'])<= 500)]
            if df.empty:
                st.warning("No data available after applying material filter. Please adjust the filter criteria.")
    return df
# Function to calculate performance values
def ModelPerformanceValue(df):
    df = df.copy(deep=True)

    #create a new date column for grouping
    df['Date'] = df['CalculationTime'].dt.date
    #devided selected date range data by days weeks or months
    devidedtype = st.selectbox("Select the date Devide type", ['Daily', 'Weekly', 'Monthly'] , key='date_devide_type')
    if devidedtype == 'Daily':
        groupedDaily = df.groupby(df['Date'])    
        df['Daily'] = df['CalculationTime'].dt.to_period('D').apply(lambda r: r.start_time)
    elif devidedtype == 'Weekly':
        df['Weekly'] = df['CalculationTime'].dt.to_period('W').apply(lambda r: r.start_time)
        groupedDaily = df.groupby('Weekly')
    elif devidedtype == 'Monthly':
        df['Monthly'] = df['CalculationTime'].dt.to_period('M').apply(lambda r: r.start_time)
        groupedDaily = df.groupby('Monthly')
    else:
        groupedDaily = [('All Data', df)]
    df['delta_temp'] = -df['AimtempEOB'] + df['CeloxTemp']
    df['delta_C'] = -df[Data_columns["AimAnalEOBC"]] + df['CeloxCarbon']
    dfsummary = df.copy(deep=True)
    Temp_Range_Start,Temp_Range_end = st.slider('Delta Temp Range Performance', float(df['delta_temp'].min()), float(df['delta_temp'].max()), (float(-15), float(20)))
    Carbon_Range_Start,Carbon_Range_end = st.slider('Delta C Range Perforamnce', float(df['delta_C'].min()), float(df['delta_C'].max()), (float(-0.02), float(0.02))) 
    PerformanceData = []   
    for name, group in groupedDaily:
        #st.write(f"### Performance Analysis for {devidedtype}: {name}")
        #st.write(f"Number of Records: {len(group)}")
        df = group.copy()
        GroupDate = df[devidedtype]
        performance_data_Temp = df[(df['delta_temp'] >= Temp_Range_Start) & (df['delta_temp'] <= Temp_Range_end)].count()/df.count()
        performance_data_C = df[(df['delta_C'] >= Carbon_Range_Start) & (df['delta_C'] <= Carbon_Range_end)].count()/df.count()
        performance_data_C_Temp = df[(df['delta_temp'] >= Temp_Range_Start) & (df['delta_temp'] <= Temp_Range_end) & (df['delta_C'] >= Carbon_Range_Start) & (df['delta_C'] <= Carbon_Range_end)].count()/df.count()
        Entries = EC.DynamicClass(a=None)
        Entries.Add(**{ 'Date': GroupDate.iloc[0]})
        Entries.Add(**{'Heats_records': len(group)})
        Entries.Add(**{ 'performance_data_Temp': performance_data_Temp})
        Entries.Add(**{ 'performance_data_C': performance_data_C})
        Entries.Add(**{ 'performance_data_C_Temp': performance_data_C_Temp})  # Assuming BlowEndTime is same as CeloxTempDateTime for simplicity

        PerformanceData.append(Entries)
    st.write("### Summary of Performance Data")
    Summary_df = pd.DataFrame([{
        'Date': entry.Date, 
        'Heats_records': entry.Heats_records,
        'Performance_Temp': entry.performance_data_Temp['delta_temp'], 
        'Performance_C': entry.performance_data_C['delta_C'],
        'Performance_C_Temp': entry.performance_data_C_Temp['delta_C']
        } for entry in PerformanceData])
    st.write(Summary_df)

    # Plotting the summary
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(Summary_df['Date'], Summary_df['Performance_C'], label='Performance C', marker='o', color='blue')
    ax2 = ax.twinx()  
    ax2.plot(Summary_df['Date'], Summary_df['Performance_Temp'], label='Performance Temp', marker='*', color='red')
    ax2.plot(Summary_df['Date'], Summary_df['Performance_C_Temp'], label='Performance C & Temp', marker='x', color='green')
    ax.set_title(f'Performance Values Over {devidedtype}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Performance Value')
    ax.legend()
    ax2.set_ylabel('Performance Value')
    ax2.legend(loc='upper right')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    # Plotting the summary

    # #3D bar chart with lines for performance values
    # from mpl_toolkits.mplot3d import Axes3D
    # fig = plt.figure(figsize=(10, 6))
    # ax = fig.add_subplot(111, projection='3d')
    # xpos = np.arange(len(Summary_df))
    # ypos = np.zeros(len(Summary_df))
    # zpos = np.zeros(len(Summary_df))
    # dx = np.ones(len(Summary_df)) * 0.2
    # dy = np.ones(len(Summary_df)) * 0.1
    # dz_temp = Summary_df['Performance_Temp'] * 100
    # dz_C = Summary_df['Performance_C'] * 100
    # dz_C_Temp = Summary_df['Performance_C_Temp'] * 100
    # ax.bar3d(xpos, ypos+0.3, zpos, dx, dy, dz_temp, color='r', alpha=0.6, label='Performance Temp')
    # ax.bar3d(xpos, ypos+0.6, zpos, dx, dy, dz_C, color='b', alpha=0.6, label='Performance C')
    # ax.bar3d(xpos, ypos, zpos, dx, dy, dz_C_Temp, color='g', alpha=0.6, label='Performance C & Temp')
    # ax.set_xticks(xpos + 0.3)
    # ax.set_xticklabels(Summary_df['Date'], rotation=45, ha='right')
    # ax.set_ylabel('Performance Type')
    # ax.set_zlabel('Performance Value (%)',position=(0,0,0))
    # ax.set_title('3D Bar Chart of Performance Values')
    # ax.legend()
    # st.pyplot(fig)
    
    # #3D scatter plot for delta_temp and delta_C
    # fig = plt.figure(figsize=(10, 6))
    # ax = fig.add_subplot(111, projection='3d')
    # clean_data = dfsummary[['delta_temp', 'delta_C','CeloxTemp']].dropna()
    # ax.scatter(clean_data['delta_temp'], clean_data['delta_C'], clean_data['CeloxTemp'], c='b', marker='o')
    # ax.set_xlabel('Delta Temp')
    # ax.set_ylabel('Delta C')
    # ax.set_zlabel('Calculation Time')
    # ax.set_title('3D Scatter Plot of Delta Temp vs Delta C over Time')
    # st.pyplot(fig)

    


     # Filter data based on slider values
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].hist(dfsummary['delta_temp'], bins=30, color='skyblue', edgecolor='black')
    ax[0].set_title('Histogram of Delta Temp')
    ax[0].set_xlabel('Delta Temp')
    ax[0].set_ylabel('Frequency')
    ax[0].axvline(Temp_Range_Start, color='red', linestyle='dashed', linewidth=1)
    ax[0].axvline(Temp_Range_end, color='red', linestyle='dashed', linewidth=1)
    #normal distribution curve for delta_temp
    #normal distribution curve
    mu, std = stats.norm.fit(dfsummary['delta_temp'].dropna())
    xmin, xmax = ax[0].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    ax[0].plot(x, p * len(dfsummary['delta_temp']) * (xmax - xmin) / 30, 'k', linewidth=2)
    #draw normal value lines
    ax[0].axvline(mu, color='green', linestyle='dashed', linewidth=2)  





    ax[1].hist(dfsummary['delta_C'], bins=30, color='lightgreen', edgecolor='black')
    ax[1].set_title('Histogram of Delta C')
    ax[1].set_xlabel('Delta C')
    ax[1].set_ylabel('Frequency')
    ax[1].axvline(Carbon_Range_Start, color='red', linestyle='dashed', linewidth=1)
    ax[1].axvline(Carbon_Range_end, color='red', linestyle='dashed', linewidth=1)
    #normal distribution curve for delta_C
    mu_c, std_c = stats.norm.fit(dfsummary['delta_C'].dropna())
    xmin_c, xmax_c = ax[1].get_xlim()
    x_c = np.linspace(xmin_c, xmax_c, 100)
    p_c = stats.norm.pdf(x_c, mu_c, std_c)
    ax[1].plot(x_c, p_c * len(dfsummary['delta_C']) * (xmax_c - xmin_c) / 30, 'k', linewidth=2)
    #draw normal value lines
    ax[1].axvline(mu_c, color='green', linestyle='dashed', linewidth=2)   
    plt.tight_layout()
    st.pyplot(fig) 
    #performance data evaluation
    st.write("Overall Performance Summary for Selected Date Range:")
    st.write("Total Records Analyzed: ", len(dfsummary))
    performance_data_Temp = dfsummary[(dfsummary['delta_temp'] >= Temp_Range_Start) & (dfsummary['delta_temp'] <= Temp_Range_end)].count()/dfsummary.count()
    performance_data_C = dfsummary[(dfsummary['delta_C'] >= Carbon_Range_Start) & (dfsummary['delta_C'] <= Carbon_Range_end)].count()/dfsummary.count()
    performance_data_C_Temp = dfsummary[(dfsummary['delta_temp'] >= Temp_Range_Start) & (dfsummary['delta_temp'] <= Temp_Range_end) & (dfsummary['delta_C'] >= Carbon_Range_Start) & (dfsummary['delta_C'] <= Carbon_Range_end)].count()/dfsummary.count()
    st.write(f"Performance within Delta Temp range ({Temp_Range_Start}, {Temp_Range_end}): {performance_data_Temp['delta_temp']:.2%}")
    st.write(f"Performance within Delta C range ({Carbon_Range_Start}, {Carbon_Range_end}): {performance_data_C['delta_C']:.2%}")
    st.write(f"Performance within both Delta Temp and Delta C ranges: {performance_data_C_Temp['delta_C']:.2%}")






if st.session_state.get('df') is not None:
    df = st.session_state.df
    
    st.title("Performance Value Analysis")
    st.write("This page allows you to analyze the performance values from the uploaded data.")
     # Specify the datetime columns to convert
    date_cols = ['CalculationTime','CeloxTempDateTime','BlowStartTime']
    df = convert_to_datetime(df, date_cols)
    #st.write(df[date_cols])
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
        #st.write("Basic Statistics of Filtered Data:")
        #st.write(filtered_data.describe())
        # Call the ModelPerformanceValue function
        filtered_data = data_validation(filtered_data)
        ModelPerformanceValue(filtered_data)    
    
else:
    st.write("Please upload a JSON file on the main page to analyze performance values.")    
 