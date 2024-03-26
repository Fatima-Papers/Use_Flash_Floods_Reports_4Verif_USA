import os
from datetime import datetime, timedelta
import numpy as np
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 23_Plot_Shap_Vals.py plots the shap values for each prediction.
# Runtime: the script can take up to 1 hour to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Years_Train (string): years covered in the training dataset.
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# Git_Repo (string): repository's local path
# DirIN_ML (string): relative path of the directory containg the weights for the ML model.
# DirOUT (string): relative path containing the ML predictions.

# INPUT PARAMETERS
DateTime_Start_S = datetime(2021,9,1,12)
DateTime_Start_F = datetime(2021,9,1,12)
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Years_Train = "2005_2020"
Specification_PDT_list = ["AllRepFF_AllPredictors", "AllRepFF_NoPopDens"]
Predictors_array_list = [ ["Total Precipitation", "Percentage of Soil Saturation", "Slope of the Sub-Grid Orography", "Standard Deviation of the Sub-Grid Orography", "Population Density"], ["Total Precipitation", "Percentage of Soil Mosture", "Slope of the Sub-Grid Orography", "Standard Deviation of the Sub-Grid Orography"] ]
PredSymb_array_list = [["tp", "ss", "slor", "stdor", "pd"], ["tp", "ss", "slor", "stdor"]]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/21_Predict_RepFF"
DirOUT = "Data/Plot/23_Shap_Vals"
#############################################################################


#################
# Costum functions #
#################

def shap_vals(TheDateTime_Start, TheDateTime_Final, Title_Training_Dataset, Predictors_array, PredSymb_array, FileIN, MainDirOUT):

      # Reading the probabilities of having a flood report at each grid-box
      Shap_Vals = mv.read(FileIN)
      
      # Defining the dates for plot title
      ValidityDateS = TheDateTime_Start
      DayVS = ValidityDateS.strftime("%d")
      MonthVS = ValidityDateS.strftime("%B")
      YearVS = ValidityDateS.strftime("%Y")
      TimeVS = ValidityDateS.strftime("%H")
      ValidityDateF = TheDateTime_Final
      DayVF = ValidityDateF.strftime("%d")
      MonthVF = ValidityDateF.strftime("%B")
      YearVF = ValidityDateF.strftime("%Y")
      TimeVF = ValidityDateF.strftime("%H")
      title_plot2 = "Training dataset: " + Title_Training_Dataset
      title_plot3 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          

      # Defining the plot settings
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
            contour_level_list = np.round(np.concatenate((np.arange(0, 0.01 + 0.0001, 0.0001), np.array([1]))), decimals = 4).tolist(),
            contour_label = "off",
            contour_shade = "on",
            contour_shade_technique = "grid_shading",
            contour_shade_colour_method = "list",
            contour_shade_colour_list = [
                  "rgb(0.851, 0.851, 0.851)", # grey
                  "rgb(0.79453, 0.79453, 0.79453)",
                  "rgb(0.73806, 0.73806, 0.73806)",
                  "rgb(0.68159, 0.68159, 0.68159)",
                  "rgb(0.62512, 0.62512, 0.62512)",
                  "rgb(0.56865, 0.56865, 0.56865)",
                  "rgb(0.51218, 0.51218, 0.51218)",
                  "rgb(0.45571, 0.45571, 0.45571)",
                  "rgb(0.39924, 0.39924, 0.39924)",
                  "rgb(0.2863, 0.2863, 0.2863)",

                  "rgb(0.947, 0.7682, 0.7236)", # brown
                  "rgb(0.90281, 0.70437, 0.654847)",
                  "rgb(0.85862, 0.64054, 0.586094)",
                  "rgb(0.81443, 0.57671, 0.517341)",
                  "rgb(0.77024, 0.51288, 0.448588)",
                  "rgb(0.72605, 0.44905, 0.379835)",
                  "rgb(0.68186, 0.38522, 0.311082)",
                  "rgb(0.63767, 0.32139, 0.242329)",
                  "rgb(0.59348, 0.25756, 0.173576)",
                  "rgb(0.5051, 0.1299, 0.03607)"

                  "rgb(0.939, 0.81, 0.9067)", # light purple
                  "rgb(0.88117, 0.733718, 0.84426)",
                  "rgb(0.82334, 0.657436, 0.78182)",
                  "rgb(0.76551, 0.581154, 0.71938)",
                  "rgb(0.70768, 0.504872, 0.65694)",
                  "rgb(0.64985, 0.42859, 0.5945)",
                  "rgb(0.59202, 0.352308, 0.53206)",
                  "rgb(0.53419, 0.276026, 0.46962)",
                  "rgb(0.47636, 0.199744, 0.40718)",
                  "rgb(0.3607, 0.04718, 0.2823)",

                  "rgb(0.9448, 0.7493, 0.8177)", # pink
                  "rgb(0.92537, 0.676178, 0.76337)",
                  "rgb(0.90594, 0.603056, 0.70904)",
                  "rgb(0.88651, 0.529934, 0.65471)",
                  "rgb(0.86708, 0.456812, 0.60038)",
                  "rgb(0.84765, 0.38369, 0.54605)",
                  "rgb(0.82822, 0.310568, 0.49172)",
                  "rgb(0.80879, 0.237446, 0.43739)",
                  "rgb(0.78936, 0.164324, 0.38306)",
                  "rgb(0.7505, 0.01808, 0.2744)",

                  "rgb(0.8061, 0.8061, 0.9429)",
                  "rgb(0.72549, 0.72549, 0.94861)",
                  "rgb(0.64488, 0.64488, 0.95432)",
                  "rgb(0.56427, 0.56427, 0.96003)",
                  "rgb(0.48366, 0.48366, 0.96574)",
                  "rgb(0.40305, 0.40305, 0.97145)",
                  "rgb(0.32244, 0.32244, 0.97716)",
                  "rgb(0.24183, 0.24183, 0.98287)",
                  "rgb(0.16122, 0.16122, 0.98858)",
                  "rgb(0.0, 0.0, 1.0)",

                  "rgb(0.7719, 0.7084, 0.9465)", # purple
                  "rgb(0.70888, 0.64193, 0.89297)",
                  "rgb(0.64586, 0.57546, 0.83944)",
                  "rgb(0.58284, 0.50899, 0.78591)",
                  "rgb(0.51982, 0.44252, 0.73238)",
                  "rgb(0.4568, 0.37605, 0.67885)",
                  "rgb(0.39378, 0.30958, 0.62532)",
                  "rgb(0.33076, 0.24311, 0.57179)",
                  "rgb(0.26774, 0.17664, 0.51826)",
                  "rgb(0.1417, 0.0437, 0.4112)",

                  "rgb(0.9373, 0.9373, 0.749)", # green
                  "rgb(0.91225, 0.91225, 0.69169)",
                  "rgb(0.8872, 0.8872, 0.63438)",
                  "rgb(0.86215, 0.86215, 0.57707)",
                  "rgb(0.8371, 0.8371, 0.51976)",
                  "rgb(0.81205, 0.81205, 0.46245)",
                  "rgb(0.787, 0.787, 0.40514)",
                  "rgb(0.76195, 0.76195, 0.34783)",
                  "rgb(0.7369, 0.7369, 0.29052)",
                  "rgb(0.6868, 0.6868, 0.1759)",

                  "rgb(0.943, 0.9227, 0.7903)", # yellow
                  "rgb(0.94792, 0.90677, 0.712443)",
                  "rgb(0.95284, 0.89084, 0.634586)",
                  "rgb(0.95776, 0.87491, 0.556729)",
                  "rgb(0.96268, 0.85898, 0.478872)",
                  "rgb(0.9676, 0.84305, 0.401015)",
                  "rgb(0.97252, 0.82712, 0.323158)",
                  "rgb(0.97744, 0.81119, 0.245301)",
                  "rgb(0.98236, 0.79526, 0.167444)",
                  "rgb(0.98728, 0.77933, 0.089587)",

                  "rgb(0.9509, 0.849, 0.6962)", # light brown
                  "rgb(0.943, 0.81762, 0.629586)",
                  "rgb(0.9351, 0.78624, 0.562972)",
                  "rgb(0.9272, 0.75486, 0.496358)",
                  "rgb(0.9193, 0.72348, 0.429744)",
                  "rgb(0.9114, 0.6921, 0.36313)",
                  "rgb(0.9035, 0.66072, 0.296516)",
                  "rgb(0.8956, 0.62934, 0.229902)",
                  "rgb(0.8877, 0.59796, 0.163288)",
                  "rgb(0.8719, 0.5352, 0.03006)",

                  "rgb(0.7852, 0.9429, 0.7825)",
                  "rgb(0.712652, 0.87036, 0.709955)",
                  "rgb(0.640104, 0.79782, 0.63741)",
                  "rgb(0.567556, 0.72528, 0.564865)",
                  "rgb(0.495008, 0.65274, 0.49232)",
                  "rgb(0.42246, 0.5802, 0.419775)",
                  "rgb(0.349912, 0.50766, 0.34723)",
                  "rgb(0.277364, 0.43512, 0.274685)",
                  "rgb(0.204816, 0.36258, 0.20214)",
                  "rgb(0.132268, 0.29004, 0.129595)",
                  "rgb(0.05972, 0.2175, 0.05705)",

                  "black"
                  ]
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font_size = 0.5,
            )

      # Plotting the shap values for the different predictors
      for ind_Predictors in range(len(Predictors_array)):

            Predictors = Predictors_array[ind_Predictors]
            Predictors_symb = PredSymb_array[ind_Predictors]
            
            title_plot1 = "Shap Values for " + Predictors
            title = mv.mtext(
                  text_line_count = 4,
                  text_line_1 = title_plot1,
                  text_line_2 = title_plot2,
                  text_line_3 = title_plot3,
                  text_line_4 = " ",
                  text_colour = "charcoal",
                  text_font_size = 0.7
                  )

            # Saving the plot
            # FileOUT = MainDirOUT + "/Shap_Vals_" + Predictors_symb + "_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H")
#             png = mv.png_output(output_name = FileOUT)
#             mv.setoutput(png)
            mv.plot(geo_view, Shap_Vals[ind_Predictors], contouring, legend, title)
            exit()
            
#############################################################################


# Plotting the predictions created with a specific training dataset
for ind in range(len(Specification_PDT_list)):

      Specification_PDT = Specification_PDT_list[ind]
      Predictors_array = Predictors_array_list[ind]
      PredSymb_array = PredSymb_array_list[ind]

      Training_Dataset = Specification_PDT + "_" + Years_Train
      Title_Training_Dataset = Specification_PDT

      print()
      print("Saving the map plots of shap values for the training dataset: " + Training_Dataset)
      
      TheDateTime_Start = DateTime_Start_S
      while TheDateTime_Start <= DateTime_Start_F:
            
            TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)

            print(" - " + TheDateTime_Final.strftime("%Y%m%d"))
            FileIN = Git_Repo + "/" + DirIN + "/" + Training_Dataset + "/Shap_Vals_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Training_Dataset
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            
            shap_vals(TheDateTime_Start, TheDateTime_Final, Title_Training_Dataset, Predictors_array, PredSymb_array, FileIN, MainDirOUT)

            TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)