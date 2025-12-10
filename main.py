from file_input import import_grid, import_dataset
from regrid import populate_regrid
from output import create_image, save_image, save_dataset

grid_path = "data/osom_grid.nc"
data_path = "data/osom_data_6210.nc"
output_image_path = "out/osom_data_6210-small.png"
output_nc_path = "out/osom_data_6210-small.nc"
variable = "temp" # options: temp, salt, zeta, ubar_eastward, ubar_westward
surfaceOrBottom = "surface" # options: surface, bottom
time_point = 1
output_size_x = 26
output_size_y = 16

if __name__ == "__main__":
    lat, lon, mask, bathymetry = import_grid("data/osom_grid.nc")
    data = import_dataset(data_path, variable, surfaceOrBottom)
    data_at_timepoint = data[time_point]
    regridded = populate_regrid(output_size_x, output_size_y, lon, lat, data_at_timepoint)
    regridded_image = create_image(regridded, output_size_x, output_size_y)
    save_image(regridded_image, output_image_path)
    save_dataset(regridded, variable, output_nc_path)
