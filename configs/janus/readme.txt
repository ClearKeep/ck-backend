#run in server to replace configuration
docker cp /home/ubuntu/ck-backend/configs/janus/janus.jcfg docker_janus_webrtc_1:/usr/local/etc/janus
docker cp /home/ubuntu/ck-backend/configs/janus/janus.transport.http.jcfg docker_janus_webrtc_1:/usr/local/etc/janus
docker stop docker_janus_webrtc_1
docker start docker_janus_webrtc_1