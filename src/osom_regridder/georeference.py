from osgeo import gdal
import osgeo
from pathlib import Path


def make_mbtile(src: str, dst: str):
    # https://stackoverflow.com/a/61117295
    image = gdal.Open(src)
    gdal.SetConfigOption("COMPRESS_OVERVIEW", "DEFLATE")
    image.BuildOverviews("AVERAGE", [2, 4, 8, 16, 32, 64, 128, 256])
    kwargs = {
        "format": "MBTILES",
        "projWin": [-72.7, 41.9, -69.96, 40.5],
        "projWinSRS": "EPSG:4326",
    }

    gdal.Translate(dst, src, **kwargs)


def make_mbtile_for_dir(src_dir: str, dst_dir: str):
    dst_path = Path(dst_dir)
    for src_file in Path(src_dir).iterdir():
        if src_file.is_file():
            dst_name = dst_path / (src_file.stem + ".mbtiles")
            make_mbtile(src_file, dst_name)
