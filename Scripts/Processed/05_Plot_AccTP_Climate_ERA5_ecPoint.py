import os
import numpy as np
import metview as mv

#####################################################################################
# CODE DESCRIPTION
# 05_Plot_AccTP_Climate_ERA5_ecPoint.py plots the rainfall climatology from ERA5-ecPoint, for 
# different return periods and for a specific rainfall accumulation period.
# Runtime: the script takes up to 30 seconds to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Acc (integer, in hours): rainfall's accumulation period.
# Perc2Plot_list (list of floats): list of percentiles to plot.
# YearRP_list (list of integers): list of the years return period corresponding to the considered percentiles.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# FileIN_Mask (string): relative path of the file containing ERA5's mask for USA.
# DirIN (string): relative path of the directory containing the rainfall climatology.
# DirOUT (string): relative path of the directory containing the plot of the rainfall climatology.

# NOTES
# The percentiles correspond roughly to the following return periods:
# 99.9th -> once in 1 years
# 99.95th -> once in 2 years
# 99.98th -> once in 5 years
# 99.99th -> once in 10 years
# 99.995th -> once in 20 years

# INPUT PARAMETERS
Acc = 12
Perc2Plot_list = [99.9, 99.95, 99.98, 99.99, 99.995]
YearRP_list = [1, 2, 5, 10, 20]
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Raw/Analysis/ERA5_ecPoint/tp_climate"
DirOUT = "Data/Plot/05_AccTP_Climate_ERA5_ecPoint"
#####################################################################################

# Reading the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)

# Reading the rainfall climatology and the computed percentiles 
climate = mv.read(Git_Repo + "/" + DirIN + "/tp_climate_" + f"{Acc:02}" + "h_ERA5_ecPoint.grib")
percs_computed = np.load(Git_Repo + "/" + DirIN + "/percs.npy")

# Select the percentiles to plot
print("Creating and saving plot of " + f"{Acc:02}" + "-hourly rainfall climatology for the:")

for ind_perc in range(len(Perc2Plot_list)):

    Perc2Plot = Perc2Plot_list[ind_perc]
    YearRP = YearRP_list[ind_perc]

    print(" - " + str(Perc2Plot) + "th percentile (" + str(YearRP) + "-year return period)")

    # Select the percentile to plot
    ind_Perc = np.where(percs_computed == Perc2Plot)[0][0]
    climate_perc = climate[ind_Perc]

    # Selecting the grid-points within the considered domain
    climate_perc_mask = ((mask == 0) * -9999) + ((mask == 1) * climate_perc)

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
        text_line_count = 2,
        text_line_1 = "Climatology from ERA5-ecPoint for " + f"{Acc:02}" + "h rainfall - " + str(Perc2Plot) + "th  percentile (" + str(YearRP) + "-year return period)",
        text_line_2 = " ",
        text_colour = "charcoal",
        text_font_size = 0.75
        )

    # Saving the maps
    DirOUT_temp = Git_Repo + "/" + DirOUT
    if not os.path.exists(DirOUT_temp):
        os.makedirs(DirOUT_temp)
    FileOUT = DirOUT_temp + "/tp" + f"{Acc:02}" + "h_climate_" + str(Perc2Plot) + "th"
    png = mv.png_output(output_width = 5000, output_name = FileOUT)
    mv.setoutput(png)
    mv.plot(geo_view, climate_perc_mask, contouring, legend, title)