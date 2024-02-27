import os
import zipfile
import rasterio
import numpy as np
import metview as mv
from eccodes import *

################################################################################
# CODE DESCRIPTION
# 09_Compute_ExtractRaw_Regrid_PopDens.py reads NASA's population density at different 
# resolutions (as geotiff files), and extracts some statistics (e.g. max or average) for each grid-box 
# in the grid of interest. It finally saves both resolution datasets (raw and regridded) as grib files. 
# Runtime: the runtime of the code varies significantly according to the resolution of the raw data. 
# It can take up to 10 seconds to run in serial for raw data with 15min resolution (30 km), and up 
# to 30 minutes for raw data with 30sec resolution (1km).

# INPUT PARAMETERS DESCRIPTION
# Year_S (integer, in YYYY format): start year to consider.
# Year_F (integer, in YYYY format): final year to consider.
# Disc_Year (integer): discretization for the years to consider.
# Grid_Raw (string): grid of NASA's raw dataset.
# Grid_2_Interpolate (string): grid to interpolate onto (e.g. "n320" for ERA5's grid).
# Git_Repo (string): repository's local path
# DirIN (string): relative path containing NASA's raw population density.
# DirOUT (string): relative path containing the extracted raw and interpolated population density.

# INPUT PARAMETERS
Year_S = 2000
Year_F = 2020
Disc_Year = 5
Grid_Raw = "15_min"
Grid_2_Interpolate = "n320"
Git_Repo = "/ec/vol/ecpoint_dev/mofp/Papers_2_Write/Use_FlashFloodsRep_4Verif_USA"
DirIN = "Data/Raw/OBS/NASA_PopDens"
DirOUT = "Data/Compute/09_ExtractRaw_Regrid_PopDens"
################################################################################

PopDens_all = None

for Year in range(Year_S, Year_F+1, Disc_Year):

      print(" ")
      print("Post-processing NASA's population dataset for year: " + str(Year))

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

      codes_set(h, "paramId", "167")
      codes_set(h, "bitmapPresent", 0)
      codes_set(h, "bitsPerValue", "16")

      codes_set_values(h, vals_array2d)

      # Saving NASA's raw population density as grib
      with open(MainDirOUT + "/PopDens_" +  Grid_Raw + "_" + str(Year) + (".grib", ".grib2")[codes_get(h, "edition") == 2], "wb") as f:
            codes_write(h, f)
      codes_release(h)


      #############################################
      # Interpolating NASA's raw dataset into required grid  #
      #############################################

      # Interpolating to required grid
      pop_dens_raw = mv.read(MainDirOUT + "/PopDens_" +  Grid_Raw + "_" + str(Year) + ".grib2")

      pop_dens_regridded = mv.regrid(
            grid = Grid_2_Interpolate,
            interpolation = "grid_box_statistics", # voronoid_statistics, grid_box_statistics
            interpolation_statistics = "maximum",
            data = pop_dens_raw
      )

      # Encoding nan values in the regridded dataset 
      lsm = mv.retrieve(
            class_ = "ea",
            date = "1940-01-01",
            expver = 1,
            levtype = "sfc",
            param = "lsm",
            step = 0,
            stream = "oper",
            time = "00:00:00",
            type = "an"
            )
      lsm_nan = mv.bitmap(lsm, 0)
      pop_dens_regridded = mv.bitmap(mv.set_values(lsm, mv.values(pop_dens_regridded)), lsm_nan)

      # Saving regridded population density as grib
      mv.write(MainDirOUT + "/PopDens_" + str(Year) + "_" +  Grid_2_Interpolate + "_from_" + Grid_Raw + ".grib2", pop_dens_regridded)

      # Merging to the previous years the values of population density for the correspondent year
      PopDens_all = mv.merge(PopDens_all, pop_dens_regridded)

# Creating the average populaiton density over all the considered years
print(" ")
print("Saving the average population density over the considered period of time...")
PopDens_av = mv.mean(PopDens_all)
MainDirOUT = Git_Repo + "/" + DirOUT
mv.write(MainDirOUT + "/PopDens_mean_" +  Grid_2_Interpolate + "_from_" + Grid_Raw + ".grib2", PopDens_av)
