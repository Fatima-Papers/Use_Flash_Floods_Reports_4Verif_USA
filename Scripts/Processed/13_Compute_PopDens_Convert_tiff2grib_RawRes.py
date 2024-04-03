import os
import zipfile
import rasterio
import numpy as np
from eccodes import *

############################################################################################
# CODE DESCRIPTION
# 13_Compute_PopDens_Convert_tiff2grib_RawRes.py converts the NASA's population density (at different 
# resolutions) from geotiff to grib2.
# Runtime: the code can take up to 10 minutes to run in serial.

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Disc_Year (integer): discretization for the years to consider.
# Grid_Raw (string): grid of NASA's raw dataset.
# Git_Repo (string): repository's local path.
# DirIN (string): relative path of the directory containing the NASA's raw population density.
# DirOUT (string): relative path of the directory containing the extracted raw and interpolated population density.

# INPUT PARAMETERS
Year_S = 2000
Year_F = 2020
Disc_Year = 5
Grid_Raw = "30_sec"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Raw/OBS/NASA_PopDens"
DirOUT = "Data/Compute/13_PopDens_Convert_tiff2grib_RawRes"
############################################################################################

for Year in range(Year_S, Year_F+1, Disc_Year):

      print(" ")
      print("Post-processing NASA's population dataset at " + Grid_Raw + " resolution for year: " + str(Year))

      ########################################################
      # Extracting the zip files containing NASA's raw population density   #
      ########################################################

      print(" - Extracting NASA's raw population density from zip file...")

      # Creating output directory
      MainDirOUT = Git_Repo + "/" + DirOUT + "/" + str(Year)
      if not os.path.exists(MainDirOUT):
            os.makedirs(MainDirOUT)

      # Extracting zip files
      FileIN = Git_Repo + "/" + DirIN + "/gpw-v4-population-density-rev11_" + str(Year) + "_" + Grid_Raw + "_tif.zip"
      with zipfile.ZipFile(FileIN, 'r') as zip_ref:
            zip_ref.extractall(MainDirOUT)
      
      
      ###############################
      # Converting the geotiff file into grib #
      ###############################
      
      # Reading the geotiff file
      print(" - Reading the geotiff file...")
      File_geotiff = MainDirOUT + "/gpw_v4_population_density_rev11_" + str(Year) + "_" + Grid_Raw + ".tif"
      geotiff = rasterio.open(File_geotiff)

      # Extracting the population density values from the geotiff file
      print(" - Extracting the raw population density values from the geotiff file...")
      vals_array2d = np.array(geotiff.read(), dtype=float) [0,:,:].flatten()
      vals_array2d[vals_array2d == geotiff.nodata] = 0

      # Encoding the geotiff file as grib
      print(" - Encoding the geotiff file as grib...")
      ni, nj = (geotiff.width, geotiff.height)
      
      n, w, s, e = (
                  geotiff.bounds.top,
                  geotiff.bounds.left,
                  geotiff.bounds.bottom,
                  geotiff.bounds.right,
                  )
      
      di = (e - w) / ni
      dj = (n - s) / nj

      h = codes_grib_new_from_samples("regular_ll_sfc_grib2")
      
      codes_set(h, "Ni", ni)
      codes_set(h, "Nj", nj)
      codes_set(h, "iDirectionIncrementInDegrees", di)
      codes_set(h, "jDirectionIncrementInDegrees", dj)

      codes_set(h, "latitudeOfFirstGridPointInDegrees", min(90, n - dj / 2))
      codes_set(h, "latitudeOfLastGridPointInDegrees", max(-90, s + dj / 2))
      codes_set(h, "longitudeOfFirstGridPointInDegrees", w + di / 2)
      codes_set(h, "longitudeOfLastGridPointInDegrees", e - dj / 2)

      codes_set(h, "shortName", "lsm")

      codes_set_values(h, vals_array2d)

      # Saving NASA's raw population density as grib
      with open(MainDirOUT + "/PopDens_" +  Grid_Raw + "_" + str(Year) + (".grib", ".grib2")[codes_get(h, "edition") == 2], "wb") as f:
            codes_write(h, f)
      codes_release(h)