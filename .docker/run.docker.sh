echo '~~~~~ Start build docker clearkeep-backend ~~~~~~~~~'
docker build --no-cache -t clearkeep -f ./.docker/clearkeep.dockerfile .
echo '~~~~~ Start run docker clearkeep-backend ~~~~~~~~~'
docker run --name clearkeep -p 5000:5000 clearkeep