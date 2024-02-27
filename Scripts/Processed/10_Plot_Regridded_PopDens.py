import os
import metview as mv

################################################################################
# CODE DESCRIPTION
# 10_Plot_Regridded_PopDens.py plots population density.
# Runtime: negligible.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Disc_Year (integer): discretization for the years to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Grid_Raw (string): grid of NASA's raw dataset.
# Grid_2_Interpolate (string): grid to interpolate onto (e.g. "n320" for ERA5's grid).
# Git_Repo (string): repository's local path
# DirIN (string): relative path containing NASA's raw population density.
# DirOUT (string): relative path containing the extracted raw and interpolated population density.

# INPUT PARAMETERS
Year_S = 2000
Year_F = 2020
Disc_Year = 5
Mask_Domain = [22,-130,52,-60]
Grid_Raw = "15_min"
Grid_2_Interpolate = "n320"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
FileIN_Mask = "Data/Raw/Mask/USA_ERA5/Mask.grib"
DirIN = "Data/Compute/09_ExtractRaw_Regrid_PopDens"
DirOUT = "Data/Plot/10_Regridded_PopDens"
################################################################################


# Plotting the population density for specific years
for Year in range(Year_S-Disc_Year, Year_F+1, Disc_Year):

    if Year == (Year_S-Disc_Year):
        print("Saving the plot for the average population density")
        PopDens_2_Plot_IN = "PopDens_mean" 
        PopDens_2_Plot_OUT = "PopDens_mean" 
    else:
        print("Saving the plot for the population density of " + str(Year))
        PopDens_2_Plot_IN = str(Year) + "/PopDens_" + str(Year)
        PopDens_2_Plot_OUT = "PopDens_" + str(Year)
    
    # Reading the population density
    FileIN = Git_Repo + "/" + DirIN + "/" + PopDens_2_Plot_IN + "_" + Grid_2_Interpolate + "_from_" + Grid_Raw + ".grib2"
    pop_dens = mv.read(FileIN)

    # Selecting the grid-points within the considered domain
    mask = mv.read(Git_Repo + "/" + FileIN_Mask)
    pop_dens_mask = ((mask == 0) * -9999) + ((mask == 1) * pop_dens)

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
        contour_level_list = [0, 2, 4, 6, 8, 10, 25, 50, 100, 250, 500, 1000, 2500, 10000],
        contour_label = "off",
        contour_shade = "on",
        contour_shade_technique = "grid_shading",
        contour_shade_colour_method = "list",
        contour_shade_colour_list = [
                    "rgb(0.8863,0.8863,0.8863)", #0-2
                    "rgb(0.7686,0.7686,0.7686)", #2-4
                    "rgb(0.651,0.651,0.651)", #4-6
                    "rgb(0.4784,0.4784,0.4784)", #6-8
                    "rgb(0.349,0.349,0.349)", #8-10
                    "rgb(0.7534,0.7236,0.947)", #10-25
                    "rgb(0.4583,0.3797,0.9694)", #25-50
                    "rgb(0.1155,0.03345,0.6489)", #50-100
                    "rgb(0.9488,0.6669,0.8078)", #100-250
                    "rgb(1,0,0.498)", #250-500
                    "rgb(0.5818,0.02998,0.3059)", #500-1000
                    "rgb(0.968,0.887,0.428)", #1000-2500
                    "rgb(0.6154,0.5272,0.02774)"] #2500-10000
                    )

    legend = mv.mlegend(
        legend_text_colour = "charcoal",
        legend_text_font_size = 0.5,
        )

    title = mv.mtext(
        text_line_count = 2,
        text_line_1 = "Population Density [n. of people within a 1km pixel]",
        text_line_2 = " ",
        text_colour = "charcoal",
        text_font_size = 0.75
        )

    # Saving the plot
    MainDirOUT = Git_Repo + "/" + DirOUT
    if not os.path.exists(MainDirOUT):
        os.makedirs(MainDirOUT)
    FileOUT = MainDirOUT + "/" + PopDens_2_Plot_OUT + "_" + Grid_2_Interpolate + "_from_" + Grid_Raw + ".grib2"
    png = mv.png_output(output_name = FileOUT)
    mv.setoutput(png)
    mv.plot(geo_view, pop_dens_mask, contouring, legend, title)