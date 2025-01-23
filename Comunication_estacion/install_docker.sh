#/bin/bash
curl -fsSL test.docker.com -o get-docker.sh && sh get-docker.sh
sudo usermod -aG docker ${USER}
newgrp docker
sudo apt install docker-compose
sudo systemctl enable docker


