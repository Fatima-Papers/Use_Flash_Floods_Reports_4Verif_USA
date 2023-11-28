import os
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 01_Plot_Mask_USA_ENS_Orog.py plots USA's mask and its orography for the ECMWF ENS 
# grid.
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Git_Repo (string): repository's local path
# DirIN (string): relative path where USA's mask can be found
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Mask_Domain = [15,-135,55,-55]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Raw/Mask_USA_ENS"
DirOUT = "Data/Plot/Mask_USA_ENS_Orog"
###########################################################################


# Retrieving the ensemble orography
print("Retrieving ENS orography ...")
orog = mv.retrieve(
    type = "cf",
    stream = "ef",
    levtype = "sfc",
    param = "z",
    grid = "o640"
    ) / 9.81 

# Reading USA's mask
print("Reading USA's mask ...")
mask = mv.read(Git_Repo + "/" + DirIN + "/Mask.grib")

# Selecting the orography values within the considered domain
print("Selecting the orography values within the considered domain ...")
orog_mask = ((mask == 0) * (-1)) + ((mask == 1) * orog) 

# Plotting the orography values within the considered domain
print("Plotting the orography values within the considered domain ...")

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
    contour_level_list = [0, 50, 250, 500, 750, 1200, 1500, 2000, 2500, 99999],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = ["RGB(0.0353,0.4392,0.2235)", "RGB(0.3020,0.5725,0.2314)", "RGB(0.4298,0.7810,0.3327)", "RGB(0.9525,0.9259,0.5534)", "RGB(0.8706,0.7647,0.4235)", "RGB(0.7333,0.4706,0.1765)", "RGB(0.5882,0.2157,0.0392)", "RGB(0.4549,0.2784,0.2902)", "RGB(0.8235,0.8235,0.8235)"]
    )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Orography [m.a.s.l.]",
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
print("Saving the map plot ...")
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Mask_USA_ENS_Orog" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, orog_mask, contouring, coastlines, legend, title)