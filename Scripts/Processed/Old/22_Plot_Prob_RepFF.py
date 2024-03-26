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
DateTime_Start_S = datetime(2021,1,1,0)
DateTime_Start_F = datetime(2021,12,31,12)
Acc = 12
Disc_Acc = 12
Mask_Domain = [22,-130,52,-60]
Years_Train = "2005_2020"
Specification_PDT_list = [
      "AllRepFF_AllPredictors", 
      "AllRepFF_NoPopDens", 
      "GradRedFF_NoPopDens"
      "NoEastFF_AllPredictors", # East
      "NoEastFF_NoPopDens", 
      "NoEastGP_AllPredictors",
      "NoEastGP_NoPopDens",
      "NoWestFF_AllPredictors", # West
      "NoWestFF_NoPopDens", 
      "NoWestGP_AllPredictors",
      "NoWestGP_NoPopDens",             
      "NoNorthFF_AllPredictors", #North
      "NoNorthFF_NoPopDens", 
      "NoNorthGP_AllPredictors",
      "NoNorthGP_NoPopDens",            
      "NoSouthFF_AllPredictors", # South
      "NoSouthFF_NoPopDens", 
      "NoSouthGP_AllPredictors",
      "NoSouthGP_NoPopDens",   
      ]
Perc_RedFF_list = [0,1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Compute/21_Predict_RepFF"
DirOUT = "Data/Plot/22_Prob_RepFF"
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
            contour_level_list = [0, 0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4, 5, 100],
            contour_label = "off",
            contour_shade = "on",
            contour_shade_technique = "grid_shading",
            contour_shade_colour_method = "list",
            contour_shade_colour_list = [
                  "rgb(0.8,0.8,0.8)",
                  "rgb(0.7,0.7,0.7)",
                  "rgb(0.6,0.6,0.6)",
                  "rgb(0.5,0.5,0.5)",
                  "rgb(0.4,0.4,0.4)",
                  "rgb(0.9228,0.6627,0.6537)",
                  "rgb(0.9661,0.4554,0.4378)",
                  "rgb(0.9819,0.2739,0.2495)",
                  "rgb(0.6481,0.04717,0.02644)",
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
      FileOUT = MainDirOUT + "/Prob_RepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H")
      png = mv.png_output(output_name = FileOUT)
      mv.setoutput(png)
      mv.plot(geo_view, Prob_RepFF, contouring, legend, title)


#############################################################################


# Plotting the predictions created with a specific training dataset
for Specification_PDT in Specification_PDT_list:

      Training_Dataset = Specification_PDT + "_" + Years_Train
      Title_Training_Dataset = Specification_PDT
      
      if Specification_PDT == "GradRedFF_NoPopDens":

            for Perc_RedFF in Perc_RedFF_list:
                    
                  Training_Dataset_temp = Training_Dataset + "/" + str(int(Perc_RedFF * 100))
                  Title_Training_Dataset = Specification_PDT + " (Reduction of " + str(int(Perc_RedFF * 100)) + "%)"

                  print()
                  print("Saving the plot of probabilities of having a flood report for the " + Training_Dataset_temp + " training dataset and the periods ending on:")
      
                  TheDateTime_Start = DateTime_Start_S
                  while TheDateTime_Start <= DateTime_Start_F:
                        
                        TheDateTime_Final = TheDateTime_Start + timedelta(hours=Acc)

                        print(" - " + TheDateTime_Final.strftime("%Y%m%d"))
                        FileIN = Git_Repo + "/" + DirIN + "/" + Training_Dataset_temp + "/Prob_RepFF_" +  TheDateTime_Final.strftime("%Y%m%d") + "_" + TheDateTime_Final.strftime("%H") + ".grib"
                        MainDirOUT = Git_Repo + "/" + DirOUT + "/" + Training_Dataset_temp
                        if not os.path.exists(MainDirOUT):
                              os.makedirs(MainDirOUT)
                        
                        plot_predFF(TheDateTime_Start, TheDateTime_Final, Title_Training_Dataset, FileIN, MainDirOUT)

                        TheDateTime_Start = TheDateTime_Start + timedelta(hours=Disc_Acc)

      else:
              
            print()
            print("Saving the plots of probabilities of having a flood report for the training dataset: " + Training_Dataset)
            
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