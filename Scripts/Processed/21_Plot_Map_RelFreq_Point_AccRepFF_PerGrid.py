import os
from datetime import datetime, timedelta
import metview as mv

##########################################################################################
# CODE DESCRIPTION
# 21_Plot_Map_RelFreq_Point_AccRepFF_PerGrid.py creates a map plot of the relative 
# frequency of point accumulated flash flood reports in each grid-box of the domain.
# Runtime: the code takes up to 3 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer): start year to consider.
# Year_F (integer): final year to consider.
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation periods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the accumulated point flash flood reports per grid-box.
# DirOUT (string): relative path of the directory containing the map plot of the relative frequency.

# INPUT PARAMETERS
Year_S = 2005
Year_F= 2023
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/19_Grid_AccRepFF"
DirOUT = "Data/Plot/21_Map_RelFreq_Point_AccRepFF_PerGrid"
##########################################################################################


# Defining the accumulation periods to consider
TheDateTime_Start_S = datetime(Year_S,1,1,0)
TheDateTime_Start_F = datetime(Year_F,12,31,24-Disc_Acc)

# Defining the total number of days in the considered period
Num_Acc_Periods = ((TheDateTime_Start_F - TheDateTime_Start_S).days + 1) * (24 / Disc_Acc)

# Initializing the variable that will store the absolute frequency of accumulated gridded flash flood reports per grid-box within the considered period
AbsFreq_Grid_AccRepFF = 0

# Adding up the number of accumulated gridded flash flood reports observed within the considered period
print()
print("Computing the relative frequency of " + str(Acc) + "-hourly gridded flash flood reports in each grid-box of the domain between " + str(Year_S) + " and " + str(Year_F))
print("Adding the reports in the period ending:")
TheDateTime_Start = TheDateTime_Start_S
while TheDateTime_Start <= TheDateTime_Start_F:
    TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)
    print(" - on " + TheDateTime_Final.strftime("%Y-%m-%d") + " at " + TheDateTime_Final.strftime("%H") + " UTC")
    FileIN_Grid_AccRepFF_SinglePer = Git_Repo + "/" + DirIN + "/" + TheDateTime_Final.strftime("%Y") + "/" + TheDateTime_Final.strftime("%Y%m%d") + "/Grid_AccRepFF_" + TheDateTime_Final.strftime("%Y%m%d%H") + ".grib"
    Grid_AccRepFF_SinglePer = mv.read(FileIN_Grid_AccRepFF_SinglePer)
    AbsFreq_Grid_AccRepFF = AbsFreq_Grid_AccRepFF + Grid_AccRepFF_SinglePer
    TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)

# Bitmapping all those grid-boxes that have never seen any flash flood reports
AbsFreq_Grid_AccRepFF = mv.bitmap(AbsFreq_Grid_AccRepFF, 0)

# Computing the relative frequency
RelFreq_Grid_AccRepFF = AbsFreq_Grid_AccRepFF / Num_Acc_Periods * 100

# Creating the regions
RelFreq_Grid_AccRepFF_nw = mv.bitmap(mv.mask(RelFreq_Grid_AccRepFF, [50,-140,38,-100]) * RelFreq_Grid_AccRepFF,0)
RelFreq_Grid_AccRepFF_sw = mv.bitmap(mv.mask(RelFreq_Grid_AccRepFF, [38,-140,20,-100]) * RelFreq_Grid_AccRepFF,0)
RelFreq_Grid_AccRepFF_ne = mv.bitmap(mv.mask(RelFreq_Grid_AccRepFF, [50,-100,38,-60]) * RelFreq_Grid_AccRepFF,0)
RelFreq_Grid_AccRepFF_se = mv.bitmap(mv.mask(RelFreq_Grid_AccRepFF, [38,-100,20,-60]) * RelFreq_Grid_AccRepFF,0)

# Ploting the map with the flood reports density
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

contouring_nw = mv.mcont(
    legend = "on", 
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 0.1, 1, 10],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.9504,0.8372,0.6417)",
        "rgb(0.9333,0.6392,0.1255)",
        "rgb(0.3451,0.2387,0.0549)",
        ]
    )

contouring_sw = mv.mcont(
    legend = "on", 
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 0.1, 1, 10],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.9396,0.947,0.7236)",
        "rgb(0.8304,0.8538,0.3854)",
        "rgb(0.3364,0.3429,0.214)",
        ]
    )

contouring_ne = mv.mcont(
    legend = "on", 
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 0.1, 1, 10],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.7592,0.9427,0.9213)",
        "rgb(0.3512,0.8174,0.763)",
        "rgb(0.05917,0.3487,0.3149)",
        ]
    )

contouring_se = mv.mcont(
    legend = "on", 
    contour = "off",
    contour_level_selection_type = "level_list",
    contour_level_list = [0, 0.1, 1, 10],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.6962,0.8872,0.9509)",
        "rgb(0.1326,0.7278,0.9262)",
        "rgb(0.04315,0.3372,0.4353)",
        ]
    )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.3,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Relative frequency [%] of gridded flood reports between " + str(Year_S) + " and " + str(Year_F),
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Map_RelFreq_Point_AccRepFF_PerGrid_" +  str(Year_S) + "_" + str(Year_F)
png = mv.png_output(output_width = 5000, output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, RelFreq_Grid_AccRepFF_nw, contouring_nw, RelFreq_Grid_AccRepFF_sw, contouring_sw, RelFreq_Grid_AccRepFF_ne, contouring_ne, RelFreq_Grid_AccRepFF_se, contouring_se, legend, title)