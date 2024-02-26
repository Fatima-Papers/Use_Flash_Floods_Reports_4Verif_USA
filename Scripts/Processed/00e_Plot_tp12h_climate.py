import os
import numpy as np
import metview as mv

############################################################################
# CODE DESCRIPTION
# 00e_Plot_tp12h_climate.py plots the climatology from ERA5-ecPoint for 12h rainfall.
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Acc (integer, in hours): rainfall's accumulation period.
# Perc2Plot (float): percentile to plot.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing ERA5's mask for USA.
# DirIN (string): relative path of the directory containing the rainfall climatology.
# DirOUT (string): relative path of the directory containing the plot of the rainfall climatology.

# NOTES
# The percentiles correspond roughly to the following return periods:
# 99th -> 3 times in a year
# 99.8th -> once in 1 year
# 99.9th -> once in 2 years
# 99.95th -> once in 5 years
# 99.98th -> once in 10 years
# 99.99th -> once in 20 years
# 99.995th -> once in 50 years
# 99.998th -> once in 100 years

# INPUT PARAMETERS
Acc = 12
Perc2Plot = 99.8
Mask_Domain = [15,-135,55,-55]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirOUT = "Data/Plot/00e_tp12h_climate"
############################################################################

# Reading the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Reading the rainfall climatology and the computed percentiles 
climate = mv.read(Git_Repo + "/" + DirIN + "/tp_climate_" + f"{Acc:02}" + "h_ERA5_ecPoint.grib")
percs_computed = np.load(Git_Repo + "/" + DirIN + "/percs_computed_4_tp_climate.npy")

# Select the percentile to plot
ind_Perc = np.where(percs_computed == Perc2Plot)[0][0]
climate_perc = climate[ind_Perc]

# Selecting the grid-points within the considered domain
climate_perc_mask = ((mask == 0) * -9999) + ((mask == 1) * climate_perc)

# Plot the rainfall climatology
geo_view = mv.geoview(
    map_projection = "mercator",
    map_area_definition = "corners",
    area = Mask_Domain
    )

coastlines = mv.mcoast(
    map_coastline_colour = "charcoal",
    map_coastline_thickness = 1,
    map_coastline_resolution = "high",
    map_coastline_sea_shade = "on",
    map_coastline_sea_shade_colour = "RGB(0.7398,0.9465,0.943)",
    map_boundaries = "on",
    map_boundaries_colour = "charcoal",
    map_boundaries_thickness = 1,
    map_grid_latitude_increment = 5,
    map_grid_longitude_increment = 10,
    map_label_right = "off",
    map_label_top = "off",
    map_label_colour = "charcoal",
    map_grid_thickness = 1,
    map_grid_colour = "charcoal",
    map_label_height = 0.5
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
      text_line_count = 2,
      text_line_1 = "Climatology from ERA5-ecPoint for " + str(Acc) + "h rainfall - " + str(Perc2Plot) + "th  percentile",
      text_line_2 = " ",
      text_colour = "charcoal",
      text_font_size = 0.75
      )

# Saving the maps
DirOUT_temp = Git_Repo + "/" + DirOUT
if not os.path.exists(DirOUT_temp):
      os.makedirs(DirOUT_temp)
FileOUT = DirOUT_temp + "/tp" + f"{Acc:02}" + "h_climate_" + str(Perc2Plot) + "th"
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, climate_perc_mask, contouring, coastlines, legend, title)