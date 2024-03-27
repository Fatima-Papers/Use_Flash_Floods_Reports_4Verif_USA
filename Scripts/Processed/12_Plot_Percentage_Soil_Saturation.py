import os
import sys
from datetime import datetime, timedelta
import metview as mv

##############################################################################################
# CODE DESCRIPTION
# 12_Plot_Percentage_Soil_Saturation.py plots the percentage to instantaneous soil saturation for the top 1m level.
# Runtime: the code takes up to 60 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year (integer, in YYYY format): year to consider.
# Disc_Time (integer, in hours): discretization for time.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the USA's mask is stored for ERA5_Land.
# DirIN (string): relative path containing the volumetric soil water for levels 1 (0-7cm), 2(7-28cm), and 3(28-100cm).
# DirOUT (string): relative path containing the percentage to soil saturation.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Disc_Time = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5_Land/Mask.grib"
DirIN = "Data/Compute/11_Percentage_Soil_Saturation"
DirOUT = "Data/Plot/12_Percentage_Soil_Saturation"
##############################################################################################

# Reading the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Plotting the percentage of soil saturation within the considered domain
print()
print("Computing and saving the percentage of soil saturation:")

DateTime_S = datetime(Year,1,1,0)
DateTime_F = datetime(Year,12,31,12)

TheDateTime = DateTime_S
while TheDateTime <= DateTime_F:

      print(" - on " + TheDateTime.strftime("%Y-%m-%d") + " at " + TheDateTime.strftime("%H") + " UTC")

      # Reading the percentage of soil saturation 
      FileIN = Git_Repo + "/" + DirIN + "/" + TheDateTime.strftime("%Y") + "/" + TheDateTime.strftime("%Y%m%d")  + "/soil_saturation_perc_" + TheDateTime.strftime("%Y%m%d%H") + ".grib"
      ss_perc = mv.read(FileIN)
      ss_perc_mask =  mv.bitmap(mask, 0) * ss_perc

      # Plotting the percentage of soil saturation 
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
            contour_level_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_colour_method = "list",
            contour_shade_method = "area_fill",
            contour_shade_colour_list = ["rgb(1,0.9333,0.8)","rgb(1,0.8667,0.6)","rgb(1,0.8,0.3333)","rgb(1,1,0)","rgb(0.3333,1,0)","rgb(0.2,0.6,0)","rgb(0.2,0.8667,0.7333)","rgb(0.2,0.6667,0.6667)","rgb(0.2,0.4667,0.6667)","rgb(0,0,1)"]
            )
      
      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font_size = 0.5,
            )

      title = mv.mtext(
            text_line_count = 3,
            text_line_1 = "Percentage of Soil Saturation [-]",
            text_line_2 = "on " + TheDateTime.strftime("%Y-%m-%d") + " at " + TheDateTime.strftime("%H") + " UTC",
            text_line_3 = " ",
            text_colour = "charcoal",
            text_font_size = 0.75
            )

      # Saving the plot
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + TheDateTime.strftime("%Y%m")
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)
      FileOUT = MainDirOUT + "/Percentage_Soil_Saturation_" + TheDateTime.strftime("%Y%m%d") + "_" + TheDateTime.strftime("%H")
      png = mv.png_output(output_width = 5000, output_name = FileOUT)
      mv.setoutput(png)
      mv.plot(geo_view, ss_perc_mask, contouring, legend, title)

      TheDateTime = TheDateTime + timedelta(hours=Disc_Time)