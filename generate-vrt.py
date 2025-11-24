import re
from pathlib import Path

data_dir = Path("./data")

WIDTH_TILES = 36
HEIGHT_TILES = 18

TILE_WIDTH = 2400
TILE_HEIGHT = 2400

WIDTH = WIDTH_TILES * TILE_WIDTH
HEIGHT = HEIGHT_TILES * TILE_HEIGHT

print(
    f"""
      <VRTDataset rasterXSize="{WIDTH}" rasterYSize="{HEIGHT}">
  <SRS dataAxisToSRSAxisMapping="2,1">GEOGCS["Unknown datum based upon the GRS 1980 Authalic Sphere ellipsoid",DATUM["Not specified (based on GRS 1980 Authalic Sphere spheroid)",SPHEROID["GRS 1980 Authalic Sphere",6370997,0,AUTHORITY["EPSG","7047"]]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST]]</SRS>
  <GeoTransform> -1.8000000000000000e+02,  4.1666666666666666e-03,  0.0000000000000000e+00,  9.0000000000000000e+01,  0.0000000000000000e+00, -4.1666666666666666e-03</GeoTransform>"""
)

print(
    """<VRTRasterBand dataType="Float32" band="1">
    <NoDataValue>65535</NoDataValue>
    <Scale>1</Scale>"""
)

for name in data_dir.glob("*.h5"):
    match = re.search(r"h([0-9]{2})v([0-9]{2})", name.stem)
    if not match:
        raise ValueError(f"Could not parse {name}")
    x, y = int(match.group(1)), int(match.group(2))

    print(" <ComplexSource>")
    print(
        f'  <SourceFilename relativeToVRT="1">HDF5:"{name}"://HDFEOS/GRIDS/VIIRS_Grid_DNB_2d/Data_Fields/AllAngle_Composite_Snow_Free</SourceFilename>'
    )
    print("<SourceBand>1</SourceBand>")
    print(f'<SrcRect xOff="0" yOff="0" xSize="{TILE_WIDTH}" ySize="{TILE_HEIGHT}"/>')
    print(
        f'<DstRect xOff="{x*TILE_WIDTH}" yOff="{int(y)*TILE_HEIGHT}" xSize="{TILE_WIDTH}" ySize="{TILE_HEIGHT}"/>'
    )
    print("<NODATA>65535</NODATA>")
    print(" </ComplexSource>")

print("</VRTRasterBand>")
print("</VRTDataset>")
