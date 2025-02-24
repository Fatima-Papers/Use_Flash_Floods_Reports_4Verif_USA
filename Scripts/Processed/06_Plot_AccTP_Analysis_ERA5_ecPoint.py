import os
import sys
from datetime import datetime, timedelta
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 06_Plot_AccTP_Analysis_ERA5_ecPoint.py plots the 99th percentile of rainfall from 
# ERA5-ecPoint over the considered accumulation period.
# Runtime: the code takes up to 90 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Perc (float, from 0 to 100): percentile to plot.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN (string): relative path of the directory containing the ERA5-ecPoint analysis.
# DirOUT (string): relative path of the directory containing the 99th percentile's plots.

# INPUT PARAMETERS
Year = 2024
#Year = int(sys.argv[1])
Acc = 12
Perc = 99
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Raw/Analysis/ERA5_ecPoint/tp"
DirOUT = "Data/Plot/06_AccTP_Analysis_ERA5_ecPoint"
###########################################################################


# Reading the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_vals = mv.values(mask)
mask_bitmap = mv.bitmap(mask, 0)

# Defining the period to consider
TheDate_S = datetime(Year,4,24)
TheDate_F = datetime(Year,4,24)

# Plotting the accumulated rainfall totals from ERA5_ecPoint analysis
print()
print("Plotting accumulated rainfall analysis from ERA5-ecPoint for the " + str() + "-hourly period ending:")
TheDate = TheDate_S
while TheDate <= TheDate_F:

      for EndPeriod in range(0+Acc, 24+1, Acc):

            TheDateTime_Final = TheDate + timedelta(hours=EndPeriod)
            print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

            tp = mv.read(Git_Repo + "/" + DirIN + "/Pt_BC_PERC/" + TheDate.strftime("%Y%m") + "/Pt_BC_PERC_" + TheDate.strftime("%Y%m%d") + "_" + "0" + str(EndPeriod) + ".grib2")
            tp_perc = tp[Perc-1]
            tp_perc_bitmap = mv.bitmap(tp_perc, mask_bitmap)

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
            title_plot1 = "ERA5-ecPoint " + str(Acc) + "-hourly tp (mm/" + str(Acc) + "h), " + str(Perc) + "th percentile"
            title_plot2 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          
            
            # Plot the rainfall climatology
            coastlines = mv.mcoast(
                  map_coastline_colour = "charcoal",
                  map_coastline_thickness = 2,
                  map_coastline_resolution = "full",
                  map_coastline_sea_shade = "on",
                  map_coastline_sea_shade_colour = "rgb(0.665,0.9193,0.9108)",
                  map_boundaries = "on",
                  map_boundaries_colour = "charcoal",
                  map_boundaries_thickness = 4,
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
                  contour_level_list = [0,0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500,5000],
                  contour_label = "off",
                  contour_shade = "on",
                  contour_shade_colour_method = "list",
                  contour_shade_method = "area_fill",
                  contour_shade_colour_list = ["white","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)","RGB(1,0.73,0.0039)","RGB(1,0.49,0.0039)","red","RGB(0.85,0.0039,1)","RGB(0.63,0.0073,0.92)","RGB(0.37,0.29,0.91)","RGB(0.04,0.04,0.84)","RGB(0.042,0.042,0.43)","RGB(0.45,0.45,0.45)"]
                  )

            legend = mv.mlegend(
                  legend_text_colour = "charcoal",
                  legend_text_font_size = 0.5,
                  )

            title = mv.mtext(
                  text_line_count = 3,
                  text_line_1 = title_plot1,
                  text_line_2 = title_plot2,
                  text_line_3 = " ",
                  text_colour = "charcoal",
                  text_font_size = 0.75
                  )

            # Saving the maps
            # DirOUT_temp = Git_Repo + "/" + DirOUT + "/" + TheDateTime_Final.strftime("%Y%m")
#             if not os.path.exists(DirOUT_temp):
#                   os.makedirs(DirOUT_temp)
#             FileOUT = DirOUT_temp + "/tp" + str(Acc) + "h_" + str(Perc) + "th_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H")
#             png = mv.png_output(output_width = 5000, output_name = FileOUT)
#             mv.setoutput(png)
            mv.plot(coastlines, tp_perc, contouring, legend, title)

      TheDate = TheDate + timedelta(days=1)