FROM datasetteproject/datasette:0.54

RUN apt update \
 && apt install -y git \
 && apt clean

RUN pip install \
          datasette-leaflet-geojson \
          datasette-render-timestamps \
          github-to-sqlite \
          pocket-to-sqlite \
          twitter-to-sqlite \
          dogsheep-beta \
          dropbox
