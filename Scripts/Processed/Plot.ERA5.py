import metview as mv

tp_temp1 = mv.retrieve(
    class_ = "ea",
    date = "2021-03-27",
    expver = 1,
    levtype = "sfc",
    param = "228.128",
    step = [7, 8, 9, 10, 11, 12],
    stream = "oper",
    time = "18:00:00",
    type = "fc"
)

tp_temp2 = mv.retrieve(
    class_ = "ea",
    date = "2021-03-28",
    expver = 1,
    levtype = "sfc",
    param = "228.128",
    step = [1, 2, 3, 4, 5, 6],
    stream = "oper",
    time = "06:00:00",
    type = "fc"
)

tp = (mv.sum(tp_temp1) + mv.sum(tp_temp2)) * 1000

# Plot the rainfall climatology
coastlines = mv.mcoast(
      map_coastline_colour = "charcoal",
      map_coastline_thickness = 2,
      map_coastline_resolution = "full",
      map_coastline_sea_shade = "on",
      map_coastline_sea_shade_colour = "rgb(0.665,0.9193,0.9108)",
      map_boundaries = "on",
      map_boundaries_colour = "charcoal",
      map_boundaries_thickness = 4,
      map_grid_latitude_increment = 10,
      map_grid_longitude_increment = 20,
      map_label_right = "off",
      map_label_top = "off",
      map_label_colour = "charcoal",
      map_grid_thickness = 1,
      map_grid_colour = "charcoal",
      map_label_height = 0.7
      )

contouring = mv.mcont(
      legend = "on",
      contour = "off",
      contour_level_selection_type = "level_list",
      contour_level_list = [0,0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500,5000],
      contour_label = "off",
      contour_shade = "on",
      contour_shade_colour_method = "list",
      contour_shade_method = "area_fill",
      contour_shade_colour_list = ["white","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)","RGB(1,0.73,0.0039)","RGB(1,0.49,0.0039)","red","RGB(0.85,0.0039,1)","RGB(0.63,0.0073,0.92)","RGB(0.37,0.29,0.91)","RGB(0.04,0.04,0.84)","RGB(0.042,0.042,0.43)","RGB(0.45,0.45,0.45)"]
      )

legend = mv.mlegend(
      legend_text_colour = "charcoal",
      legend_text_font_size = 0.5,
      )

title = mv.mtext(
      text_line_count = 3,
      text_line_1 = "ERA5 Rainfall",
      text_line_2 = "VT: 2024-04-24 00 UTC to 2024-04-24 12 UTC",
      text_line_3 = " ",
      text_colour = "charcoal",
      text_font_size = 0.75
      )

mv.plot(tp, coastlines, contouring, legend, title)