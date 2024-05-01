import os
import sys
from datetime import datetime, timedelta
import metview as mv

##########################################################################
# CODE DESCRIPTION
# 30_Plot_Prob_AccRepFF.py plots a map with the probabilities of having a flash flood 
# event in each grid-box.
# Runtime: the script can take up to 1 hour to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# DirIN (string): relative path of the directory containg the probabilities.
# DirOUT (string): relative path of the directory containg the map plots.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Name_Domain = "Central_East_Africa"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = sys.argv[2]
DirOUT = sys.argv[3]
##########################################################################


# Define the name of the considered training dataset (point data table, PDT)
DirOUT_Split = DirOUT.split("/")
Train_Split = DirOUT_Split[3].split("_")
if Train_Split[0] == "RedRndFF":
      Name_PDT = Train_Split[0] + "_" + DirOUT_Split[-1] + "_" + DirOUT_Split[-2] + "_" + Train_Split[1] + "_" + Train_Split[2]
else: 
      Name_PDT = Train_Split[0] + "_" + DirOUT_Split[-1] + "_" + Train_Split[1] + "_" + Train_Split[2]

print()
print("Plotting the probabilities of having a flash flood event at a grid-box for: " + Name_PDT)

TheDateTime_Start_S = datetime(Year, 1, 1, 0)
TheDateTime_Start_F = datetime(Year, 12, 31, 24-Disc_Acc)
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      # Reading the probabilities of having a flood report at each grid-box
      FileIN = Git_Repo + "/" + DirIN + "/Prob_AccRepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      Prob_AccRepFF = mv.read(FileIN)
      
      # Defining the plot titles
      ValidityDateS = TheDateTime_Start
      DayVS = ValidityDateS.strftime("%d")
      MonthVS = ValidityDateS.strftime("%B")
      YearVS = ValidityDateS.strftime("%Y")
      TimeVS = ValidityDateS.strftime("%H")
      ValidityDateF = TheDateTime_Final
      DayVF = ValidityDateF.strftime("%d")
      MonthVF = ValidityDateF.strftime("%B")
      YearVF = ValidityDateF.strftime("%Y")
      TimeVF = ValidityDateF.strftime("%H")
      
      title_plot1 = "Probability (%) of having a flash flood event within each grid-box"
      title_plot2 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          

      # Plotting the probabilities
      coastlines = mv.mcoast(
            map_coastline_colour = "charcoal",
            map_coastline_thickness = 2,
            map_coastline_resolution = "full",
            map_coastline_sea_shade = "on",
            map_coastline_sea_shade_colour = "rgb(0.665,0.9193,0.9108)",
            map_boundaries = "on",
            map_boundaries_colour = "evergreen",
            map_boundaries_thickness = 4,
            map_grid_latitude_increment = 10,
            map_grid_longitude_increment = 20,
            map_label_colour = "charcoal",
            map_grid_thickness = 1,
            map_grid_colour = "charcoal",
            map_label_height = 0.7
            )

      geo_view = mv.geoview(
            map_area_definition = "corners",
            area = [-20,15,20,60],
            coastlines = coastlines
            )

      contouring = mv.mcont(
            legend = "on", 
            contour = "off", 
            contour_level_selection_type = "level_list",
            contour_level_list = [0, 0.2, 0.4, 0.6, 0.8, 1, 3, 5, 7, 10, 100],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_technique = "grid_shading",
            contour_shade_colour_method = "list",
            contour_shade_colour_list = [
                  "rgb(0.8,0.8,0.8)", # 0 - 0.2
                  "rgb(0.7,0.7,0.7)", # 0.2 - 0.4
                  "rgb(0.6,0.6,0.6)", # 0.4 - 0.6
                  "rgb(0.5,0.5,0.5)", # 0.6 - 0.8
                  "rgb(0.4,0.4,0.4)", # 0.8 - 1
                  "rgb(0.9562,0.5968,0.7765)", # 1 -3
                  "rgb(1,0,0.498)", # 3 - 5
                  "rgb(0.5654,0.5043,0.9624)", # 5 - 7
                  "rgb(0.1451,0,1)", # 7 - 10
                  "rgb(0.749,0.5765,0.07451)" # 10 - 100
                  ]
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
            text_font_size = 0.7
            )

      # Saving the plot
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Name_Domain
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/Prob_AccRepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H")
      png = mv.png_output(output_width = 5000, output_name = FileOUT)
      mv.setoutput(png)
      mv.plot(Prob_AccRepFF, geo_view,  contouring, legend, title)

      TheDateTime_Start = TheDateTime_Start + timedelta(hours = Disc_Acc)