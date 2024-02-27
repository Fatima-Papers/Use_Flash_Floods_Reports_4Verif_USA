import os
import metview as mv

############################################################################
# CODE DESCRIPTION
# 02_Plot_Soil_Type_ENS_9km.py plots the soil type from the new ENS (at 9 km resolution).  
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
DirOUT = "Data/Plot/02_Soil_Type_ENS_9km"
############################################################################

# Retrieving the soil type
print("Retrieving the soil type ...")
slt = mv.retrieve(
    {"class" : "od",
     "stream" : "enfo", 
     "type" : "cf", 
     "expver" : "1", 
     "levtype" : "sfc",
     "param" : "43.128",
    })

# Reading USA's domain
print("Reading the USA's domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Selecting the soil type values within the considered domain
print("Selecting the soil type values within the domain ...")
slt_mask = (mask == 1) * slt

# Plotting the soil type values within the considered domain
print("Plotting the soil type values within the domain ...")

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
    contour_level_list = [0.1, 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = ["rgb(1,0.8863,0.6588)", "rgb(0.4039,0.0549,0.003922)", "rgb(0,0.9961,0.01176)", "rgb(0.298,0.3843,0)", "cyan", "charcoal", "blue"])

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    legend_display_type = "disjoint",
    legend_text_composition = "user_text_only",
    legend_user_lines = ["coarse","medium","medium fine","fine","very fine","organic","tropical organic"],
    legend_entry_text_width = 90.00,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Soil Type",
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
print("Saving the map plot ...")
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Soil_Type" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, slt_mask, contouring, legend, title)