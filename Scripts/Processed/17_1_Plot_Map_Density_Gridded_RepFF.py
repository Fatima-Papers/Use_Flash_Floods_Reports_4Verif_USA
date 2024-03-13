import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 17_1_Plot_Map_Density_Gridded_RepFF.py creates a map plot showing the density of the
# gridded flood reports within the domain.
# Runtime: the code takes up to 3 minutes to run in serial for 15 years.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Final_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the end of the accumulation period).
# DateTime_Final_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the end of the accumulation period).
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# DirIN (string): relative path where USA's mask can be found
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
DateTime_Final_S = datetime(2021,1,1,12)
DateTime_Final_F = datetime(2022,1,1,0)
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/16_Gridded_AccRepFF"
DirOUT = "Data/Plot/17_1_Map_Density_Gridded_RepFF"
###########################################################################


print("Creating the map plot of the relative frequency of flood reports between " + DateTime_Final_S.strftime("%Y%m%d%H") + " and " + DateTime_Final_F.strftime("%Y%m%d%H") + ". Reading reports for:") 

# Define the total number of days in the considered period
NumPeriods = ((DateTime_Final_F - DateTime_Final_S).days + 1) * (24 / Disc_Acc)

# Initialize the variable that will store the total of flash flood reports per grid-box in the considered period
Grid_RepFF_Total = 0

# Adding up the number of flood reports observed in the considered period
TheDateTime_Final = DateTime_Final_S
while TheDateTime_Final <= DateTime_Final_F:
    
    print(" - " + TheDateTime_Final.strftime("%Y%m%d%H"))
    
    FileIN_Grid_AccRepFF = Git_Repo + "/" + DirIN + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/FlashFloodRep_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
    Grid_AccRepFF = mv.read(FileIN_Grid_AccRepFF)

    Grid_RepFF_Total = Grid_RepFF_Total + Grid_AccRepFF

    TheDateTime_Final = TheDateTime_Final + timedelta(hours=Disc_Acc)


# Bitmapping all those grid-boxes that have never seen any flash flood reports
Grid_RepFF_Total = mv.bitmap(Grid_RepFF_Total, 0)

# Transforming the total flood reports in percentages
Grid_RepFF_Density = Grid_RepFF_Total / NumPeriods * 100

# Ploting the map with the flood reports density
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
    contour_level_list = [0, 0.2, 0.4, 0.6, 0.8, 1, 3, 5, 7, 9, 20],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.9409, 0.8081, 0.8081)",
        "rgb(0.9533, 0.6310, 0.6310)",
        "rgb(0.9616, 0.5129, 0.5129)",
        "rgb(0.9698, 0.3949, 0.3949)",
        "rgb(0.9781, 0.2768, 0.2768)",
        "rgb(0.9165, 0.0970, 0.0970)",
        "rgb(0.7926, 0.0832, 0.0832)",
        "rgb(0.6687, 0.0694, 0.0694)",
        "rgb(0.5449, 0.0555, 0.0555)",
        "rgb(0.3292,0.04724,0.04724)",
        ]
    )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    )

title = mv.mtext(
    text_line_count = 3,
    text_line_1 = "Relative frequency [%] of gridded flood reports",
    text_line_2 = "between " + DateTime_Final_S.strftime("%Y-%m-%d") + " and " + DateTime_Final_F.strftime("%Y-%m-%d"),
    text_line_3 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
print("Saving the map plot ...")
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Grid_RepFF_Density_" +  DateTime_Final_S.strftime("%Y%m%d") + "_" + DateTime_Final_F.strftime("%Y%m%d")
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, Grid_RepFF_Density, contouring, legend, title)