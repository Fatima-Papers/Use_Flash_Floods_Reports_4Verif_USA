import os
from datetime import datetime, timedelta
import metview as mv

##############################################################################################################################################
# CODE DESCRIPTION
# 01_Compute_Percentage_Soil_Saturation.py computes the percentage to soil saturation for the top 1m level.
# Runtime: the code takes up to several hours to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Git_Repo (string): repository's local path
# DirIN (string): relative path containing the volumetric soil water for levels 1 (0-7cm), 2(7-28cm), and 3(28-100cm).
# DirOUT (string): relative path containing the percentage to soil saturation.

# INPUT PARAMETERS
DateTime_Start_S = datetime(2016,1,1,0)
DateTime_Start_F = datetime(2022,12,31,12)
Acc = 12
Disc_Acc = 12
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Raw/Analysis/ERA5_Land"
DirOUT = "Data/Compute/01_Percentage_Soil_Saturation"
##############################################################################################################################################

# Retrieving the soil type
print("Retrieving the soil type ...")
soil_type = mv.retrieve(
    {"class" : "od",
     "stream" : "enfo", 
     "type" : "cf", 
     "expver" : "1", 
     "levtype" : "sfc",
     "param" : "43.128",
    })

soil_type = mv.bitmap(soil_type, 0) # sostitute the zeros for the sea with missing values to avoid dividing by zero

# Calculating the fields of maximum saturation, field capacity and permanent wilting point using the new soil hydrology scheme (obtained from: https://confluence.ecmwf.int/pages/viewpage.action?pageId=121839768)
soil_type_codes = [1, 2, 3, 4, 5, 6, 7]
pwp = [0.059, 0.151, 0.133, 0.279, 0.335, 0.267, 0.151] # permanent wilting point
fc = [0.242, 0.346, 0.382, 0.448, 0.541, 0.662, 0.346] # field capacity
sat = [0.403, 0.439, 0.430, 0.520, 0.614, 0.766, 0.472] # maximum saturation
pwp_field = ( (soil_type == soil_type_codes[0]) * pwp[0] ) + ( (soil_type == soil_type_codes[1]) * pwp[1] ) + ( (soil_type == soil_type_codes[2]) * pwp[2] ) + ( (soil_type == soil_type_codes[3]) * pwp[3] ) + ( (soil_type == soil_type_codes[4]) * pwp[4] ) + ( (soil_type == soil_type_codes[5]) * pwp[5] ) + ( (soil_type == soil_type_codes[6]) * pwp[6] )
fc_field = ( (soil_type == soil_type_codes[0]) * fc[0] ) + ( (soil_type == soil_type_codes[1]) * fc[1] ) + ( (soil_type == soil_type_codes[2]) * fc[2] ) + ( (soil_type == soil_type_codes[3]) * fc[3] ) + ( (soil_type == soil_type_codes[4]) * fc[4] ) + ( (soil_type == soil_type_codes[5]) * fc[5] ) + ( (soil_type == soil_type_codes[6]) * fc[6] )
sat_field = ( (soil_type == soil_type_codes[0]) * sat[0] ) + ( (soil_type == soil_type_codes[1]) * sat[1] ) + ( (soil_type == soil_type_codes[2]) * sat[2] ) + ( (soil_type == soil_type_codes[3]) * sat[3] ) + ( (soil_type == soil_type_codes[4]) * sat[4] ) + ( (soil_type == soil_type_codes[5]) * sat[5] ) + ( (soil_type == soil_type_codes[6]) * sat[6] )

# Computing the levels of moisture content in the soil
TheDateTime_Start = DateTime_Start_S
print("Computing the percentage to soil saturation for the accumulation period ending on:")
while TheDateTime_Start <= DateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
      
      # Read the volumetric soil water for level 1 (0 - 7 cm)
      swvl = "swvl1"
      FileIN_start_1 = Git_Repo + "/" + DirIN + "/" + swvl + "/" + TheDateTime_Start.strftime("%Y") + "/" + TheDateTime_Start.strftime("%Y%m%d") + "/" + swvl + "_" + TheDateTime_Start.strftime("%Y%m%d") + "_" + TheDateTime_Start.strftime("%H") + ".grib"
      FileIN_final_1 = Git_Repo + "/" + DirIN + "/" + swvl + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/" + swvl + "_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      swvl1 = ( mv.read(FileIN_start_1) + mv.read(FileIN_final_1) ) / 2
     
      # Read the volumetric soil water for level 2 (7 - 28 cm)
      swvl = "swvl2"
      FileIN_start_2 = Git_Repo + "/" + DirIN + "/" + swvl + "/" + TheDateTime_Start.strftime("%Y") + "/" + TheDateTime_Start.strftime("%Y%m%d") + "/" + swvl + "_" + TheDateTime_Start.strftime("%Y%m%d") + "_" + TheDateTime_Start.strftime("%H") + ".grib"
      FileIN_final_2 = Git_Repo + "/" + DirIN + "/" + swvl + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/" + swvl + "_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      swvl2 = ( mv.read(FileIN_start_2) + mv.read(FileIN_final_2) ) / 2
      
      # Read the volumetric soil water for level 3 (28 - 100 cm)
      swvl = "swvl3"
      FileIN_start_3 = Git_Repo + "/" + DirIN + "/" + swvl + "/" + TheDateTime_Start.strftime("%Y") + "/" + TheDateTime_Start.strftime("%Y%m%d") + "/" + swvl + "_" + TheDateTime_Start.strftime("%Y%m%d") + "_" + TheDateTime_Start.strftime("%H") + ".grib"
      FileIN_final_3 = Git_Repo + "/" + DirIN + "/" + swvl + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/" + swvl + "_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      swvl3 = ( mv.read(FileIN_start_3) + mv.read(FileIN_final_3) ) / 2
      
      # Integrating the volumetric soil water for the top 1m
      swvl = (swvl1*(7-0)/100) + (swvl2*(28-7)/100) + (swvl3*(100-28)/100)
      
      # Defining the water content in the soil (in percentage)
      soil_saturation_perc = swvl / sat_field
      soil_saturation_perc = ((soil_saturation_perc >= 1) * 1) + ((soil_saturation_perc < 1) * soil_saturation_perc) # to correct the few spurious grid-boxes with values of soil moiture >= 1
      
      # Save the field
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") 
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/soil_saturation_perc_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
      mv.write(FileOUT, soil_saturation_perc)
      
      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)