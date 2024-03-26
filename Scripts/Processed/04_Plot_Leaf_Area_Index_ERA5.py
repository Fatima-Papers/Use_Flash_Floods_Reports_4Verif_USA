import os
from datetime import datetime, timedelta
import metview as mv

#############################################################################
# CODE DESCRIPTION
# 04_Plot_Leaf_Area_Index_ERA5.py plots the leaf area index from ERA5 (at 31 km resolution).
# Runtime: the code takes up to 20 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the US mask is stored.
# DirIN (string): relative path of the directory containing the leaf area index files.
# DirOUT (string): relative path of the directory containing the leaf area index plots.

# INPUT PARAMETERS
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Raw/Analysis/ERA5/lai"
DirOUT = "Data/Plot/04_Leaf_Area_Index_ERA5"
#############################################################################


# Plotting the leaf area index for different days in the year
print()
print("Plotting the leaf area index for:")

DateS = datetime(2020,1,1)
DateF = datetime(2020,12,31)
TheDate = DateS
while TheDate <= DateF:

    print(" - " + TheDate.strftime("%m-%d"))

    # Reading the leaf area index
    lai = mv.read(Git_Repo + "/" + DirIN + "/lai_" + TheDate.strftime("%m%d") + ".grib")

    # Masking the US domain
    mask = mv.read(Git_Repo + "/" + FileIN_Mask)
    mask = mv.bitmap(mask,0) # bitmap the values outside the domain
    lai_mask = (mask == 1) * lai

    # Plotting the leaf area index for the US domain
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
        contour_level_list = [-0.05, 0.05, 0.2, 0.6, 1, 1.5, 2, 3, 4, 5, 6 , 7],
        contour_label = "off",
        contour_shade = "on",
        contour_shade_method = "area_fill",
        contour_shade_colour_method = "list",
        contour_shade_colour_list = [
            "rgb(1,0.9216,0.8431)", # -0.05 - 0.05
            "rgb(0.902,0.902,0.8)", # 0.05 - 0.2
            "rgb(0.7804,0.851,0.7412)", # 0.2 - 0.6
            "rgb(0.549,0.8,0.502)", # 0.6 - 1
            "rgb(0,1,0)", # 1 - 1.5
            "rgb(0.09804,0.8196,0.09804)", # 1.5 - 2
            "rgb(0.1098,0.651,0.1098)", # 2 - 3
            "rgb(0.09804,0.502,0.298)", # 3- 4
            "rgb(0.06667,0.349,0.2078)",  # 4 - 5
            "rgb(0,0.2,0.09804)", # 5 - 6
            "black"  # 6 - 7
            ])

    legend = mv.mlegend(
        legend_text_colour = "charcoal",
        legend_text_font_size = 0.5,
        )

    title = mv.mtext(
        text_line_count = 2,
        text_line_1 = "Leaf Area Index [m^2 / m^2] - " + TheDate.strftime("%m-%d"),
        text_line_2 = " ",
        text_colour = "charcoal",
        text_font_size = 0.75
        )

    # Saving the plot
    MainDirOUT = Git_Repo + "/" + DirOUT
    if not os.path.exists(MainDirOUT):
        os.makedirs(MainDirOUT)
    FileOUT = MainDirOUT + "/lai_" + TheDate.strftime("%m%d")
    png = mv.png_output(output_width = 5000, output_name = FileOUT)
    mv.setoutput(png)
    mv.plot(geo_view, lai_mask, contouring, legend, title)

    TheDate = TheDate + timedelta(days=1)
