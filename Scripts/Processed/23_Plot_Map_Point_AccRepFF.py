import os
import sys
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import metview as mv

#####################################################################################
# CODE DESCRIPTION
# 23_Plot_Map_Point_AccRepFF.py creates map plots of the accumulated point flash flood reports over 
# specific accumulation periods.
# Runtime: The code takes up to 60 minutes to run in serial mode.

# INPUT PARAMETERS DESCRIPTION
# Year (year, in YYYY format): year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation periods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing the domain's mask.
# DirIN_Point (string): relative path of the directory containing the point accumulated flash flood reports.
# DirOUT (string): relative path containing the map plots of the point accumulated flash flood reports.

# INPUT PARAMETERS
Year = int(sys.argv[1])
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN_Point = "Data/Compute/18_Point_AccRepFF"
DirOUT = "Data/Plot/23_Map_Point_AccRepFF"
#####################################################################################


# Defining the accumulation periods to consider
TheDateTime_Start_S = datetime(Year,1,1,0)
TheDateTime_Start_F = datetime(Year,12,31,24-Disc_Acc)

# Converting the domain's mask into a geopoint to plot the actual location of the grid-points within the domain
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_vals = mv.values(mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)
mask_lats = mv.filter(mask_lats, mask_vals == 1)
mask_lons = mv.filter(mask_lons, mask_vals == 1)
mask_vals = mv.filter(mask_vals, mask_vals == 1) - 2 # to assign the value -1 to the domain's grid points 
mask_geo = mv.create_geo(type = "xyv",
      latitudes = mask_lats,
      longitudes = mask_lons,
      values = mask_vals
      )

# Plotting the point accumulated flash flood reports for specific accumulation periods
print()
print("Plotting the point accumulated flash flood reports over the " + str(Acc) + "-hourly period ending:")
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:

      TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
      print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
      
      # Reading the point accumulated flash flood reports 
      FileIN_Point = Git_Repo + "/" + DirIN_Point + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Point_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".csv"
      if os.path.exists(FileIN_Point):
            
            # Creating the geopoints containing the point flash flood reports
            point = pd.read_csv(FileIN_Point)
            lats_point = point["AREA_AFFECTED_CENTRE_LAT"].values
            lons_point = point["AREA_AFFECTED_CENTRE_LON"].values
            point_geo = mv.create_geo(type = "xyv",
                              latitudes = lats_point,
                              longitudes = lons_point,
                              values = np.zeros(len(lats_point))
                              )

            # Plotting the point accumulated flash flood reports 
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
            
            symb_point = mv.msymb(
                  legend = "off",
                  symbol_type = "marker",
                  symbol_table_mode = "on",
                  symbol_outline = "on",
                  symbol_min_table = [-0.1],
                  symbol_max_table = [0.1],
                  symbol_colour_table = "red",
                  symbol_marker_table = 15,
                  symbol_height_table = 0.3
                  )

            symb_gridpoints = mv.msymb(
                  legend = "off",
                  symbol_type = "marker",
                  symbol_table_mode = "on",
                  symbol_outline = "on",
                  symbol_min_table = [-1.1],
                  symbol_max_table = [-0.9],
                  symbol_colour_table = "rgb(0.8,0.8,0.8)",
                  symbol_marker_table = 15,
                  symbol_height_table = 0.1
                  )

            title = mv.mtext(
                  text_line_count = 2,
                  text_line_1 = "Point flash flood reports accumulated over the " + str(Acc) + "-hourly period ending on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC",
                  text_line_2 = " ",
                  text_colour = "charcoal",
                  text_font = "arial",
                  text_font_size = 0.6
                  )

            # Saving the plot
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + str(Year) + "/" + TheDateTime_Final.strftime("%Y%m%d") 
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            FileOUT = MainDirOUT + "/Point_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H")
            png = mv.png_output(output_width = 5000, output_name = FileOUT)
            mv.setoutput(png)
            mv.plot(geo_view, mask_geo, symb_gridpoints, point_geo, symb_point, title)

      TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)