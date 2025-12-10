import netCDF4 as nc
import numpy as np

def get_coordinates_for_point(x, y, lon_cell_size, lat_cell_size, lon_min, lat_min):
  '''
  Determines the latitude and longitude bounds of a pixel in the output grid.
  '''
  # Note (AM): This is a method that's a little flawed right now. This will collect
  # all points enclosed by a lat/lon region. For low density regriddings, it's 
  # totally okay, but for higher density ones it's a little worse. For example, it's
  # possible to imagine a dataset pixel that encloses entirely a regridding pixel, which
  # would be skipped under the current algorithm. In effect, this only detects the *edges*
  # of dataset pixels, not the pixels themselves. 
  cell_lon_min = (x * lon_cell_size) + lon_min
  cell_lon_max = ((x + 1) * lon_cell_size) + lon_min
  cell_lat_min = (y * lat_cell_size) + lat_min
  cell_lat_max = ((y + 1) * lat_cell_size) + lat_min
  return (cell_lon_min, cell_lon_max, cell_lat_min, cell_lat_max)

def get_data_for_points(x_mask, y_mask, dataset):
  '''
  Determines the data for points determined to be within the bounds of output grid cell.
  '''
  collected_data = []
  for i in range(len(x_mask)):
    data = dataset[x_mask[i]][y_mask[i]]
    collected_data.append(data)
  return collected_data

def get_model_data_at_point(x, y, grid_lon, grid_lat, dataset, lon_cell_size, lat_cell_size, lon_min, lat_min):
  '''
  Determines the output grid cell value based on values extracted from the dataset.
  '''
  cell_lon_min, cell_lon_max, cell_lat_min, cell_lat_max = get_coordinates_for_point(x, y, lon_cell_size, lat_cell_size, lon_min, lat_min)
  lon_mask = (grid_lon > cell_lon_min) & (grid_lon < cell_lon_max)
  lat_mask = (grid_lat > cell_lat_min) & (grid_lat < cell_lat_max)
  x_mask, y_mask = np.where(lon_mask & lat_mask)
  bounded_points = get_data_for_points(x_mask, y_mask, dataset)
  if len(bounded_points) >= 1:
    averaged_points = np.average(bounded_points)
    return averaged_points
  else:
    return np.nan

def populate_regrid(size_x, size_y, grid_lon, grid_lat, dataset):
  '''
  Creates a lat/lon output grid based on an input dataset.

  At each output grid cell value, dataset points are collected if they fall within lat/lon
  bounds, and averaged together to give a single output value. This is repeated across the 
  entire output grid to create a regridded raster.
  '''
  regrid = np.empty((size_x, size_y))
  regrid.fill(np.nan)

  lat_min = np.min(grid_lat)
  lat_max = np.max(grid_lat)
  lon_min = np.min(grid_lon)
  lon_max = np.max(grid_lon)

  lat_range = lat_max - lat_min
  lon_range = lon_max - lon_min

  lat_cell_size = lat_range / size_y
  lon_cell_size = lon_range / size_x

  # Note (AM): This is a prime candidate for parallelization / other optimization. Iterating
  # through all x / y coordinates is a naive O(N^2) implementation. And while it works as a 
  # proof of concept, it can probably be improved prior to processing an entire dataset. The
  # value for each grid cell can be computed in parallel, potentially speeding up this process
  # dramatically. Additionally, we know that many output grid cells will simply not have data.
  # There might be a heuristic we can use to determine if certain lat / lon ranges can be skipped
  # outright, reducing the effective value of N for the time complexity of this function.
  for x in range(size_x):
    #print(x, "/", size_x)
    for y in range(size_y):
      regrid[x][y] = get_model_data_at_point(x, y, grid_lon, grid_lat, dataset, lon_cell_size, lat_cell_size, lon_min, lat_min)
  return regrid

  