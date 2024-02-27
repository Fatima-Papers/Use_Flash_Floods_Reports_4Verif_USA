import os
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 01_Plot_Orog_ENS_9km.py plots the orography from the new ENS (at 9 km resolution). 
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Git_Repo (string): repository's local path
# FileIN_Mask (string): relative path where the USA's mask is stored.
# DirOUT (string): relative path where to store the plot 

# INPUT PARAMETERS
Mask_Domain = [22,-130,52,-60]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ENS_9km/Mask.grib"
DirOUT = "Data/Plot/01_Orog_ENS_9km"
###########################################################################

# Retrieve the geopotential height and converting it in metres
print("Reading the geopotential height and converting it in metres ...")
orog = mv.retrieve(
    {"class" : "od",
     "stream" : "oper", 
     "type" : "fc", 
     "expver" : "1", 
     "levtype" : "sfc",
     "param" : "129.128",
    }) / 9.81 

# Reading USA's domain
print("Reading the USA's domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Selecting the orography values within the considered domain
print("Selecting the orography values within the domain ...")
orog_mask = (mask == 1) * orog

# Plotting the orography values within the considered domain
print("Plotting the orography values within the domain ...")

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
FileOUT = MainDirOUT + "/Orog" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, orog_mask, contouring, legend, title)