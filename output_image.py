from PIL import Image
import numpy as np

def normalize(v, v_scale_min, v_scale_max, o_scale_min, o_scale_max):
  '''
  Utility function to normalize model data for the creation of output images.
  '''
  standard_normalization = (v - v_scale_min) / (v_scale_max - v_scale_min)
  return ((o_scale_max - o_scale_min) * standard_normalization) + o_scale_min

def create_image(dataset, output_dim_x, output_dim_y):
  image = Image.new(mode="RGBA", size=(output_dim_x, output_dim_y), color = (0, 0, 0, 0))
  values = np.unique(dataset[~np.isnan(dataset)])
  output_min = np.min(values)
  output_max = np.max(values)
  for x in range(output_dim_x):
    for y in range(output_dim_y):
      value = dataset[x][y]
      if not np.isnan(value):
        color_as_value = int(normalize(value, output_min, output_max, 0, 255))
        image.putpixel((x, output_dim_y - 1 - y), (color_as_value, 0, color_as_value, 255))
  return image

def save_image(image, image_path):
  image.save(image_path)

if __name__ == "__main__":
  pass