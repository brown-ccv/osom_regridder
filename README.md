# OSOM Regridder

The OSOM Regridder is a Python package that's designed to transform OSOM data from the internal model grid to a visualizable latitude / longitude grid that can be plotted on a map.

## The Algorithm

The grid is transformed by creating a canvas in the output dimensions, and selected data, pixel by pixel, from the OSOM dataset. At each pixel, data is select based on the relative latitude / longitude positions of the input grid against the output canvas, and averaged in cases were multiple data points are select. Any pixel without a data point is treated as a masked value.

## Package Stuff

#### Format

```bash
uv format
```

#### Build

```bash
uv build
```
