from import_raster import import_grid, import_dataset
from regrid import populate_regrid
from output_image import create_image, save_image

grid_path = "data/osom_grid.nc"
data_path = "data/osom_data_6210.nc"
output_image_path = "out/osom_data_6210.png"
variable = "temp" # options: temp, salt, zeta, ubar_eastward, ubar_westward
surfaceOrBottom = "surface" # options: surface, bottom
time_point = 1
output_size_x = 260
output_size_y = 160

if __name__ == "__main__":
    lon, lat, mask, bathymetry = import_grid("data/osom_grid.nc")
    data = import_dataset(data_path, variable, surfaceOrBottom)
    data_at_timepoint = data[time_point]
    regridded = populate_regrid(output_size_x, output_size_y, lon, lat, data_at_timepoint)
    regridded_image = create_image(regridded, output_size_x, output_size_y)
    save_image(regridded_image, output_image_path)
