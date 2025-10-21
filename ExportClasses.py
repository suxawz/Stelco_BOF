import json
class Heats:
    def __init__(self,MetaInfo, HeatInfo,Aim,Input,Output,ActualData,ModelParameter):
        self.MetaInfo = MetaInfo
        self.HeatInfo = HeatInfo
        self.Aim = Aim
        self.Input = Input
        self.Output = Output
        self.ActualData = ActualData
        self.ModelParameter = ModelParameter
class MetaInfo:
    def __init__(self, FileVersion= '', PlantType = "BOF", Project="Stelco"):
        self.FileVersion = FileVersion
        self.PlantType = PlantType
        self.Project = Project
class  HeatInfo:
    def __init__(self, BOFCalculationID,TreatmentStartTime,HeatID,Cast_ID):
        self.BOFCalculationID = BOFCalculationID 
        self.TreatmentStartTime = TreatmentStartTime
        self.HeatID = HeatID
        self.Cast_ID = Cast_ID 
class Aim:
    def __init__(self, Grade, CarbonAfterBlowing_perc,CarbonAtTapping_perc,PhosphorusAtTapping_perc,Temperature_C,):
        self.Grade = Grade
        self.CarbonAfterBlowing_perc = CarbonAfterBlowing_perc
        self.CarbonAtTapping_perc = CarbonAtTapping_perc
        self.PhosphorusAtTapping_perc = PhosphorusAtTapping_perc
        self.Temperature_C = Temperature_C
class Grade:
    def __init__(self, GradeNumber,Description,SteelGrade,Aims):
        self.SteelGrade = SteelGrade 
        self.GradeNumber = GradeNumber
        self.Description = Description
        self.Aims = Aims
class Aims:
    def __init__(self,Element=None,Aim=None,Min=None,Max=None):
        self.Element = Element
        self.Aim = Aim
        self.Min = Min
        self.Max = Max
class Fluxes:
    def __init__(self,Lime,Dolomite):
        self.Lime = Lime
        self.Dolomite = Dolomite
class Lime:
    def __init__(self,Weight_kg):
        self.Weight_kg = Weight_kg     
class Dolomite:
    def __init__(self,Weight_kg):
        self.Weight_kg = Weight_kg             
class Input:
    def __init__(self, HotMetal, Scrap,Fluxes):
        self.HotMetal = HotMetal
        self.Scrap = Scrap
        self.Fluxes = Fluxes
class Output:
    def __init__(self,CrudeSteel):
        self.CrudeSteel = CrudeSteel
class CrudeSteel:
    def __init__(self,Analysis_perc):
        self.Analysis_perc = Analysis_perc                 
class HotMetal:
    def __init__(self, Temperature_C,Analysis_perc, Weight_kg):
        self.Temperature_C = Temperature_C
        self.Analysis_perc = Analysis_perc
        self.Weight_kg = Weight_kg
class Analysis_perc:
    def __init__(self, C=None, Si=None, Mn=None,P=None,S=None,CO2=None,CO=None,H2=None,N2=None,O2=None):
        self.C = C
        self.Si = Si
        self.Mn = Mn
        self.P = P
        self.S = S
        self.CO2 = CO2
        self.CO = CO
        self.H2 = H2
        self.N2 = N2
        self.O2 = O2
class Scrap:
    def __init__(self, SumWeight_kg,HomeScrap,PAnds,PitScrap,PrimeBundles,Shred,SlabCrops):
        self.SumWeight_kg = SumWeight_kg
        self.HomeScrap = HomeScrap  
        self.PAnds = PAnds
        self.PitScrap = PitScrap
        self.PrimeBundles = PrimeBundles
        self.Shred = Shred
        self.SlabCrops = SlabCrops
class HomeScrap:
    def __init__(self,Weight_kg):
        self.Weight_kg =   Weight_kg       
class PAnds:
    def __init__(self,Weight_kg):
        self.Weight_kg =   Weight_kg  
class PitScrap:
    def __init__(self,Weight_kg):
        self.Weight_kg =   Weight_kg  
class PrimeBundles:
    def __init__(self,Weight_kg):
        self.Weight_kg =   Weight_kg  
class Shred:
    def __init__(self,Weight_kg):
        self.Weight_kg =   Weight_kg  
class SlabCrops:
    def __init__(self,Weight_kg):
        self.Weight_kg =   Weight_kg          
class ActualData:
    def __init__(self, Series_SampleAnalysis, Series_WasteGas,WasteGasEOB):
        self.Series_SampleAnalysis = Series_SampleAnalysis
        self.Series_WasteGase = Series_WasteGas
        self.WasteGasEOB = WasteGasEOB
class Series_SampleAnalysis:
    def __init__(self, Mix,Usage,Bomb):
        self.Mix = Mix
        self.Usage = Usage
        self.Bomb = Bomb
class Usage:
    def __init__(self, BlowingProfile,MaterialTapping,MaterialFlux):
        self.BlowingProfile = BlowingProfile
        self.MaterialTapping = MaterialTapping
        self.MaterialFlux = MaterialFlux
class Mix:
    def __init__(self, Analysis_perc):
        self.Analysis_perc = Analysis_perc
class ModelParameter:
    def __init__(self, Prediction):
        self.Prediction = Prediction  
class Prediction:
    def __init__(self, Materials,WasteGasEOB):
        self.Materials = Materials
        self.WasteGasEOB = WasteGasEOB
class Materials:
    def __init__(self, Basicity,HotMetal_kg,Scrap_kg,Ore_kg,Lime_kg,Dolomit_kg,Oxygen_m3):
        self.Basicity = Basicity
        self.HotMetal_kg = HotMetal_kg
        self.Scrap_kg = Scrap_kg
        self.Ore_kg = Ore_kg
        self.Lime_kg = Lime_kg
        self.Dolomit_kg = Dolomit_kg
        self.Oxygen_m3 = Oxygen_m3
class Series_WasteGas:
    def __init__(self,TimeStamp=None, Temperature_C=None, Flow_m3nperH=None,Analysis_perc=None):
        self.TimeStamp = TimeStamp
        self.Temperature_C = Temperature_C
        self.Flow_m3nperH = Flow_m3nperH
        self.Analysis_perc = Analysis_perc
      
class Bomb:
    def __init__(self, TimeStamp, Temperature_C,Oxygen_ppm,Carbon_perc):
        self.TimeStamp = TimeStamp
        self.Temperature_C = Temperature_C
        self.Oxygen_ppm = Oxygen_ppm
        self.Carbon_perc = Carbon_perc                     
class WasteGasEOB:
    def __init__(self,OffgasAnalyzer,EOBO2Amount,EOBSwitchOffValue,EOBSwitchOffValueLast,EOBSwitchOffValueTarget,EOBCO,EOBCO2,EOBDetectionLog):
        self.OffgasAnalyzer = OffgasAnalyzer
        self.OffgasAnalyzer = OffgasAnalyzer
        self.EOBO2Amount = EOBO2Amount
        self.EOBSwitchOffValue = EOBSwitchOffValue
        self.EOBSwitchOffValueLast = EOBSwitchOffValueLast
        self.EOBSwitchOffValueTarget = EOBSwitchOffValueTarget
        self.EOBCO = EOBCO
        self.EOBCO2 = EOBCO2
        EOBDetectionLog = EOBDetectionLog
class Parameters:
    def __init__(self,BOFModelParameterID,Name,UnitgroupNumber,PracticeNumber,Type,Value,IsActive,IsDialog,Conversion,Max,Min,Entries):
        self.BOFModelParameterID = BOFModelParameterID
        self.Name = Name
        self.UnitgroupNumber = UnitgroupNumber
        self.PracticeNumber = PracticeNumber
        self.Type = Type
        self.Value = Value
        self.IsActive = IsActive
        self.IsDialog = IsDialog
        self.Conversion = Conversion
        self.Max = Max
        self.Min = Min
        self.Entries = Entries
class Entries:
    def __init__(self,BOFModelParameterID=None,Key1=None,Key2=None,Value=None):
        self.BOFModelParameterID = BOFModelParameterID
        self.Key1 =Key1
        self.Key2 = Key2
        self.Value = Value
class Material:
    def __init__(self,Material_ID=None,IsAvailable=None,Groups=None,Type=None,ChemicalEfficiency_perc=None,DisplayName=None,Description=None,Enthalpy_kJ_at1600C=None,Price=None,Density_kg_m3=None,BulkDensity_kg_m3=None,BaseElement=None,Analysis_perc=None):
        self.Material_ID =Material_ID
        self.IsAvailable =IsAvailable
        self.Groups = Groups
        self.Type = Type
        self.ChemicalEfficiency_perc = ChemicalEfficiency_perc
        self.DisplayName = DisplayName
        self.Description = Description
        self.Enthalpy_kJ_at1600C = Enthalpy_kJ_at1600C
        self.Price = Price
        self.Density_kg_m3 = Density_kg_m3
        self.BulkDensity_kg_m3 = BulkDensity_kg_m3
        self.BaseElement = BaseElement
        self.Analysis_perc = Analysis_perc
class DynamicClass:
    def __init__(self, **kwargs):
        #self.attributes = {}
        for key, value in kwargs.items():
            setattr(self, key, value)  # 使用setattr动态设置属性
            #self.attributes[key] = value  # 也可以存储在一个字典中
    def Add(self, **kwargs):
        #self.attributes = {}
        for key, value in kwargs.items():
            setattr(self, key, value)  # 使用setattr动态设置属性
            #self.attributes[key] = value  # 也可以存储在一个字典中        
# heats = Heats(
#     MetaInfo=MetaInfo(FileVersion="1.0"),
#     HeatInfo=HeatInfo(
#         BOFCalculationID=12345,
#         TreatmentStartTime="2023-10-01T12:00:00Z",
#         HeatID="H001",
#         Cast_ID="C001"
#     ),
#     Aim=Aim(
#         Grade=Grade(SteelGrade="A"),
#         CarbonAfterBlowing_perc=0.05,
#         CarbonAtTapping_perc=0.03,
#         PhosphorusAtTapping_perc=0.02,
#         Temperature_C=1600
#     ),
#     Input=Input(
#         HotMetal=HotMetal(
#             Temperature_C=1400,
#             Analysis_perc=Analysis_perc(C=4.5, Si=0.5, Mn=0.3, P=0.1, S=0.05),
#             Weight_kg=10000
#         ),
#         Scrap=Scrap(
#             Weight_kg=2000,
#             Type="TypeA"
#         )
#     ),
#     ActualData=ActualData(
#         Series_SampleAnalysis=Series_SampleAnalysis(
#             Mix=Mix(Analysis_perc=Analysis_perc(C=3.5, Si=0.4, Mn=0.2, P=0.08, S=0.03)),
#             Usage=Usage(
#                 BlowingProfile="Profile1",
#                 MaterialTapping="Material1",
#                 MaterialFlux="Flux1"
#             ),
#             Bomb=Bomb(
#                 TimeStamp="2023-10-01T12:30:00Z",
#                 Temperature_C=1500,
#                 Oxygen_ppm=50,
#                 Carbon_perc=2.5
#             )
#         ),
#         Series_WasteGas=[
#             Series_WasteGas(
#                 TimeStamp="2023-10-01T12:15:00Z",
#                 Temperature_C=1200,
#                 Flow_m3nperH=500,
#                 Analysis_perc=Analysis_perc(CO2=15, CO=20, H2=5, N2=50, O2=10)
#             ),
#             Series_WasteGas(
#                 TimeStamp="2023-10-01T12:30:00Z",
#                 Temperature_C=1250,
#                 Flow_m3nperH=550,
#                 Analysis_perc=Analysis_perc(CO2=16, CO=18, H2=6, N2=49, O2=11)
#             )   
#         ]
#     ),
#     ModelParameter=ModelParameter(
#         Prediction=Prediction(
#             Materials=Materials(
#                 Basicity=1.5,
#                 HotMetal_kg=10000,
#                 Scrap_kg=2000,
#                 Ore_kg=500,
#                 Lime_kg=300,
#                 Dolomit_kg=200,
#                 Oxygen_m3=1500
#             )
#         )
#     )
# )   
# json_data = json.dumps(heats, default=lambda o: o.__dict__, indent=4)
#print(json_data)