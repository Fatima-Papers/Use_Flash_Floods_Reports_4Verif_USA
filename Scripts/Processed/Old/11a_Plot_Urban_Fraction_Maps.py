import os
import metview as mv

###############################################################################
# CODE DESCRIPTION
# 11a_Plot_Urban_Fraction_Maps.py plots urban fraction.
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Disc_Year (integer): discretization for the years to consider.
# Grid (string): grid to consider (e.g. "n320" for ERA5's grid).
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path of the file containing ERA5's mask for USA.
# DirIN (string): relative path containing NASA's raw population density.
# DirOUT (string): relative path containing the extracted raw and interpolated population density.

# INPUT PARAMETERS
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/10_PopDens_Regrid"
DirOUT = "Data/Plot/11a_Urban_Fraction_Maps"
###############################################################################


# Plotting the population density for specific years
print()
print("Plotting urban fraction...")

DirIN = "/home/rdx/data/climate/climate.v020/639_4"
FileNameIN = "urban"

urb_frac = mv.read(DirIN + "/" + FileNameIN)
urb_frac_bitmap = ((urb_frac == 0) * -1) + ((urb_frac > 0) * urb_frac)

# Plotting the population density
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
    contour_level_list = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 1],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_colour_method = "list",
    contour_shade_method = "area_fill",
    contour_shade_colour_list = [
                "rgb(0.9525,0.7114,0.6632)", # 0 -0.1
                "rgb(0.851,0.7176,0.4667)",
                "rgb(1,0.1451,0)",
                "rgb(0.498,1,0)",
                "rgb(0,1,1)",
                "rgb(1,0.6902,0)",
                "rgb(0.5513,0.8604,0.8244)", # 0.1 - 0.2
                "rgb(0.907,0.5832,0.907)", # 0.2 - 0.3
                "rgb(0.5921,0.7045,0.472)", # 0.3 - 0.4
                "rgb(0.451,0.6392,1)", # 0.4 - 0.5
                "rgb(0.6,0.08235,0.02745)"] # 0.5 - 1
                )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Urban Fraction [-]",
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
# MainDirOUT = Git_Repo + "/" + DirOUT
# if not os.path.exists(MainDirOUT):
#     os.makedirs(MainDirOUT)
# FileOUT = MainDirOUT + "/PopDens_" + Grid + "_" + str(Year)
# png = mv.png_output(output_name = FileOUT)
# mv.setoutput(png)
mv.plot(urb_frac_bitmap, contouring, legend, title)