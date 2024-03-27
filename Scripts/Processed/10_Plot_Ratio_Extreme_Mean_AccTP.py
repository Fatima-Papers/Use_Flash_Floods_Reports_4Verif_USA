import os
import sys
from datetime import datetime, timedelta
import metview as mv

##########################################################################################################
# CODE DESCRIPTION
# 10_Plot_Ratio_Extreme_Mean_AccTP.py plots the ratio between the extreme and the mean point-rainfall ERA5-ecPoint 
# reanalysis in each grid-box. The grid-boxes in which the return period class for the extreme is zero are masked out.
# Runtime: the code takes up to 60 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the US mask is stored.
# DirIN_ClassRP (string): relative path of the directory containing the return period class for the extreme rainfall.
# DirIN_Ratio (string): relative path of the directory containing the ratio between the extreme and the mean ERA5-ecPoint rainfall.
# DirOUT (string): relative path of the directory containing the plots of the return period class.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN_ClassRP = "Data/Compute/07_ClassRP_AccTP"
DirIN_Ratio = "Data/Compute/09_Ratio_Extreme_Mean_AccTP"
DirOUT = "Data/Plot/10_Ratio_Extreme_Mean_AccTP"
##########################################################################################################


# Reading US mask
print("Reading the US domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Plotting the return period class for the extreme accumulated rainfall from ERA5-ecPoint.
print()
print("Computing the return period class for the extreme  " +  f"{Acc:02}" + "-hourly rainfall from ERA5-ecPoint, ending:")
TheDateTime_Final_S = datetime(Year, 1, 1, 12)
TheDateTime_Final_F = datetime(Year+1, 1, 1, 0)
TheDateTime_Final = TheDateTime_Final_S
while TheDateTime_Final <= TheDateTime_Final_F:

      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")

      # Reading the return period class, and mask the zero return period class (corresponding to very small rainfall values)
      FileIN_ClassRP = Git_Repo + "/" + DirIN_ClassRP + "/" + TheDateTime_Final.strftime("%Y%m") + "/ClassRP_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      classRP = mv.read(FileIN_ClassRP)
      classRP_bitmap = mv.bitmap(classRP, 0)

      # Reading the ratios, and masking the grid-boxes with zero return period class. Masking also the US domain
      FileIN_Ratio = Git_Repo + "/" + DirIN_Ratio + "/" + TheDateTime_Final.strftime("%Y%m") + "/Ratio_" + f"{Acc:02}" + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      ratio = mv.read(FileIN_Ratio)
      ratio_bitmap = mv.bitmap(ratio, classRP_bitmap)
      ratio_mask = mv.bitmap(ratio_bitmap, mask)

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
            
      # Plot the ratios
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
            contour_level_list = [0, 0.9, 1.1, 2, 3, 5, 10, 20, 1000],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_technique = "grid_shading",
            contour_shade_colour_list = [
                  "rgb(0.7,0.7,0.7)", # 0-0.9
                  "rgb(0,0,1)", # 0.9-1.1
                  "rgb(0.947,0.7673,0.7314)", # 1.1-2
                  "rgb(0.7927,0.8991,0.4734)", # 2-3
                  "rgb(0,0.2667,0.5333)", # 3-5
                  "rgb(0.8667,0.6667,0.2)", # 5-10
                  "rgb(0.7333,0.3333,0.4)", # 10-20
                  "black"] # 20-1000
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font_size = 0.5,
            )

      title = mv.mtext(
        text_line_count = 3,
        text_line_1 = "Ratio between extreme and mean rainfall [-]",
        text_line_2 = title_plot2,
        text_line_3 = " ",
        text_colour = "charcoal",
        text_font_size = 0.75
        )

      # Saving the plot
      MainDirOUT = Git_Repo + "/" + DirOUT  + "/" + TheDateTime_Final.strftime("%Y%m")
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT +"/Ratio_" + str(Acc) + "h_" + TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
      png = mv.png_output(output_width = 5000, output_name = FileOUT)
      mv.setoutput(png)
      mv.plot(geo_view, ratio_mask, contouring, legend, title)

      TheDateTime_Final = TheDateTime_Final + timedelta(hours = Disc_Acc)