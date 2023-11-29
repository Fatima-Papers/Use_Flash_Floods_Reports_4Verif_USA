#     - identify the nearest grid-boxese to the centre of the area affected: six new columns are created "NEAREST_DOMAIN_GRIDBOX_CENTRE_LAT", "NEAREST_DOMAIN_GRIDBOX_CENTRE_LON", "NEAREST_DOMAIN_GRIDBOX_WEST", "NEAREST_DOMAIN_GRIDBOX_EAST", "NEAREST_DOMAIN_GRIDBOX_NORTH", and "NEAREST_DOMAIN_GRIDBOX_SOUTH".




FileIN_Mask = "Data/Raw/Mask_USA_ENS/Mask.grib"



# Reading the domain's mask
mask = mv.read(Git_Repo + "/" + FileIN_Mask)
mask_lats = mv.latitudes(mask)
mask_lons = mv.longitudes(mask)



listdef = mv.nearest_gridpoint_info(mask,area_affected_centre_lat, area_affected_centre_lon)[0]
            print(listdef)
            nearest_domain_gridbox_centre_lat = listdef["latitude"]
            nearest_domain_gridbox_centre_lon = listdef["longitude"] + 360
            index_grid = int(listdef["index"])
            nearest_domain_gridbox_west = round(mask_lons[index_grid-1],4)
            nearest_domain_gridbox_east = round(mask_lons[index_grid+1],4)
            print(nearest_domain_gridbox_west)
            print(nearest_domain_gridbox_centre_lon)
            print(nearest_domain_gridbox_east)