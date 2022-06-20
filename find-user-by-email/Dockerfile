# Pin to node:16.15.0
FROM node:16.15-slim

WORKDIR /src
COPY ./ ./

# setup library
# TODO: pin pip version, don't do latest like this
RUN npm install

EXPOSE 12016
EXPOSE 19090
EXPOSE 10051

CMD node ./app.js --ip $PUBLIC_IP_ADDRESS --type $TYPE --db $ORBITDB

