import os
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 03_Plot_Slope_Orog_ENS_9km.py plots the slope of sub-gridscale orography from the 
# new ENS (at 9 km resolution).
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
DirOUT = "Data/Plot/03_Slope_Orog_ENS_9km"
###########################################################################


# Retrieving the slope of sub-gridscale orography
print("Retrieving the slope of sub-gridscale orography...")
slor = mv.retrieve(
    {"class" : "od",
     "stream" : "enfo", 
     "type" : "cf", 
     "expver" : "1", 
     "levtype" : "sfc",
     "param" : "163.128",
    }) * 90

# Reading USA's domain
print("Reading the USA's domain ...")
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask = mv.bitmap(mask,0) # bitmap the values outside the domain

# Selecting the slope of sub-gridscale orography values within the considered domain
print("Selecting the slope of sub-gridscale orography values within the considered domain...")
slor_mask = (mask == 1) * slor

# Plotting the slope of sub-gridscale orography values within the considered domain
print("Plotting the slope of sub-gridscale orography values within the considered domain...")

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
    contour_level_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 90],
    contour_label = "off",
    contour_shade = "on",
    contour_shade_technique = "grid_shading",
    contour_shade_colour_method = "list",
    contour_shade_colour_list = [
        "rgb(0.04706,0.3529,0.2459)",
        "rgb(0.03368,0.5389,0.3621)",
        "rgb(0.02841,0.6304,0.4197)",
        "rgb(0.02458,0.7127,0.4718)",
        "rgb(0.01845,0.7659,0.5043)",
        "rgb(0.01341,0.8415,0.5517)",
        "rgb(0.01605,0.8938,0.5866)",
        "rgb(0,0.9961,0.6475)",
        "rgb(0.4144,0.966,0.7729)",
        "rgb(0.6669,0.9488,0.8501)",
        "rgb(0.9543,0.9045,0.6221)",
        "rgb(0.9837,0.8639,0.1849)",
        "rgb(0.9039,0.7857,0.1157)",
        "rgb(0.8542,0.5451,0.04775)",
        "rgb(0.6947,0.4387,0.02689)",
        "rgb(0.572,0.365,0.03197)",
        "rgb(0.4853,0.3147,0.04018)",
        "rgb(0.3607,0.2405,0.04718)",
        "rgb(0.2705,0.1864,0.05107)",
        "rgb(0.702,0.702,0.702)"]
        )

legend = mv.mlegend(
    legend_text_colour = "charcoal",
    legend_text_font_size = 0.5,
    )

title = mv.mtext(
    text_line_count = 2,
    text_line_1 = "Slope of sub-gridscale orography [degrees]",
    text_line_2 = " ",
    text_colour = "charcoal",
    text_font_size = 0.75
    )

# Saving the plot
print("Saving the map plot ...")
MainDirOUT = Git_Repo + "/" + DirOUT
if not os.path.exists(MainDirOUT):
    os.makedirs(MainDirOUT)
FileOUT = MainDirOUT + "/Slope_Orog" 
png = mv.png_output(output_name = FileOUT)
mv.setoutput(png)
mv.plot(geo_view, slor_mask, contouring, legend, title)