import os
from datetime import datetime, timedelta
import metview as mv

###########################################################################
# CODE DESCRIPTION
# 22_Plot_Prob_RepFF.py plots the probabilities of having a flash flood report or observe a flash flood event at each grid-box.
# Runtime: the script can take up to 1 hour to run in serial.

# INPUT PARAMETERS DESCRIPTION
# DateTime_Start_S (date and time): start date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# DateTime_Start_F (date and time): final date (first three numbers) and time (fourth number) for the analysis period (representing the beginning of the accumulation period).
# Acc (integer, in hours): accumulation period.
# Disc_Acc (integer, in hours): discretization for the accumulation peiods to consider.
# Mask_Domain (list of floats, in S/W/N/E coordinates): domain's coordinates.
# Years_Train (string): years covered in the training dataset.
# Specification_PDT (string): specification of the dataset (PDT) used  for training.
# Perc_RedFF_list (list of floats, from o to 1): list of percentages for the reduction of flood reports in the training dataset. 
# Git_Repo (string): repository's local path
# DirIN_ML (string): relative path of the directory containg the weights for the ML model.
# DirOUT (string): relative path containing the ML predictions.

# INPUT PARAMETERS
DateTime_Start_S = datetime(2021,7,14,12)
DateTime_Start_F = datetime(2021,7,14,12)
Acc = 12
Disc_Acc = 12
Years_Train = "2005_2020"
Specification_PDT_list = ["AllRepFF_NoPopDens"]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/26_Predict_RepFF_Globe"
DirOUT = "Data/Plot/27_Prob_RepFF_Globe"
#############################################################################


#################
# Costum functions #
#################

def plot_predFF(TheDateTime_Start, TheDateTime_Final, Title_Training_Dataset, FileIN, MainDirOUT):

      # Reading the probabilities of having a flood report at each grid-box
      Prob_RepFF = mv.read(FileIN)
      
      # Defining the plot titles
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
      
      if Title_Training_Dataset == "AllRepFF_AllPredictors":
            title_plot1 = "Probability (%) of having a flash flood report in each grid-box"
      else:
            title_plot1 = "Probability (%) of observing a flash flood event in each grid-box"
      title_plot2 = "Training dataset: " + Title_Training_Dataset
      title_plot3 = "VT: " + DayVS + " " + MonthVS + " " + YearVS + " " + TimeVS + " UTC - " + DayVF + " " + MonthVF + " " + YearVF + " " + TimeVF  + " UTC"          

      # Defining the plot
      coastlines = mv.mcoast(
            map_coastline_colour = "charcoal",
            map_coastline_thickness = 1,
            map_coastline_resolution = "low",
            map_coastline_sea_shade = "on",
            map_coastline_sea_shade_colour = "RGB(0.7398,0.9465,0.943)",
            map_boundaries = "on",
            map_boundaries_colour = "charcoal",
            map_boundaries_thickness = 1,
            map_grid_latitude_increment = 30,
            map_grid_longitude_increment = 60,
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
            contour_level_list = [0, 0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4, 5, 100],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_technique = "grid_shading",
            contour_shade_colour_method = "list",
            contour_shade_colour_list = [
                  "rgb(0.9509,0.8617,0.6962)",
                  "rgb(0.9702,0.7495,0.3396",
                  "rgb(0.9962,0.6557,0.02345)",
                  "rgb(0.7264,0.4814,0.02658)",
                  "rgb(0.411,0.2853,0.05171)",
                  
                  "rgb(0.8792,0.7569,0.9451)",
                  "rgb(0.7998,0.4949,0.9639)",
                  "rgb(0.7049,0.2163,0.968)",
                  "rgb(0.4824,0.06667,0.702)",
                  
                  "rgb(0.1451,0,1)"]
            )

      legend = mv.mlegend(
            legend_text_colour = "charcoal",
            legend_text_font_size = 0.5,
            )

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
      # FileOUT = MainDirOUT + "/Prob_RepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H")
#       png = mv.png_output(output_name = FileOUT)
#       mv.setoutput(png)
      mv.plot(coastlines, Prob_RepFF, contouring, legend, title)
      exit()


#############################################################################


# Plotting the predictions created with a specific training dataset
for Specification_PDT in Specification_PDT_list:

      Training_Dataset = Specification_PDT + "_" + Years_Train
      Title_Training_Dataset = Specification_PDT
      
      TheDateTime_Start = DateTime_Start_S
      while TheDateTime_Start <= DateTime_Start_F:
            
            TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)

            print(" - " + TheDateTime_Final.strftime("%Y%m%d"))
            FileIN = Git_Repo + "/" + DirIN + "/" + Training_Dataset + "/Prob_RepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
            MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Training_Dataset
            if not os.path.exists(MainDirOUT):
                  os.makedirs(MainDirOUT)
            
            plot_predFF(TheDateTime_Start, TheDateTime_Final, Title_Training_Dataset, FileIN, MainDirOUT)

            TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)