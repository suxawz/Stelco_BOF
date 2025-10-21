import pandas as pd
import json
import ExportClasses as EC
import glob
import os
import math

import time
from datetime import datetime, timedelta

def safe_json_to_df(json_data):
    """
    Transfer json data to pandas dataframe
    """
    try:
        # 尝试直接转换
        df = pd.DataFrame(json_data)
    except ValueError:
        # 处理混合类型数据
        df = pd.DataFrame(
            {k: [v] if isinstance(v, (int, float, str)) else v 
             for k, v in json_data.items()},
            index=range(max(len(v) for v in json_data.values()))
        )
    return df
def readJsonfile(folder_path):
    """
    Read all execute all json file in folder.
    """
    import chardet
    json_files = glob.glob(os.path.join(folder_path, '*.json'))
    # print(json_files[0]) 
    # with open(json_files[0], 'rb') as f:
    #     content = f.read()
    #     encoding = chardet.detect(content)['encoding']
    #     print(encoding)
    # 正确方式：使用文件对象
    df_list = []
    for file in json_files:
        with open(file, 'r',encoding='UTF-8-SIG') as f:
            data = json.load(f)  # 注意是load()不是loads()
            df = safe_json_to_df(data)
            df_list.append(df)
            #print(df)
    df_merged = pd.concat(df_list, ignore_index=True)
    return df_merged
def add_seconds_to_timestr(time_str, seconds, input_format="%Y-%m-%d %H:%M:%S", output_format=None):
    """
    字符串时间戳添加秒数（支持常见时间格式）
    :param time_str: 时间字符串 如 "2023-01-01 12:00:00"
    :param seconds: 要添加的秒数（可正可负）
    :param input_format: 输入时间格式，默认ISO格式
    :param output_format: 输出时间格式，默认与input_format相同
    :return: 新时间字符串
    """
    if output_format is None:
        output_format = input_format
        
    dt = datetime.strptime(time_str, input_format)
    new_dt = dt + timedelta(seconds=seconds)
    return new_dt.strftime(output_format)
def get_series_Aims(df_SteelGrade,GradeName):
    ListElements = ['C','Si','Mn','P','S','Al','Cu']
    series_Aims_data = []
    df_Result = df_SteelGrade.loc[df_SteelGrade['GradeNumber'] == GradeName]
   
    for index, row in df_Result.iterrows():
        for Element in ListElements:
            Aims = EC.Aims()
            Aims.Element = Element
            Name = Element + 'InternalAim'
            Aims.Aim = row[Name]
            Name = Element + 'InternalMax'
            Aims.Max = row[Name]
            Name = Element + 'InternalMin'
            Aims.Min = row[Name]
            series_Aims_data.append(Aims)   
    return series_Aims_data


def get_series_wastegas(df_CyclicTrend,HeatID,StartTime,EndTime):
    series_WasteGase_data = []
    cyclic_delta = 10
    vessel_no = 1
    if(str(HeatID)[0:1] == '8'):
        vessel_no=2 

    if( EndTime == None):
        if(StartTime == None):
            return series_WasteGase_data
        else:
            EndTime = add_seconds_to_timestr(StartTime,1200)
    else:
        if(StartTime == None):
            StartTime = add_seconds_to_timestr(EndTime,-1200)     
        

        
        # print(datatime)
        # print(EndTime)
        #df_Result = df_CyclicTrend[df_CyclicTrend['TimestampLocal'].between(datatime,add_seconds_to_timestr(datatime,cyclic_delta)) and df_CyclicTrend['Path'].str.contains('^BOF{vessel_no}')]
    mask_time = df_CyclicTrend['TimestampLocal'].between(StartTime,EndTime )
    df_Result = df_CyclicTrend[mask_time]

    for index, row in df_Result.iterrows():
        wastegas_record = EC.Series_WasteGas()
        Analysis_WG = EC.Analysis_perc()
        wastegas_record.TimeStamp = row['TimestampLocal'] 
        if(vessel_no ==1):
            wastegas_record.Flow_m3nperH = row['BOF1OFFGASFlow']   
            wastegas_record.Temperature_C = row['BOF1OFFGASTemp']   
            Analysis_WG.CO = row['BOF1OFFGASCO'] 
            Analysis_WG.CO2 = row['BOF1OFFGASCO2']    
            Analysis_WG.O2 = row['BOF1OFFGASO2']   
        else:
            wastegas_record.Flow_m3nperH = row['BOF2OFFGASFlow']   
            wastegas_record.Temperature_C = row['BOF2OFFGASTemp']   
            Analysis_WG.CO = row['BOF2OFFGASCO'] 
            Analysis_WG.CO2 = row['BOF2OFFGASCO2']    
            Analysis_WG.O2 = row['BOF2OFFGASO2']    
        wastegas_record.Analysis_perc = Analysis_WG              
        series_WasteGase_data.append(wastegas_record)
    return  series_WasteGase_data
       
def json_to_classes(df_Performance,df_CyclicTrend,df_SteelGrade):
    """
    Construce the class based on the Df data.
    parameters:
    df_Performance: base value 
    df_CyclicTrend:cyclic data block 
    df_SteelGrade:steel grade definition
    """
    heats_list = []
    for heat_data_Performance in df_Performance.itertuples(index = True,name = 'pandas'):
        
        heatInfo = EC.HeatInfo(
            BOFCalculationID=heat_data_Performance.BOFCalculationID,
            TreatmentStartTime=heat_data_Performance.CalculationTime,
            HeatID=heat_data_Performance.HeatNumber,
            Cast_ID=heat_data_Performance.ModelCastingLadle
        )
        series_Aim_data = get_series_Aims(df_SteelGrade,heat_data_Performance.Grade)
        grade = EC.Grade(GradeNumber=heat_data_Performance.Grade,SteelGrade=heat_data_Performance.Grade,Description=None,Aims=series_Aim_data)
        aim = EC.Aim(
            Grade=grade,
            CarbonAfterBlowing_perc=heat_data_Performance.AimAnalEOBC,
            CarbonAtTapping_perc=heat_data_Performance.AimC,
            PhosphorusAtTapping_perc=heat_data_Performance.AimP,
            Temperature_C=heat_data_Performance.AimtempEOB
        )
        analysis_perc = EC.Analysis_perc(
            C=heat_data_Performance.HotMetalC,
            Si=heat_data_Performance.HotMetalSi,
            #Mn=analysis_perc_data['Mn'],
            P=heat_data_Performance.HotMetalP,
            #S=analysis_perc_data['S']
        )
        hotMetal = EC.HotMetal(
            Temperature_C=heat_data_Performance.HotMetalTemp,
            Weight_kg=heat_data_Performance.ActHotMetalWeight,
            Analysis_perc=analysis_perc
        )
        
        scrap = EC.Scrap(SumWeight_kg=heat_data_Performance.ActTotal,
                         HomeScrap=EC.HomeScrap(heat_data_Performance.ActHomeScrap),
                         PAnds=EC.PAnds(heat_data_Performance.ActPAndS),
                         PitScrap=EC.PitScrap(heat_data_Performance.ActPitScrap),
                         PrimeBundles=EC.PrimeBundles(heat_data_Performance.ActPrimeBundles),
                         Shred=EC.Shred(heat_data_Performance.ActShred),
                         SlabCrops=EC.SlabCrops(heat_data_Performance.ActSlabCrops)
                         )
        fluxes = EC.Fluxes(Lime=EC.Lime(Weight_kg=heat_data_Performance.ACTUAL_LIME),Dolomite=EC.Dolomite(Weight_kg=heat_data_Performance.ACTUAL_DOLO))

        input_obj = EC.Input(
            HotMetal=hotMetal,
            Scrap=scrap,
            Fluxes=fluxes
        )
        mix = EC.Mix(
            EC.Analysis_perc(
            C=heat_data_Performance.MixAnalysisC,
            Si=heat_data_Performance.MixAnalysisSi
            #Mn=analysis_perc_data['Mn'],
            #P=heat_data_Performance['HotMetalP'],
            #S=analysis_perc_data['S']
                            )
        )

        usage = EC.Usage(
            BlowingProfile=heat_data_Performance.BlowingProfileActive,
            MaterialTapping=heat_data_Performance.MaterialTappingActive,
            MaterialFlux=heat_data_Performance.MaterialFluxActive
        )
        Bomb = EC.Bomb(TimeStamp =heat_data_Performance.CeloxTempDateTime ,Temperature_C=heat_data_Performance.CeloxTemp,Oxygen_ppm=heat_data_Performance.CeloxOxygen,Carbon_perc=heat_data_Performance.CeloxCarbon)
        series_SampleAnalysis = EC.Series_SampleAnalysis(
            Mix=mix,
            Usage=usage,
            Bomb = Bomb
        )
        
        series_WasteGase_data = get_series_wastegas(df_CyclicTrend,heat_data_Performance.HeatNumber,heat_data_Performance.BlowStartTime,heat_data_Performance.CeloxTempDateTime)
        series_WasteGase =  series_WasteGase_data
        WasteGasEOB = EC.WasteGasEOB(
            OffgasAnalyzer=heat_data_Performance.OffgasAnalyzer,
            EOBCO=heat_data_Performance.EOBCO,
            EOBCO2=heat_data_Performance.EOBCO2,
            EOBO2Amount=heat_data_Performance.EOBO2AmountAct,
            EOBSwitchOffValueTarget=heat_data_Performance.EOBSwitchOffValueTargetAct,
            EOBSwitchOffValueLast= heat_data_Performance.EOBSwitchOffValueLastAct,
            EOBSwitchOffValue=heat_data_Performance.EOBSwitchOffValueAct,
            EOBDetectionLog=heat_data_Performance.EOBDetectionLogAct
        )
        actualData = EC.ActualData(
            Series_SampleAnalysis=series_SampleAnalysis,
            Series_WasteGas=series_WasteGase,
            WasteGasEOB=WasteGasEOB
        )
        materials = EC.Materials(
            Basicity=heat_data_Performance.PredBascy,
            HotMetal_kg=heat_data_Performance.ModelHotMetalWeight,
            Scrap_kg=heat_data_Performance.PredTotal,
            Ore_kg=heat_data_Performance.PRED_ORE,
            Lime_kg=heat_data_Performance.PRED_LIME,
            Dolomit_kg=heat_data_Performance.PRED_DOLO,
            Oxygen_m3=heat_data_Performance.OxygenVolumePred
        )
        WasteGasEOB = EC.WasteGasEOB(
            OffgasAnalyzer=heat_data_Performance.OffgasAnalyzer,
            EOBCO=heat_data_Performance.EOBCO,
            EOBCO2=heat_data_Performance.EOBCO2,
            EOBO2Amount=heat_data_Performance.EOBO2Amount,
            EOBSwitchOffValueTarget=heat_data_Performance.EOBSwitchOffValueTarget,
            EOBSwitchOffValueLast= heat_data_Performance.EOBSwitchOffValueLast,
            EOBSwitchOffValue=heat_data_Performance.EOBSwitchOffValue,
            EOBDetectionLog=heat_data_Performance.EOBDetectionLog
        )
        prediction = EC.Prediction(Materials=materials,WasteGasEOB=WasteGasEOB)
        modelParameter = EC.ModelParameter(Prediction=prediction)
        analysis_perc = EC.Analysis_perc(C=heat_data_Performance.SteelAnalysisC,P=heat_data_Performance.SteelAnalysisP)
        CrudeSteel = EC.CrudeSteel(Analysis_perc=analysis_perc)
        output_obj = EC.Output(CrudeSteel=CrudeSteel)
        heat = EC.Heats(
            MetaInfo=EC.MetaInfo(),
            HeatInfo=heatInfo,
            Aim=aim,
            Input=input_obj,
            Output = output_obj,
            ActualData=actualData,
            ModelParameter=modelParameter
        )
        heats_list.append(heat)
    return heats_list  
#### 
def getParameterEntries(df_ParametersMitrix,BOFModelParameterID):
    ParametersEntriesList = []
    df_Result = df_ParametersMitrix.loc[df_ParametersMitrix['BOFModelParameterID'] == BOFModelParameterID]
   
    for index, row in df_Result.iterrows():
        Entries = EC.Entries()
        Entries.BOFModelParameterMatrixID = row['BOFModelParameterMatrixID']
        Entries.Key1 = row["KEY1"]
        Entries.Key2 = row["KEY2"]
        Entries.Value = row["VALUE"]

        ParametersEntriesList.append(Entries)   
    return ParametersEntriesList

    
def json_to_Parametersclasses(df_Parameters,df_ParametersMitrix):
     ParametersList = []
     for Parameter in df_Parameters.itertuples(index = True,name = 'pandas'):
        ParameterEntries = getParameterEntries(df_ParametersMitrix,Parameter.BOFModelParameterID)
        Entries = EC.DynamicClass(a=None)
        Parameter = EC.Parameters(
            BOFModelParameterID=Parameter.BOFModelParameterID,
            Name=Parameter.PNAME,
            UnitgroupNumber=Parameter.UNITGROUP_NO,
            PracticeNumber=Parameter.PRAC_NO,
            Type=Parameter.TYPE,
            Value=Parameter.VALUE,
            IsActive=Parameter.INST_ACTV,
            IsDialog=Parameter.DIALOG_PARAM,
            Conversion=Parameter.CONV,
            Max=Parameter.MAX_VALUE,
            Min=Parameter.MIN_VALUE,
            Entries=ParameterEntries
        )
        Entries.Add(**{ Parameter.Name: Parameter})
        #parameter = {Parameter.Name,Parameter}
        ParametersList.append(Entries)
     return ParametersList  
def getMaterialGroupsEntries(df_MaterialMap,MaterialID):
    MaterialGroupEntriesList = []
    df_Result = df_MaterialMap.loc[df_MaterialMap['MaterialID'] == MaterialID]
   
    for index, row in df_Result.iterrows():

        MaterialGroupEntriesList.append(row["InternalName"])   
    return MaterialGroupEntriesList
def getMaterialAnalysis(df_MaterialElement,MaterialID):
    df_Result = df_MaterialElement.loc[df_MaterialElement['MaterialID'] == MaterialID]
    analysis = df_Result[["Name","Content"]]
    Entries = EC.DynamicClass(a=None)
    for index, row in analysis.iterrows():
       ElementName = row["Name"]
       Content = row["Content"]
       Entries.Add(**{ ElementName: Content})

    return Entries

def json_to_Materialclasses(df_MaterialMaster,df_MaterialMap,df_MaterialElement):
    MaterialsList = []
    for Material in df_MaterialMaster.itertuples(index = True,name = 'pandas'):
        GroupsEntries = getMaterialGroupsEntries(df_MaterialMap,Material.MaterialID)
        Materialanalysis = getMaterialAnalysis(df_MaterialElement,Material.MaterialID)
        MaterialItem = EC.Material(
            Material_ID=Material.MaterialID,
            IsAvailable=Material.Status,
            Groups=GroupsEntries,
            Type=Material.MaterialTypeID,
            ChemicalEfficiency_perc=Material.Yield,
            DisplayName=Material.Name,
            Description=Material.Description,
            Enthalpy_kJ_at1600C=Material.Enthalpy,
            Price=Material.Price,
            Density_kg_m3=Material.SpecificWeight,
            BulkDensity_kg_m3=Material.BulkWeight,
            BaseElement=Material.BasicElement,
            Analysis_perc=Materialanalysis
        )
        #parameter = {Parameter.Name,Parameter}
        MaterialsList.append(MaterialItem)
    return MaterialsList  

def json_to_dataframe(data):
    heats = json_to_classes(data)
    records = []
    for heat in heats:
        record = {
            "BOFCalculationID": heat.heatInfo.BOFCalculationID,
            "TreatmentStartTime": heat.heatInfo.TreatmentStartTime,
            "HeatID": heat.heatInfo.HeatID,
            "Cast_ID": heat.heatInfo.Cast_ID,
            "SteelGrade": heat.Aim.Grade.SteelGrade,
            "CarbonAfterBlowing_perc": heat.Aim.CarbonAfterBlowing_perc,
            "CarbonAtTapping_perc": heat.Aim.CarbonAtTapping_perc,
            "PhosphorusAtTapping_perc": heat.Aim.PhosphorusAtTapping_perc,
            "Temperature_C_Aim": heat.Aim.Temperature_C,
            "HotMetal_Temperature_C": heat.Input.HotMetal.Temperature_C,
            "HotMetal_C_perc": heat.Input.HotMetal.Analysis_perc.C,
            "HotMetal_Si_perc": heat.Input.HotMetal.Analysis_perc.Si,
            "HotMetal_Mn_perc": heat.Input.HotMetal.Analysis_perc.Mn,
            "HotMetal_P_perc": heat.Input.HotMetal.Analysis_perc.P,
            "HotMetal_S_perc": heat.Input.HotMetal.Analysis_perc.S
        }
        for idx, scrap in enumerate(heat.Input.Scrap_kg):
            record[f"Scrap_{idx+1}_Type"] = scrap.Type
            record[f"Scrap_{idx+1}_Weight_kg"] = scrap.Weight_kg
        for idx, ore in enumerate(heat.Input.Ore_kg):
            record[f"Ore_{idx+1}_Type"] = ore.Type
            record[f"Ore_{idx+1}_Weight_kg"] = ore.Weight_kg
        for idx, lime in enumerate(heat.Input.Lime_kg):
            record[f"Lime_{idx+1}_Type"] = lime.Type
            record[f"Lime_{idx+1}_Weight_kg"] = lime.Weight_kg
        for idx, dolomit in enumerate(heat.Input.Dolomit_kg):
            record[f"Dolomit_{idx+1}_Type"] = dolomit.Type
            record[f"Dolomit_{idx+1}_Weight_kg"] = dolomit.Weight_kg
        record.update({
            "Mix_Time_min": heat.ActualData.Series_SampleAnalysis.Mix.Time_min,
            "Mix_Carbon_perc": heat.ActualData.Series_SampleAnalysis.Mix.Carbon_perc,
            "Mix_Silicon_perc": heat.ActualData.Series_SampleAnalysis.Mix.Silicon_perc,
            "Mix_Manganese_perc": heat.ActualData.Series_SampleAnalysis.Mix.Manganese_perc,
            "Mix_Phosphorus_perc": heat.ActualData.Series_SampleAnalysis.Mix.Phosphorus_perc,
            "Mix_Sulfur_perc": heat.ActualData.Series_SampleAnalysis.Mix.Sulfur_perc,
            "Mix_Temperature_C": heat.ActualData.Series_SampleAnalysis.Mix.Temperature_C
        })
        for idx, blowing in enumerate(heat.ActualData.Series_SampleAnalysis.Usage.BlowingProfile):
            record[f"BlowingProfile_{idx+1}_Time_min"] = blowing.Time_min
            record[f"BlowingProfile_{idx+1}_TotalGas_Nm3"] = blowing.TotalGas_Nm3
            record[f"BlowingProfile_{idx+1}_O2_Nm3"] = blowing.O2_Nm3
            record[f"BlowingProfile_{idx+1}_N2_Nm3"] = blowing.N2_Nm3
            record[f"BlowingProfile_{idx+1}_Ar_Nm3"] = blowing.Ar_Nm3
            record[f"BlowingProfile_{idx+1}_H2O_Nm3"] = blowing.H2O_Nm3
            record[f"BlowingProfile_{idx+1}_CO2_Nm3"] = blowing.CO2_Nm3
        for idx, tapping in enumerate(heat.ActualData.Series_SampleAnalysis.Usage.MaterialTapping):
            record[f"MaterialTapping_{idx+1}_Time_min"] = tapping.Time_min
            record[f"MaterialTapping_{idx+1}_Type"] = tapping.Type
            record[f"MaterialTapping_{idx+1}_Weight_kg"] = tapping.Weight_kg
        for idx, flux in enumerate(heat.ActualData.Series_SampleAnalysis.Usage.MaterialFlux):
            record[f"MaterialFlux_{idx+1}_Time_min"] = flux.Time_min
            record[f"MaterialFlux_{idx+1}_Type"] = flux.Type
            record[f"MaterialFlux_{idx+1}_Weight_kg"] = flux.Weight_kg
        for idx, waste in enumerate(heat.ActualData.Series_WasteGase):
            record[f"WasteGase_{idx+1}_TimeStamp"] = waste.TimeStamp
            record[f"WasteGase_{idx+1}_Temperature_C"] = waste.Temperature_C
            record[f"WasteGase_{idx+1}_Flow_m3nperH"] = waste.Flow_m3nperH
            record[f"WasteGase_{idx+1}_CO2_perc"] = waste.CO2_perc
            record[f"WasteGase_{idx+1}_CO_perc"] = waste.CO_perc
            record[f"WasteGase_{idx+1}_H2_perc"] = waste.H2_perc
            record[f"WasteGase_{idx+1}_N2_perc"] = waste.N2_perc
            record[f"WasteGase_{idx+1}_O2_perc"] = waste.O2_perc
        record.update({
            "Materials_Basicity": heat.ModelParameter.Prediction.Materials.Basicity,
            "Materials_HotMetal_kg": heat.ModelParameter.Prediction.Materials.HotMetal_kg,
            "Materials_Scrap_kg": heat.ModelParameter.Prediction.Materials.Scrap_kg,
            "Materials_Ore_kg": heat.ModelParameter.Prediction.Materials.Ore_kg,
            "Materials_Lime_kg": heat.ModelParameter.Prediction.Materials.Lime_kg,
            "Materials_Dolomit_kg": heat.ModelParameter.Prediction.Materials.Dolomit_kg,
            "Materials_Oxygen_m3": heat.ModelParameter.Prediction.Materials.Oxygen_m3
        })
        records.append(record)
    df = pd.DataFrame(records)  
    return df
def replace_nan_with_none(obj):
    if isinstance(obj, dict):
        return {k: replace_nan_with_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan_with_none(item) for item in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj
def remove_null_properties(obj):
    if isinstance(obj, dict):
        return {k: remove_null_properties(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_null_properties(x) for x in obj]
    else:
        return obj 