# OpenInfraMap Nighttime Lights Pipeline

This contains some messy tooling to generate a tiled basemap of nighttime lights from NASA's [SNPP VIIRS data](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4/).

It produces a pmtiles file which is served by Cloudflare Workers.

I looked at the World Bank's [blackmarblepy](https://github.com/worldbank/blackmarblepy) tool, but I ran into quite a lot of bugs and it seemed like overkill when I needed to download the whole dataset anyway. I landed on this solution using only GDAL (and a couple of helper scripts).

# Method
It's a pretty manual process at the moment. You'll need to create a `.env` file with the contents:

    BLACKMARBLE_TOKEN=<token>

Where `<token>` is generated from your NASA Earthdata user account. Note that these tokens expire after 2 months so if you're only running this annually you'll definitely need a new one.

Then run:

    python3 ./download-files.py
    python3 ./generate-vrt.py > ./black-marble.vrt
    gdal_translate -co COMPRESS=LZW ./black-marble.vrt ./black-marble.tif

At this point we need to apply a color gradient, which I currently achieve with QGIS, although previously I've used `gdaldem` with the included colormap.txt (the thresholds on this are now wrong though).

    gdal_translate -of mbtiles -co NAME="Nighttime Lights" -co TYPE=baselayer -co TILE_FORMAT=webp -projwin -180 85.05 180 -85.05 ./black-marble-mapped.tif ./black-marble.mbtiles
    gdaladdo ./black-marble.mbtiles
    pmtiles convert ./black-marble.mbtiles ./black-marble-2023.pmtiles

You might need to run `download-files.py` multiple times if any downloads fail as there's no retry logic, but it'll only download missing files.
