import os
import sys
from datetime import datetime, timedelta
import metview as mv

####################################################################################
# CODE DESCRIPTION
# 08_Plot_ClassRP_AccTP.py plots the return period class for the 99th percentile of  
# accumulated rainfall from ERA5-ecPoint.
# Runtime: the code takes up to 60 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the US mask is stored.
# DirIN (string): relative path of the directory containing the return period class for the extreme rainfall.
# DirOUT (string): relative path of the directory containing the plots of the return period class.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/07_ClassRP_AccTP"
DirOUT = "Data/Plot/08_ClassRP_AccTP"
####################################################################################


# Reading US mask
print("Reading the US domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Defining the accumulation periods to consider
TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 24-Disc_Acc)

# Plotting the return period class for the extreme accumulated rainfall from ERA5-ecPoint.
print()
print("Computing the return period class for the extreme  " +  f"{Acc:02}" + "-hourly rainfall from ERA5-ecPoint, ending:")
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

    TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
    print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

    # Reading the return period class, and mask the US domain
    FileIN = Git_Repo + "/" + DirIN + "/" + TheDateTime_Final.strftime("%Y%m") + "/ClassRP_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
    classRP = mv.read(FileIN)
    classRP_mask = mv.bitmap(classRP, mask)

    # Defining the forecasts' valid times
    ValidityDateS = TheDateTime_Final - timedelta(hours=Acc)
    DayVS = ValidityDateS.strftime("%d")
    MonthVS = ValidityDateS.strftime("%B")
    YearVS = ValidityDateS.strftime("%Y")
    TimeVS = ValidityDateS.strftime("%H")
    ValidityDateF = TheDateTime_Final
    DayVF = ValidityDateF.strftime("%d")
    MonthVF = ValidityDateF.strftime("%B")
    YearVF = ValidityDateF.strftime("%Y")
    TimeVF = ValidityDateF.strftime("%H")
    title_plot2 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          
            
    # Plotting the return period class
    coastlines = mv.mcoast(
        map_coastline_colour = "charcoal",
        map_coastline_thickness = 2,
        map_coastline_resolution = "full",
        map_coastline_sea_shade = "on",
        map_coastline_sea_shade_colour = "rgb(0.665,0.9193,0.9108)",
        map_boundaries = "on",
        map_boundaries_colour = "charcoal",
        map_boundaries_thickness = 2,
        map_grid_latitude_increment = 10,
        map_grid_longitude_increment = 20,
        map_label_right = "off",
        map_label_top = "off",
        map_label_colour = "charcoal",
        map_grid_thickness = 1,
        map_grid_colour = "charcoal",
        map_label_height = 0.7
        )

    geo_view = mv.geoview(
        map_projection = "epsg:3857",
        map_area_definition = "corners",
        area = Mask_Domain,
        coastlines = coastlines
        )

    contouring = mv.mcont(
        legend = "on", 
        contour = "off",
        contour_level_selection_type = "level_list",
        contour_level_list = [0.1, 1.1, 2.1, 5.1, 10.1, 20.1],
        contour_label = "off",
        contour_shade = "on",
        contour_shade_technique = "grid_shading",
        contour_shade_colour_method = "list",
        contour_shade_colour_list = [
            "rgb(0.251,0.4314,0.702)", # RP1 - RP2
            "rgb(1,0.8549,0)", # RP2 - RP5
            "rgb(1,0,0.498)", # RP5 - RP10
            "rgb(0.1418,0.678,0.05927)", # RP10 - RP20
            "rgb(0.5329,0.173,0.299)" # > RP20
            ]
        )

    legend = mv.mlegend(
        legend_text_colour = "charcoal",
        legend_text_font_size = 0.5,
        legend_display_type = "disjoint",
        legend_text_composition = "user_text_only",
        legend_user_lines = ["1-2","2-5","5-10","10-20",">20"],
        legend_entry_text_width = 50.00,
        )

    title = mv.mtext(
        text_line_count = 3,
        text_line_1 = "Return Period Class [years]",
        text_line_2 = title_plot2,
        text_line_3 = " ",
        text_colour = "charcoal",
        text_font_size = 0.75
        )

    # Saving the plot
    MainDirOUT = Git_Repo + "/" + DirOUT  + "/" + TheDateTime_Final.strftime("%Y%m")
    if not os.path.exists(MainDirOUT):
        os.makedirs(MainDirOUT)
    FileOUT = MainDirOUT +"/ClassRP_" + str(Acc) + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
    png = mv.png_output(output_width = 5000, output_name = FileOUT)
    mv.setoutput(png)
    mv.plot(geo_view, classRP_mask, contouring, legend, title)

    TheDateTime_Start = TheDateTime_Start + timedelta(hours = Disc_Acc)