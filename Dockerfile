FROM datasetteproject/datasette:0.54

RUN apt-get update -qq \
 && apt-get install -y --no-install-recommends git \
 && apt-get autoclean \
 && apt-get autoremove \
 && apt-get clean

RUN pip install \
          datasette-leaflet-geojson \
          datasette-render-timestamps \
          github-to-sqlite \
          pocket-to-sqlite \
          twitter-to-sqlite \
          dogsheep-beta \
          dropbox
