import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.altex import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
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
# Function to calculate Iron value values
def ModelPerformanceIronOreValue(df):
    df['delta_temp'] = -df['AimtempEOB'] + df['CeloxTemp']
    df['delta_C'] = df[Data_columns["AimAnalEOBC"]] - df['CeloxCarbon']
    df['delta_Ore'] = df['ACTUAL_ORE'] - df['PRED_ORE']
    #Temp_Range_Start,Temp_Range_end = st.slider('Delta Temp Range Performance', float(df['delta_temp'].min()), float(df['delta_temp'].max()), (float(-20), float(20)))
    #Carbon_Range_Start,Carbon_Range_end = st.slider('Delta C Range Perforamnce', float(df['delta_C'].min()), float(df['delta_C'].max()), (float(-0.02), float(0.02)))
    st.write("Line chart for Actual vs Predicted Iron Ore amount:")
    # sparkbar_chart(
    #     data=df,
    #     x=Data_columns['CalculationTime'],
    #     y="delta_temp",
    #     title="A beautiful sparkbar chart",
    # )  
    df = df[(abs(df[Data_columns['ACTUAL_ORE']])>0)&(df['PRED_ORE']>0)]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df['CalculationTime'], df['ACTUAL_ORE'], label='Actual Iron Ore', color='blue')
    ax.plot(df['CalculationTime'], df['PRED_ORE'], label='Predicted Iron Ore', color='orange')
    ax.set_xlabel('Calculation Time')
    ax.set_ylabel('Iron Ore Amount')
    ax.set_title('Actual vs Predicted Iron Ore Amount Over Time')
    ax.legend()
    st.pyplot(fig)
    st.write("Scatter plot for Delta Ore and Delta Temp vs Actual Iron Ore:")



    fig,ax1 = plt.subplots(figsize=(10,5))
    ax1.set_xlabel('ACTUAL_ORE')
    ax1.set_ylabel('Delta Ore', color='tab:blue')
    ax1.scatter(df['ACTUAL_ORE'], df['delta_Ore'], color='tab:blue', alpha=0.6, label='Delta Ore')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Delta Temp', color='tab:red')  # we already handled
    ax2.scatter(df['ACTUAL_ORE'], df['delta_temp'], color='tab:red', alpha=0.6, label='Delta Temp')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    fig.suptitle('Delta Ore and Delta Temp vs ACTUAL_ORE')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    st.pyplot(fig)

    colNames = ['ACTUAL_ORE', 'delta_Ore']
    x  = df[colNames[0]].values
    y  = df[colNames[1]].values

    # Optimization function
    def func(t, a, b):
        return a*np.log(t) + b
  
    # Perform the curve fit
    # return:
    # popt (array): Optimal values for the poptameters so that the sum of the squared residuals of f(xdata, *popt) - ydata is minimized.
    # pcov2-D (array): The estimated covariance of popt. The diagonals provide the variance of the poptameter estimate. 
    popt, pcov = curve_fit(func, x, y)
    print("Parameter optimized: ", popt)
    print("Covariance matrix  :\n", pcov)

    # Approximated curve
    fit_func =  func(x, popt[0], popt[1])

    # Score
    #R2 = 1- SSres/SStot
    residuals = y- func(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    R2 = 1 - (ss_res / ss_tot)
    print("R2: ", R2)


    fig,ax = plt.subplots(figsize=(10,5))
    # actual data
    ax.scatter(x, y, s=5, c='blue')

    #fitting curve
    ax.scatter(x, fit_func, c='red')

    ax.set_title( 'Delta Ore vs ACTUAL_ORE Fitting', size=14, fontweight='bold')
    ax.set_xlabel(colNames[0], size=12, fontweight='bold', labelpad=15)
    ax.set_ylabel(colNames[1], size=12, fontweight='bold', labelpad=15)

    xStr = str(colNames[1])
    yStr = 'fitted curve'
    ax.legend([xStr, yStr], loc='lower left', fontsize=10)
    st.pyplot(fig)
    #st.line_chart(df[['delta_temp','delta_C']])

    #st.write(df[['delta_temp','delta_C']])
    # fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    # ax[0].hist(df['delta_temp'], bins=30, color='skyblue', edgecolor='black')
    # ax[0].set_title('Histogram of Delta Temp')
    # ax[0].set_xlabel('Delta Temp')
    # ax[0].set_ylabel('Frequency')
    # ax[0].axvline(Temp_Range_Start, color='red', linestyle='dashed', linewidth=1)
    # ax[0].axvline(Temp_Range_end, color='red', linestyle='dashed', linewidth=1)
    # ax[1].hist(df['delta_C'], bins=30, color='lightgreen', edgecolor='black')
    # ax[1].set_title('Histogram of Delta C')
    # ax[1].set_xlabel('Delta C')
    # ax[1].set_ylabel('Frequency')
    # ax[1].axvline(Carbon_Range_Start, color='red', linestyle='dashed', linewidth=1)
    # ax[1].axvline(Carbon_Range_end, color='red', linestyle='dashed', linewidth=1)
    # plt.tight_layout()
    # st.pyplot(fig)
     # Filter data based on slider values
     #performance data evaluation
    # performance_data_Temp = df[(df['delta_temp'] >= Temp_Range_Start) & (df['delta_temp'] <= Temp_Range_end)].count()/df.count()
    # performance_data_C = df[(df['delta_C'] >= Carbon_Range_Start) & (df['delta_C'] <= Carbon_Range_end)].count()/df.count()
    # performance_data_C_Temp = df[(df['delta_temp'] >= Temp_Range_Start) & (df['delta_temp'] <= Temp_Range_end) & (df['delta_C'] >= Carbon_Range_Start) & (df['delta_C'] <= Carbon_Range_end)].count()/df.count()
    # st.write(f"Performance within Delta Temp range ({Temp_Range_Start}, {Temp_Range_end}): {performance_data_Temp['delta_temp']:.2%}")
    # st.write(f"Performance within Delta C range ({Carbon_Range_Start}, {Carbon_Range_end}): {performance_data_C['delta_C']:.2%}")
    # st.write(f"Performance within both Delta Temp and Delta C ranges: {performance_data_C_Temp['delta_C']:.2%}")    



if st.session_state.get('df') is not None:
    df = st.session_state.df
    
    st.title("Iron Ore amount increase Value Analysis")
    st.write("This page to make statics analysis for Iron Ore amount increase from the uploaded data, energy balance tunning.")
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
        ModelPerformanceIronOreValue(filtered_data)    
    
else:
    st.write("Please upload a JSON file on the main page to analyze performance values.")    
 