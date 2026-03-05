import os
import osgeo
from pathlib import Path
from osgeo import gdal


def convert_image_to_tiles(src: str, dst: str):
    gdal.Translate(
        dst,
        src,
        format="MBTILES",
        outputBounds=[-72.7, 41.9, -69.96, 40.5],
        outputSRS="EPSG:4326",
    )


def add_layers_to_tiles(src: str):
    # https://stackoverflow.com/a/61117295
    tiles = gdal.Open(src, gdal.GA_Update)
    gdal.SetConfigOption("COMPRESS_OVERVIEW", "DEFLATE")
    tiles.BuildOverviews("AVERAGE", [2, 4, 8, 16, 32, 64, 128, 256])
    tiles = None


def make_mbtile(src: str, dst: str):
    convert_image_to_tiles(src, dst)
    add_layers_to_tiles(dst)


def make_mbtile_for_dir(src_dir: str, dst_dir: str):
    dst_path = Path(dst_dir)
    for src_file in Path(src_dir).iterdir():
        if src_file.is_file() and src_file.name.endswith(".tif"):
            print("Making .mbtiles for", src_file.name)
            dst_name = dst_path / (src_file.stem + ".mbtiles")
            make_mbtile(src_file, dst_name)
        else:
            print("Skipping", src_file.name)
