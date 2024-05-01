import os
import numpy as np
import pandas as pd

###########################################################################
# CODE DESCRIPTION
# 16_Compute_Extract_NOAA_RepFF.py extracts the flash flood reports from the NOAA 
# database, and manipulates the raw data to make it suitable for subsequent analysis:
#     - eliminates reports with no lat/lon coordinates or reporting date/time;
#     - indentify the flash flood affected areas: two new columns are created:
#        "AREA_AFFECTED_CENTRE_LAT", "AREA_AFFECTED_CENTRE_LON";
# Runtime: the code takes up to 2 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in the YYYY format): start year to consider.
# Year_F (integer, in the YYYY format): final year to consider.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the raw NOAA's reports.
# DirOUT (string): relative path of the directory containing the extracted flash flood reports.

# INPUT PARAMETERS
Year_S = 1950
Year_F = 2023
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Raw/OBS/NOAA_RepFF"
DirOUT = "Data/Compute/16_Extract_NOAA_RepFF"
###########################################################################


# Setting the main input/output directories
MainDirIN = Git_Repo + "/" + DirIN
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)

# Creating the variables where to store the total number of reports per year
years_rep = []
num_rep_all = []
num_rep_ff = []
num_rep_ff_withCoord = []

# Post-processing the raw flood reports
print("Creating the cleaned and merged flash flood report database. Post-processing the reports for: ")
ff_withCoord_all = pd.DataFrame()

for Year in range(Year_S, Year_F+1):
      
    print(" - " + str(Year))
    
    # Reading the raw flood reports
    string2find = "d" + str(Year) + "_"
    FileIN = [f for f in os.listdir(MainDirIN) if string2find in f and os.path.isfile(os.path.join(MainDirIN, f))]
    df = pd.read_csv(Git_Repo + "/" + DirIN + "/" + FileIN[0], low_memory=False)
    num_rows_all = df.shape[0]

    # Extracting reports for flash floods and removing reports with no lat/lon coordinates or no reporting date/time
    ff = df[df["EVENT_TYPE"].isin(["Flash Flood", "Flood", "Heavy Rain", "Hurricane/Typhoon", "Tropical Storm"])] # include also perhaps "Flood", "Heavy Rain", "Hurricane/Typhoon", "Tropical Storm"
    ff = ff.reset_index(drop=True)  # to reset the indexes of the new dataframe
    num_rows_ff = ff.shape[0]
    ff_withCoord = ff.dropna(subset=["BEGIN_DATE_TIME", "END_DATE_TIME", "BEGIN_LAT", "BEGIN_LON", "END_LAT", "END_LON"])
    ff_withCoord = ff_withCoord.reset_index(drop=True)  # to reset the indexes of the new dataframe
    num_rows_ff_withCoord = ff_withCoord.shape[0]
    
    # Storing the total number of reports per year
    years_rep.append(Year)
    num_rep_all.append(num_rows_all)
    num_rep_ff.append(num_rows_ff)
    num_rep_ff_withCoord.append(num_rows_ff_withCoord)

    # Creating the cleaned and merged flash flood report database
    if num_rows_ff_withCoord != 0:
 
        # Extracting the reports' lat/lon coordinates
        begin_lat = ff_withCoord["BEGIN_LAT"].to_numpy()
        begin_lon = ff_withCoord["BEGIN_LON"].to_numpy()
        end_lat = ff_withCoord["END_LAT"].to_numpy()
        end_lon = ff_withCoord["END_LON"].to_numpy()

        # Computing the lat/lon coordinates of the centre's area affected, and adding the column to the dataframe
        area_affected_centre_lat = np.round((begin_lat + end_lat) / 2, decimals = 4)
        area_affected_centre_lon = np.round( ( (begin_lon + end_lon) / 2 ) + 360, decimals = 4)  
        ff_withCoord.loc[:, "AREA_AFFECTED_CENTRE_LAT"] = area_affected_centre_lat
        ff_withCoord.loc[:, "AREA_AFFECTED_CENTRE_LON"] = area_affected_centre_lon

        # Extract all the rows from certain columns to streamline the dataset
        reduced_ff_withCoord = ff_withCoord[["EVENT_ID", "STATE", "CZ_TIMEZONE", "SOURCE", "EVENT_TYPE", "FLOOD_CAUSE", "BEGIN_DATE_TIME", "END_DATE_TIME", "BEGIN_LAT", "BEGIN_LON", "END_LAT", "END_LON", "AREA_AFFECTED_CENTRE_LAT", "AREA_AFFECTED_CENTRE_LON"]]

        # Merging the reports from all the years
        ff_withCoord_all = pd.concat([ff_withCoord_all, reduced_ff_withCoord], ignore_index=True)

# Saving the database with only flash flood reports and some metadata
FileOUT = MainDirOUT + "/RepFF.csv"
ff_withCoord_all.to_csv(FileOUT, index=False)

FileOUT = MainDirOUT + "/Years"
np.save(FileOUT, years_rep)

FileOUT = MainDirOUT + "/Counts_RepALL"
np.save(FileOUT, num_rep_all)

FileOUT = MainDirOUT + "/Counts_RepFF"
np.save(FileOUT, num_rep_ff)

FileOUT = MainDirOUT + "/Counts_RepFF_withCoord"
np.save(FileOUT, num_rep_ff_withCoord)