FROM datasetteproject/datasette:0.54

RUN pip install \
          datasette-render-timestamps \
          github-to-sqlite \
          pocket-to-sqlite \
          twitter-to-sqlite \
          dogsheep-beta
