# Pin to node:16.15.0
FROM node@sha256:9b8eb61072127e898d8d2682f28508937fc21a853c6cb5587fa14d8b05ab4455

WORKDIR /src
COPY ./ ./

# setup library
# TODO: pin pip version, don't do latest like this
RUN npm install

EXPOSE 12016
EXPOSE 19090
EXPOSE 10051

CMD LOG=debug node ./app.js 1 $PUBLIC_IP_ADDRESS 2>&1 | tee stdout-stderr_$(date +%a-%Y%b%d-%H%M-%S%z).log

