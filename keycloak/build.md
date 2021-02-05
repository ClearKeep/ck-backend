
sudo docker build . -t mykeycloak
sudo docker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin -v source=.clearkeep,target=/opt/jboss/keycloak/themes/clearkeep mykeycloak